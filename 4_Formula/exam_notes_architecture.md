# Pro Exam — Where User Data Is Saved

All user data from `5_Symbols/pages/pro-exam.html` is saved across four storage locations.

---

## Quick Reference — Storage Map

| What | Storage | Key / Blob name | Survives reload? | Cross-device? |
|---|---|---|---|---|
| Learner name | Cookie | `pro_exam_learner_name` | ✅ 365 days | ❌ browser only |
| Learner identity | Azure Blob | `self-learner/{slug}.json` | ✅ permanent | ✅ |
| Question notes (all) | localStorage | `exam_notes_{slug}` | ✅ permanent | ❌ browser only |
| Question notes backup | Azure Blob | `exam-notes/{slug}-notes.json` | ✅ permanent | ✅ |
| Exam answers | localStorage | `proExamProgress` | ✅ permanent | ❌ browser only |
| Mastered questions | Cookie | `claude_cert_pro_mastered` | ✅ 30 days | ❌ browser only |
| Image upload versions | localStorage | `proExamImageVersions` | ✅ permanent | ❌ browser only |

`{slug}` = learner name with non-alphanumeric characters replaced by `_`  
e.g. `Jane Smith` → `Jane_Smith`

---

## 1. Learner Name

**Trigger:** User submits the name prompt modal on first visit, or clicks "change".

**Saved to:**
- Cookie `pro_exam_learner_name` (365-day expiry, same-site)
- Azure Blob `self-learner/Jane_Smith.json`

**Cookie purpose:** Identifies the learner on every page load so their notes and image versions are loaded immediately without fetching from Azure.

**Blob schema:**
```json
{
  "name": "Jane Smith",
  "createdAt": "2026-06-02T16:00:00.000Z",
  "lastActive": "2026-06-02T16:00:00.000Z"
}
```

**Code path:**  
`saveLearnerName()` → `setCookie('pro_exam_learner_name', ...)` + `uploadLearnerToAzure()`

---

## 2. Question Notes

**Trigger:** User clicks "💾 Save Note" in the image popup notes panel (right column).

**Saved to:**
1. `localStorage['exam_notes_Jane_Smith']` — entire notes object, JSON stringified
2. Azure Blob `exam-notes/Jane_Smith-notes.json` — same JSON, uploaded on every save

**Primary read:** localStorage (instant, offline-capable). Azure is the backup for cross-device access.

**Blob schema:**
```json
{
  "learnerName": "Jane Smith",
  "lastUpdated": "2026-06-02T16:05:00.000Z",
  "notes": {
    "1":  "Coordinator routes findings to synthesis agent via tool calls.",
    "30": "Minimal footprint = request only needed permissions."
  }
}
```

Keys are question numbers (strings). Values are free-form text typed by the learner.

**Code path:**  
`saveNote(qNum)` → `localStorage.setItem(exam_notes_{slug}, ...)` + `uploadNotesToAzure()`

**Loaded on page start:**  
`initLearner()` reads the cookie, then reads `localStorage['exam_notes_{slug}']` into `examNotes{}`.  
When the image popup opens, `existingNote = examNotes[questionNumber]` pre-fills the textarea.

---

## 3. Image Upload Versions

**Trigger:** User uploads a replacement diagram via the "📎 Change Image" button → paste/drop/file → "☁️ Upload to Azure".

**Saved to:**
- Azure Blob `exam-images/q030.png` — replaces the existing image file
- `localStorage['proExamImageVersions']` — `{"30": 1717340400000, ...}` timestamp map

**Why the timestamp map?**  
Azure replaces the blob at `q030.png` but the URL doesn't change, so the browser serves the old cached version on reload. The timestamp makes the URL unique per upload:

```
before upload:  https://claudecertstore.blob.core.windows.net/exam-images/q030.png
after upload:   https://claudecertstore.blob.core.windows.net/exam-images/q030.png?t=1717340400000
```

The `?t=` param is appended by `getImageUrl(questionNumber)` which checks `imageVersions[qNum]` on every modal open and page load.

**Code path:**  
`uploadImageToAzure(qNum)` → Azure PUT → `setImageVersion(qNum)` → `localStorage['proExamImageVersions']`  
`loadImageVersions()` runs at page startup to restore the map into `imageVersions{}`.

---

## 4. Exam Answers & Mastered State

**Trigger:** User selects an answer option or clicks "🎓 Mastered".

| Data | Storage | Key | Notes |
|---|---|---|---|
| Selected answers | localStorage | `proExamProgress` | `{questionNumber: selectedOption}` |
| Mastered list | Cookie | `claude_cert_pro_mastered` | `[1, 5, 12, ...]` array, 30-day expiry |

These are independent of learner identity — they are not namespaced by name.

---

## Azure Storage Details

**Account:** `claudecertstore`

| Container | Blob pattern | Access | SAS expiry |
|---|---|---|---|
| `exam-notes` | `{slug}-notes.json` | Private, SAS write | 2028-01-01 |
| `self-learner` | `{slug}.json` | Private, SAS write | 2028-01-01 |
| `exam-images` | `q{NNN}.png` | Public read, SAS write | 2028-01-01 |

All three SAS tokens are `rwcl` (read, write, create, list) and embedded in the page JS. CORS on the storage account allows `PUT` from all origins (`*`), enabling direct browser uploads with no backend proxy.

---

## Full Save Flow (one-page summary)

```
FIRST VISIT
  ├─ Name prompt shown
  ├─ Name entered → Cookie: pro_exam_learner_name
  │                → Azure: self-learner/Jane_Smith.json
  └─ examNotes{} = {} (empty)

PAGE LOAD (returning)
  ├─ Cookie read → learnerName = "Jane Smith"
  ├─ localStorage['exam_notes_Jane_Smith'] → examNotes{}
  ├─ localStorage['proExamImageVersions'] → imageVersions{}
  ├─ localStorage['proExamProgress'] → userAnswers{}
  └─ Cookie['claude_cert_pro_mastered'] → masteredQuestions[]

OPEN IMAGE POPUP (question 30)
  ├─ getImageUrl(30) → q030.png?t=1717340400000  (if version exists)
  └─ textarea.value = examNotes[30] || ''

SAVE NOTE
  ├─ examNotes[30] = "my note text"
  ├─ localStorage['exam_notes_Jane_Smith'] = JSON.stringify(examNotes)
  └─ Azure PUT: exam-notes/Jane_Smith-notes.json

UPLOAD IMAGE (question 30)
  ├─ Azure PUT: exam-images/q030.png
  ├─ imageVersions[30] = Date.now()
  └─ localStorage['proExamImageVersions'] = JSON.stringify(imageVersions)
```
