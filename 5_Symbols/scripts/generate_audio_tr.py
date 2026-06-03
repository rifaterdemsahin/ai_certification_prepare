#!/usr/bin/env python3
"""
Generate Turkish TTS audio for all exam questions using Kokoro FastAPI (local Docker),
then upload each MP3 to Azure Blob Storage (memory-audio container) and add
audioUrlTr to questions.json.

Turkish framing: "Soru {N}. {question} ... Cevap: {answer}"
The structural labels are in Turkish; technical content stays in English.
This serves multilingual learners who benefit from Turkish framing
while studying English-language technical certification content.

Prerequisites:
    pip install azure-storage-blob requests
    docker run -d --name kokoro-tts -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu:latest

Environment:
    AZURE_STORAGE_CONNECTION_STRING  — Azure storage connection string
    AZURE_STORAGE_KEY                — Azure storage account key (alternative)

Usage:
    cd 5_Symbols/scripts
    python generate_audio_tr.py [--dry-run] [--start-id 1] [--end-id 102]
"""

import os
import sys
import json
import time
import argparse
import tempfile
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

# ── Config ──────────────────────────────────────────────────────────────────
KOKORO_URL = "http://localhost:8880/v1/audio/speech"
CONTAINER_NAME = "memory-audio"
AZURE_BASE = "https://claudecertstore.blob.core.windows.net"
VOICE = "af_heart"
SPEED = 0.85  # slightly slower for non-native Turkish comprehension
DATA_DIR = Path(__file__).parent.parent / "data"
QUESTIONS_FILE = DATA_DIR / "questions.json"


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
        "input": text,
        "voice": VOICE,
        "response_format": "mp3",
        "speed": SPEED,
    }
    r = requests.post(KOKORO_URL, json=payload, timeout=60)
    r.raise_for_status()
    return r.content


def get_blob_client(connection_string: str = None, account_key: str = None):
    if connection_string:
        client = BlobServiceClient.from_connection_string(connection_string)
    elif account_key:
        client = BlobServiceClient(
            account_url="https://claudecertstore.blob.core.windows.net",
            credential=account_key,
        )
    else:
        raise ValueError("Either connection_string or account_key must be provided")

    container = client.get_container_client(CONTAINER_NAME)
    try:
        container.get_container_properties()
    except Exception:
        print(f"📦 Creating container '{CONTAINER_NAME}'...")
        container.create_container(public_access="blob")
        print(f"✅ Container '{CONTAINER_NAME}' created\n")
    return client


def blob_exists(client, blob_name: str) -> bool:
    blob = client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
    try:
        blob.get_blob_properties()
        return True
    except Exception:
        return False


def upload_mp3(client, blob_name: str, data: bytes) -> str:
    blob = client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
    blob.upload_blob(
        data,
        overwrite=True,
        content_settings=ContentSettings(content_type="audio/mpeg"),
    )
    return f"{AZURE_BASE}/{CONTAINER_NAME}/{blob_name}"


def build_tts_text_tr(q: dict) -> str:
    """Turkish-framed spoken text. Labels in Turkish; content in English.
    Pattern: Soru {N}. {question} ... Cevap: {answer}
    """
    return f"Soru {q['id']}. {q['question']} ... Cevap: {q['answer']}"


def main():
    parser = argparse.ArgumentParser(description="Generate Turkish TTS audio for exam questions")
    parser.add_argument("--dry-run", action="store_true", help="Generate MP3 locally, skip upload")
    parser.add_argument("--start-id", type=int, default=1, help="First question ID")
    parser.add_argument("--end-id", type=int, default=102, help="Last question ID")
    parser.add_argument("--force", action="store_true", help="Overwrite existing blobs")
    args = parser.parse_args()

    if not QUESTIONS_FILE.exists():
        print(f"❌ questions.json not found at {QUESTIONS_FILE}")
        sys.exit(1)

    with open(QUESTIONS_FILE) as f:
        data = json.load(f)

    questions = data.get("questions", data) if isinstance(data, dict) else data
    questions = [q for q in questions if args.start_id <= q["id"] <= args.end_id]
    print(f"📋 Processing {len(questions)} questions (IDs {args.start_id}–{args.end_id})\n")

    if not wait_for_kokoro():
        print("❌ Kokoro is not reachable. Start it with:")
        print("   docker run -d --name kokoro-tts -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu:latest")
        sys.exit(1)

    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    account_key = os.getenv("AZURE_STORAGE_KEY")

    if not conn_str and not account_key and not args.dry_run:
        print("❌ Set AZURE_STORAGE_CONNECTION_STRING or AZURE_STORAGE_KEY")
        sys.exit(1)

    az_client = get_blob_client(conn_str, account_key) if not args.dry_run else None

    updated = skipped = errors = 0

    for q in questions:
        pad_id = str(q["id"]).zfill(3)
        blob_name = f"AUD-Q{pad_id}-TR.mp3"
        audio_url = f"{AZURE_BASE}/{CONTAINER_NAME}/{blob_name}"

        if not args.dry_run and not args.force and blob_exists(az_client, blob_name):
            print(f"⏭  Q{pad_id} TR — already exists, skipping")
            q["audioUrlTr"] = audio_url
            skipped += 1
            continue

        text = build_tts_text_tr(q)
        print(f"🎙️  Q{pad_id} TR — generating ({len(text)} chars)…")

        try:
            mp3_bytes = generate_mp3(text)
        except Exception as e:
            print(f"   ❌ Kokoro error: {e}")
            errors += 1
            continue

        if args.dry_run:
            tmp = Path(tempfile.gettempdir()) / blob_name
            tmp.write_bytes(mp3_bytes)
            print(f"   💾 Dry-run: saved to {tmp} ({len(mp3_bytes):,} bytes)")
        else:
            try:
                url = upload_mp3(az_client, blob_name, mp3_bytes)
                q["audioUrlTr"] = url
                print(f"   ✅ Uploaded → {url}")
                updated += 1
            except Exception as e:
                print(f"   ❌ Upload error: {e}")
                errors += 1

    if not args.dry_run and (updated > 0 or skipped > 0):
        with open(QUESTIONS_FILE, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n✅ questions.json updated with audioUrlTr entries")

    print(f"\n📊 Summary: {updated} uploaded, {skipped} skipped, {errors} errors")


if __name__ == "__main__":
    main()
