# Exam Notes & Learner Identity Architecture

## Overview

The Pro Exam page (`5_Symbols/pages/pro-exam.html`) supports personal study notes attached to each question. Notes are persisted in two layers — local and cloud — and are scoped to a named learner identity.

---

## Learner Identity

### How it works
On first visit, a modal prompts for the learner's name. The name is stored as a browser cookie and used as a namespace for all data.

| Storage | Key | Expiry |
|---|---|---|
| Cookie | `pro_exam_learner_name` | 365 days |
| Azure Blob | `self-learner/{slug}.json` | Permanent |

`{slug}` = name with all non-alphanumeric characters replaced by `_`.

### Blob schema — `self-learner/{slug}.json`
```json
{
  "name": "Jane Smith",
  "createdAt": "2026-06-02T16:00:00.000Z",
  "lastActive": "2026-06-02T16:00:00.000Z"
}
```

The blob is uploaded (PUT) when the learner first enters their name. It is overwritten on subsequent visits if the user changes their name.

---

## Exam Notes

### How it works
When a question's image popup is opened, a notes textarea appears on the right. The Save button writes the note to two places:

1. **`localStorage`** — keyed as `exam_notes_{slug}`, read back on page load
2. **Azure Blob Storage** — `exam-notes/{slug}-notes.json`, entire notes object uploaded on each save

Notes are loaded from `localStorage` on page load (fast, offline-capable). Azure is the backup / cross-device persistence layer.

### Blob schema — `exam-notes/{slug}-notes.json`
```json
{
  "learnerName": "Jane Smith",
  "lastUpdated": "2026-06-02T16:05:00.000Z",
  "notes": {
    "1": "Orchestrator delegates subtasks to subagents via tool calls.",
    "12": "Prompt caching threshold is 1024 tokens for Sonnet."
  }
}
```

Keys in `notes` are question numbers (strings). Values are free-form text.

---

## Azure Storage

### Account
`claudecertstore` (Azure Blob Storage)

### Containers

| Container | Purpose | Public access |
|---|---|---|
| `exam-notes` | One JSON per learner — all their question notes | Private (SAS only) |
| `self-learner` | One JSON per learner — identity/timestamp | Private (SAS only) |

### Authentication
Both containers use a **container-level SAS token** embedded in the page JS. The tokens have `rwcl` permissions (read, write, create, list) and expire 2028-01-01. This lets the browser PUT blobs directly without a backend proxy.

> **Security note:** The SAS tokens are visible in the page source. This is acceptable for a study app — there is no sensitive data and the worst case is a user overwrites their own notes blob. Rotate the tokens if abuse is detected.

### Direct upload (REST)
```
PUT https://claudecertstore.blob.core.windows.net/{container}/{blob}?{SAS}
x-ms-blob-type: BlockBlob
Content-Type: application/json

{...json body...}
```

CORS on the storage account allows all origins (`*`) with PUT/GET/OPTIONS so browser uploads work without a proxy.

---

## Data Flow

```
User types name
  → cookie: pro_exam_learner_name
  → Azure PUT: self-learner/{slug}.json

Page loads
  → read cookie → learnerName
  → read localStorage: exam_notes_{slug} → examNotes{}
  → show learner badge in header

User opens image popup (any question)
  → modal opens two-column layout
    left:  question text + diagram image
    right: notes textarea (pre-filled from examNotes)

User clicks Save Note
  → examNotes[questionNumber] = textarea.value
  → localStorage.setItem(exam_notes_{slug}, JSON.stringify(examNotes))
  → Azure PUT: exam-notes/{slug}-notes.json
  → status indicator shows "✓ Saved" for 2 seconds

User clicks "change" badge
  → learnerNameModal re-opens with current name pre-filled
  → on confirm: cookie updated, badge updated, new localStorage key used
```

---

## UI Components

### Learner badge (header)
A purple pill in the page header showing `👤 {name}` with a `change` link. Hidden until `initLearner()` resolves a name. Rendered by `updateLearnerBadge()`.

### Learner name modal
A centered overlay (`z-index: 3000`) that blocks interaction until a name is entered. Triggered on first visit and from the "change" link.

### Notes panel (image modal right column)
- `notes-q{N}` — textarea ID, value set via `.value` (not innerHTML) to prevent injection
- `notes-status-{N}` — status span, shows "✓ Saved" briefly after save
- Grid collapses to single column on screens ≤ 768px

---

## JS Functions Reference

| Function | Purpose |
|---|---|
| `initLearner()` | Reads cookie, loads localStorage notes, shows name modal if no name |
| `saveLearnerName()` | Saves name to cookie, calls badge update + Azure upload |
| `updateLearnerBadge()` | Updates the header badge DOM with current `learnerName` |
| `changeLearner()` | Re-opens the name modal pre-filled with current name |
| `saveNote(qNum)` | Writes note to `examNotes`, localStorage, Azure |
| `uploadLearnerToAzure()` | PUT `self-learner/{slug}.json` via SAS |
| `uploadNotesToAzure()` | PUT `exam-notes/{slug}-notes.json` via SAS |
