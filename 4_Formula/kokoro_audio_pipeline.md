# 🎙️ Kokoro Audio Pipeline — Formula

How we turn 100 exam Q&A cards into streamable MP3s on Azure, wired to a play button in `remember.html`.

---

## 🗺️ Pipeline Overview

```
questionsData (data.js)
        │
        │  build_tts_text()
        ▼
"Question 1. What are the three stages... Answer: Perceive, Think, Act."
        │
        │  POST /v1/audio/speech
        ▼
Kokoro FastAPI (Docker, localhost:8880)
        │
        │  audio/mpeg bytes
        ▼
Azure Blob Storage  →  memory-audio/AUD-Q001.mp3  (public read)
        │
        │  audioUrl baked into data.js
        ▼
remember.html  →  🔊 Play Audio button
```

---

## Step 1 — Text Construction

Each card's spoken text is assembled as:

```
"Question {id}. {question} ... Answer: {answer}"
```

Example for Q1:
> *"Question 1. What are the three stages of an Agentic Loop? ... Answer: Perceive, Think, and Act. The agent observes its environment, reasons about the observation, and takes action."*

The `...` pause gives a natural gap between question and answer when listening.

---

## Step 2 — Kokoro TTS Request

```python
POST http://localhost:8880/v1/audio/speech
{
  "model": "kokoro",
  "input": "<spoken text>",
  "voice": "af_heart",       # warm female voice
  "response_format": "mp3",
  "speed": 0.9               # slightly slower = better for study
}
```

Response body is raw MP3 bytes. No API key needed (local Docker).

---

## Step 3 — Azure Upload

Container: `memory-audio` (public blob read, no SAS needed for playback)

```python
blob.upload_blob(
    mp3_bytes,
    overwrite=True,
    content_settings=ContentSettings(content_type="audio/mpeg"),
)
```

Naming convention: `AUD-Q{padId}.mp3` — e.g. `AUD-Q001.mp3`, `AUD-Q042.mp3`

Public URL pattern:
```
https://claudecertstore.blob.core.windows.net/memory-audio/AUD-Q{padId}.mp3
```

---

## Step 4 — data.js Wiring

`data.js` sets `audioUrl` for every question at load time using the predictable URL pattern:

```js
q.audioUrl = q.audioUrl || `https://claudecertstore.blob.core.windows.net/memory-audio/AUD-Q${padId}.mp3`;
```

This means the play button appears immediately without needing a separate API call to discover which files exist.

---

## Step 5 — Play Button in remember.html

The button is rendered only when `audioUrl` is set (which is now always):

```js
const audioBtn = audioUrl ? `
    <button class="remember-audio-btn" id="audio-btn-${q.id}"
        onclick="event.stopPropagation(); playAudio('${audioUrl}', ${q.id})">
        🔊 Play Audio
    </button>` : '';
```

`playAudio()` streams directly from Azure — no download, no buffering delay.
Toggle behaviour: click once to play, click again to stop.

---

## Re-Running / Updating Audio

| Scenario | Action |
|----------|--------|
| Update one card's text | Delete blob from Azure, re-run script with `--start-id N --end-id N` |
| Regenerate all | Delete all blobs in `memory-audio`, re-run without flags |
| New voice | Change `VOICE` constant in `generate_audio.py`, re-run |
| Dry-run test | `python generate_audio.py --dry-run` — saves MP3 to `/tmp`, no upload |

---

## Skip Logic

The script checks Azure before calling Kokoro:

```python
if blob_exists(az_client, blob_name):
    print(f"⏭  Q{pad_id} — already exists, skipping")
