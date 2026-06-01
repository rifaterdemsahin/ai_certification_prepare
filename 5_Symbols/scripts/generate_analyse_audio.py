#!/usr/bin/env python3
"""
Generate TTS audio for all analyse pages using Kokoro FastAPI (local Docker),
then upload each MP3 to Azure Blob Storage (analyse-audio container).

Prerequisites:
    pip install azure-storage-blob requests
    docker run -d --name kokoro-tts -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu:latest

Environment:
    AZURE_STORAGE_CONNECTION_STRING  — Azure storage connection string

Usage:
    cd 5_Symbols/scripts
    python generate_analyse_audio.py [--dry-run] [--force]
"""

import os
import sys
import json
import time
import argparse
import re
from html.parser import HTMLParser
from pathlib import Path

try:
    import requests
except ImportError:
    print("❌ requests not installed — run: pip install requests")
    sys.exit(1)

try:
    from azure.storage.blob import BlobServiceClient, ContentSettings
except ImportError:
    print("❌ azure-storage-blob not installed — run: pip install azure-storage-blob")
    sys.exit(1)

# ── Config ───────────────────────────────────────────────────────────────────
KOKORO_URL      = "http://localhost:8880/v1/audio/speech"
AUDIO_CONTAINER = "analyse-audio"
PAGES_CONTAINER = "analyse-pages"
AZURE_BASE      = "https://claudecertstore.blob.core.windows.net"
VOICE           = "af_heart"
SPEED           = 0.9

DATA_DIR  = Path(__file__).parent.parent / "data"
MENU_FILE = DATA_DIR / "menu.json"


# ── HTML → plain text ────────────────────────────────────────────────────────
class _TextExtractor(HTMLParser):
    SKIP_TAGS = {"script", "style", "head", "nav", "footer"}

    def __init__(self):
        super().__init__()
        self._skip_depth = 0
        self.chunks = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data):
        if not self._skip_depth:
            text = data.strip()
            if text:
                self.chunks.append(text)


def html_to_text(html: str) -> str:
    parser = _TextExtractor()
    parser.feed(html)
    raw = " ".join(parser.chunks)
    # collapse extra whitespace
    return re.sub(r"\s{2,}", " ", raw).strip()


# ── Kokoro helpers ───────────────────────────────────────────────────────────
def wait_for_kokoro(retries: int = 12, delay: float = 5.0) -> bool:
    print("⏳ Waiting for Kokoro to be ready...")
    for i in range(retries):
        try:
            r = requests.get("http://localhost:8880/v1/models", timeout=3)
            if r.status_code == 200:
                print("✅ Kokoro is ready\n")
                return True
        except requests.exceptions.ConnectionError:
            pass
        print(f"   ... attempt {i+1}/{retries}")
        time.sleep(delay)
    return False


def generate_mp3(text: str) -> bytes:
    payload = {
        "model": "kokoro",
        "input": text[:4096],   # guard against very long pages
        "voice": VOICE,
        "response_format": "mp3",
        "speed": SPEED,
    }
    r = requests.post(KOKORO_URL, json=payload, timeout=120)
    r.raise_for_status()
    return r.content


# ── Azure helpers ────────────────────────────────────────────────────────────
def get_az_client(conn_str: str) -> BlobServiceClient:
    client = BlobServiceClient.from_connection_string(conn_str)
    container = client.get_container_client(AUDIO_CONTAINER)
    try:
        container.get_container_properties()
    except Exception:
        print(f"📦 Creating container '{AUDIO_CONTAINER}'...")
        container.create_container(public_access="blob")
        print(f"✅ Container created with public read access\n")
    return client


def blob_exists(client: BlobServiceClient, blob_name: str) -> bool:
    blob = client.get_blob_client(container=AUDIO_CONTAINER, blob=blob_name)
    try:
        blob.get_blob_properties()
        return True
    except Exception:
        return False


def upload_mp3(client: BlobServiceClient, blob_name: str, data: bytes) -> str:
    blob = client.get_blob_client(container=AUDIO_CONTAINER, blob=blob_name)
    blob.upload_blob(
        data,
        overwrite=True,
        content_settings=ContentSettings(content_type="audio/mpeg"),
    )
    return f"{AZURE_BASE}/{AUDIO_CONTAINER}/{blob_name}"


# ── Page discovery ───────────────────────────────────────────────────────────
def get_analyse_pages() -> list[dict]:
    """Return list of {page, label} for all analyse_renderer.html?page= items."""
    with open(MENU_FILE) as f:
        menu = json.load(f)

    pages = []
    for section in menu:
        if "3. Analyse" not in section.get("label", ""):
            continue
        for item in section.get("items", []):
            href = item.get("href", "")
            if "analyse_renderer.html?page=" in href and not item.get("external"):
                page_file = href.split("?page=")[1]
                pages.append({"page": page_file, "label": item.get("label", page_file)})
    return pages


def fetch_page_html(page_file: str) -> str:
    url = f"{AZURE_BASE}/{PAGES_CONTAINER}/{page_file}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Generate Kokoro TTS for analyse pages")
    parser.add_argument("--dry-run", action="store_true", help="Generate MP3 but do not upload")
    parser.add_argument("--force", action="store_true", help="Re-generate even if blob already exists")
    args = parser.parse_args()

    pages = get_analyse_pages()
    print(f"📋 Found {len(pages)} analyse pages to process\n")

    if not wait_for_kokoro():
        print("❌ Kokoro is not reachable. Start it with:")
        print("   docker run -d --name kokoro-tts -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu:latest")
        sys.exit(1)

    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not conn_str and not args.dry_run:
        print("❌ AZURE_STORAGE_CONNECTION_STRING not set")
        sys.exit(1)

    az_client = get_az_client(conn_str) if not args.dry_run else None

    uploaded = skipped = errors = 0

    for item in pages:
        page_file = item["page"]
        stem = page_file.replace(".html", "")
        blob_name = f"ANA-{stem}.mp3"

        if not args.dry_run and not args.force and blob_exists(az_client, blob_name):
            print(f"⏭  {page_file} — already exists, skipping")
            skipped += 1
            continue

        print(f"🌐 Fetching {page_file}...")
        try:
            html = fetch_page_html(page_file)
        except Exception as e:
            print(f"   ❌ Could not fetch page: {e}")
            errors += 1
            continue

        text = html_to_text(html)
        if not text:
            print(f"   ⚠️  No text extracted from {page_file}, skipping")
            skipped += 1
            continue

        print(f"🎙️  Generating audio for '{item['label']}' ({len(text)} chars)...")
        try:
            mp3_bytes = generate_mp3(text)
        except Exception as e:
            print(f"   ❌ Kokoro error: {e}")
            errors += 1
            continue

        if args.dry_run:
            print(f"   💾 Dry-run: would upload {blob_name} ({len(mp3_bytes):,} bytes)")
        else:
            try:
                url = upload_mp3(az_client, blob_name, mp3_bytes)
                print(f"   ✅ Uploaded → {url}")
                uploaded += 1
            except Exception as e:
                print(f"   ❌ Upload error: {e}")
                errors += 1

    print(f"\n📊 Summary: {uploaded} uploaded, {skipped} skipped, {errors} errors")


if __name__ == "__main__":
    main()
