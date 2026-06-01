# Questions JSON Schema

Where the memory card data lives and how the question records are structured.

---

## Data Files

| File | Questions | ID Range | Purpose |
|------|-----------|----------|---------|
| `5_Symbols/data/questions.json` | 102 | 1 – 124+ | Main study flashcard bank |
| `5_Symbols/data/pro-exam.json` | 57 | 1 – 58 (`question_number` / `id`) | Scenario-based pro exam |
| `5_Symbols/data/exam.json` | 40 | 1 – 40 | Practice exam (multiple-choice source) |

---

## questions.json — Top-Level Structure

```json
{
  "version": "1.0.0",
  "updatedAt": "2026-06-01T...",
  "questions": [ ...array of question objects... ],
  "categories": [ ...array of category objects... ],
  "questionHints": { ...hint map... }
}
```

---

## Question Object Schema

```json
{
  "id": 101,
  "category": 1,
  "question": "What is SWE-bench and how is it used to evaluate AI coding agents?",
  "answer": "SWE-bench is a benchmark of real GitHub issues...",
  "concepts": ["agentic-architecture", "benchmarking"],
  "uid": "CAT01-Q101",
  "youtubeShortUrl": "",
  "audioUrl":       "https://claudecertstore.blob.core.windows.net/memory-audio/AUD-Q101.mp3",
  "imageUrl":       "https://claudecertstore.blob.core.windows.net/memory-images/MEM-Q101_v1.png",
  "azureImageUrl":  "https://claudecertstore.blob.core.windows.net/memory-images/MEM-Q101_v1.png",
  "notesUrl":       "https://claudecertstore.blob.core.windows.net/memory-cards/MEM-Q101.md",
  "googleImageUrl": "https://www.google.com/search?tbm=isch&q=...",
  "relatedVideoUrl":"https://www.youtube.com/results?search_query=...",
  "claudePrompt":   "As a Claude Developer Certification teaching assistant, explain..."
}
```

### Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `id` | number | Unique question ID (sequential) |
| `category` | number | 1–5 matching competency area |
| `question` | string | Descriptive title — NOT "What is '[]' ?" pattern |
| `answer` | string | Short, exam-ready answer |
| `concepts` | string[] | Tag slugs (kebab-case) for filtering |
| `uid` | string | `CAT0{N}-Q{NNN}` — used in blob path keys |
| `youtubeShortUrl` | string | Direct YouTube Short URL (optional) |
| `audioUrl` | string | Azure blob: spoken audio |
| `imageUrl` | string | Azure blob: memory card illustration |
| `azureImageUrl` | string | Same as `imageUrl` (legacy alias) |
| `notesUrl` | string | Azure blob: full markdown memory card |
| `googleImageUrl` | string | Google image search deep-link |
| `relatedVideoUrl` | string | YouTube search deep-link |
| `claudePrompt` | string | Pre-built prompt for "Explain this" button |

---

## Azure Blob Storage — Memory Card Assets

Storage account: **`claudecertstore`**

| Container | Path pattern | Asset type |
|-----------|-------------|------------|
| `memory-cards` | `MEM-Q{NNN}.md` | Markdown memory card text |
| `memory-images` | `MEM-Q{NNN}_v1.png` | Memory card illustration |
| `memory-audio` | `AUD-Q{NNN}.mp3` | Spoken audio for the card |

Base URL: `https://claudecertstore.blob.core.windows.net/`

### URL templates (for new questions)

```
audioUrl   → https://claudecertstore.blob.core.windows.net/memory-audio/AUD-Q{NNN}.mp3
imageUrl   → https://claudecertstore.blob.core.windows.net/memory-images/MEM-Q{NNN}_v1.png
notesUrl   → https://claudecertstore.blob.core.windows.net/memory-cards/MEM-Q{NNN}.md
```

---

## UID ↔ Category Mapping

| UID prefix | category # | Competency |
|------------|-----------|------------|
| `CAT01` | 1 | Agentic Architecture & Orchestration (27%) |
| `CAT02` | 2 | Tool Design & MCP Integration (18%) |
| `CAT03` | 3 | Claude Code Configuration & Workflows (20%) |
| `CAT04` | 4 | Prompt Engineering & Structured Output (20%) |
| `CAT05` | 5 | Context Management & Reliability (15%) |

---

## pro-exam.json — Question Object Schema

```json
{
  "id": 1,
  "question_number": 1,
  "scenario": "Multi-Agent Research System",
  "question": "...",
  "options": { "A": "...", "B": "...", "C": "...", "D": "..." },
  "answer": "A",
  "answer_rationale": "...",
  "image_prompt": "...",
  "audioUrl": "https://claudecertstore.blob.core.windows.net/memory-audio/AUD-PRO-Q001.mp3"
}
```

`id` equals `question_number` (1–58). Pro-exam questions are a separate dataset from `questions.json`.

---

## Title Convention

Question titles must be descriptive and exam-quality. The generic **"What is '[]'?"** pattern is discouraged for new entries — use a full, clear question that conveys the concept's context:

| Bad | Good |
|-----|------|
| `What is 'SWE Bench'?` | `What is SWE-bench and how is it used to evaluate AI coding agents?` |
| `What is 'function calling'?` | `What is 'function calling' capability in Claude's API and how does it enable tool use?` |