```

This makes re-runs safe and cheap — only missing files are regenerated.

---

## Files Involved

| File | Role |
|------|------|
| `5_Symbols/scripts/generate_audio.py` | English audio pipeline |
| `5_Symbols/scripts/generate_audio_tr.py` | Turkish audio pipeline |
| `5_Symbols/js/data.js` | Bakes `audioUrl` + `audioUrlTr` into every question object |
| `5_Symbols/data/questions.json` | Updated with `audioUrl` and `audioUrlTr` after upload |
| `5_Symbols/pages/remember.html` | Renders EN + TR play buttons |
| `5_Symbols/pages/cards.html` | Renders EN + TR play buttons |
| `5_Symbols/js/state.js` | `getUserLanguage()` / `setUserLanguage()` cookie helpers |
| `5_Symbols/css/styles.css` | `.remember-audio-btn-tr` orange TR button style |

---

## Multilingual Audio — Formula

### Rationale

Multilingual learners acquire and retain technical content better when they can switch
between their native language framing and the target language. For Turkish speakers
studying an English-language certification, hearing the question label and structure
in Turkish removes cognitive load, while the English technical content trains the
exact vocabulary they need for the exam.

### Language Detection

Language preference is stored in cookie `user_language` (values: `en` | `tr`, default `en`).

- Set via `setUserLanguage(lang)` in `state.js`
- Read via `getUserLanguage()` in `state.js`
- User sets it in the Pro Exam welcome modal (🇬🇧 / 🇹🇷 picker) or via the `🌐 EN` / `🇹🇷 TR` toggle in `cards.html` and `remember.html`

### Turkish Audio Text Formula

```
"Soru {N}. {question} ... Cevap: {answer}"
```

- `Soru` = "Question" in Turkish
- `Cevap` = "Answer" in Turkish
- Question and answer text remain in English — technical content is exam-language English
- Result: Turkish framing + English content. Natural code-switching for bilingual learners.

### Azure Blob Naming Convention

| Language | Pattern | Example |
|----------|---------|---------|
| English | `AUD-Q{NNN}.mp3` | `AUD-Q042.mp3` |
| Turkish | `AUD-Q{NNN}-TR.mp3` | `AUD-Q042-TR.mp3` |

Both are stored in the `memory-audio` container of `claudecertstore`.

### UI Behaviour

| Language setting | `cards.html` | `remember.html` |
|----------------|--------------|-----------------|
| `en` (default) | Single `🔊 Play` button (blue) | Single `🔊 Play Audio` button (green) |
| `tr` | `🔊 EN` (blue) + `🔊 TR` (orange) side by side | `🔊 EN Audio` (green) + `🔊 TR Audio` (orange) |

### JSON Schema Extension

```json
{
  "id": 1,
  "audioUrl":   "https://claudecertstore.blob.core.windows.net/memory-audio/AUD-Q001.mp3",
  "audioUrlTr": "https://claudecertstore.blob.core.windows.net/memory-audio/AUD-Q001-TR.mp3"
}
```

`data.js` bakes both URLs into every question at load time so no extra API calls are needed.

### Re-running Turkish Audio

```bash
cd 5_Symbols/scripts

# Full regeneration
AZURE_STORAGE_KEY=$(az storage account keys list --account-name claudecertstore --query "[0].value" -o tsv) \
python3 generate_audio_tr.py

# Single question (e.g. Q42)
AZURE_STORAGE_KEY=... python3 generate_audio_tr.py --start-id 42 --end-id 42

# Force overwrite existing blobs
AZURE_STORAGE_KEY=... python3 generate_audio_tr.py --force

# Dry-run (local /tmp only, no upload)
python3 generate_audio_tr.py --dry-run
```

### Extending to More Languages

To add a new language (e.g. Spanish):
1. Copy `generate_audio_tr.py` → `generate_audio_es.py`
2. Change `build_tts_text_tr` to use Spanish labels (`Pregunta {N}. ... Respuesta: ...`)
3. Change blob naming to `AUD-Q{NNN}-ES.mp3`
4. Add `audioUrlEs` to `data.js` bake pattern
5. Add `es` option to the language selector in `state.js`, `cards.html`, `remember.html`, and `pro-exam.html`
| `2_Environment/kokoro.md` | Docker setup and API reference |
