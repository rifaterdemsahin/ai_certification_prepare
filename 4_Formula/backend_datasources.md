# 🗄️ Backend Datasource Containers

This formula document maps and details all backend data source containers used in the project, facilitating feedback and remediation of technical debt.

---

## 📦 Container Registry (Azure Blob Storage)

All dynamic backend content is hosted on Azure Blob Storage under the account `claudecertstore`. The serverless API (`claude-cert-api`) acts as the gatekeeper for writes, deletes, and list operations, while standard public reads fetch from the CDN/Blob endpoints directly.

| Container Name | Content Description | Format | Access Control | Primary API / Access Route |
| :--- | :--- | :--- | :--- | :--- |
| **`memory-cards`** | Flashcards for standard questions | Markdown (`.md`) | Public Read / Auth Write | `/api/cards` |
| **`memory-images`** | Visual mnemonics and diagrams | Images (`.png`, `.jpg`, etc.) | Public Read / Auth Write | `/api/UploadImage` |
| **`exam-images`** | Diagrams for exam practice questions | Images/SVGs | Public Read / Auth Write | Direct Blob URL / CDN |
| **`analyse-pages`** | Competency analysis dashboards | HTML (`.html`) | Public Read / Auth Write | `/api/AnalysePages` |
| **`memory-audio`** | Kokoro TTS audio generated questions | Audio (`.mp3`) | Public Read / Auth Write | Direct Blob URL / CDN |
| **`stories`** | Interactive agent learning stories | JSON | Public Read / Auth Write | `/api/stories` |
| **`story-images`** | User/agent-uploaded story screenshots | Images (`.png`, `.jpg`, etc.) | Public Read (Blob) / Public Write | `/api/StoryImages` or `/api/stories?action=upload-image` |

---

## 🔍 Detailed Datasource Overview

### 1. `memory-cards`
- **Purpose**: Stores detailed study cards corresponding to competency questions.
- **Naming Pattern**: `MEM-Q{ID}.md` (e.g. `MEM-Q101.md`).
- **Integrations**: Integrated with `/api/cards` for listing, fetching, updating, and deleting.
- **Auth**: Token required for POST/DELETE operations.

### 2. `memory-images`
- **Purpose**: Visual diagrams mapping Claude Certification concepts.
- **Naming Pattern**: `MEM-Q{ID}_v1.{extension}`.
- **Integrations**: Used by `UploadImage` function to store static diagrams linked inside memory cards.

### 3. `exam-images`
- **Purpose**: Diagnostic drawings and tables for exam questions.
- **Naming Pattern**: `q{ID}.png` / `q{ID}.svg`.
- **Integrations**: Standard static referencing.

### 4. `analyse-pages`
- **Purpose**: Custom dashboards rendering competency analysis.
- **Naming Pattern**: `{topic_name}.html`.
- **Integrations**: Managed via the `/api/AnalysePages` endpoint.

### 5. `memory-audio`
- **Purpose**: Audio voiceovers for study material, synthesized using the Kokoro TTS engine.
- **Naming Pattern**: `AUD-Q{ID}.mp3`.
- **Integrations**: Directly streamed via audio components in study pages.

### 6. `stories`
- **Purpose**: Graph-based node paths for multi-turn agent execution walkthroughs.
- **Naming Pattern**: `{story-id}.json`.
- **Integrations**: Loaded, listed, and saved using `/api/stories`.

### 7. `story-images`
- **Purpose**: User-generated or agent-generated screenshots for interactive stories.
- **Naming Pattern**: `story-img-{username}-{timestamp}-{rand}.{ext}`.
- **Integrations**: Managed by `/api/StoryImages` and `/api/stories?action=upload-image`.

---

## 🛠️ Identified Technical Debt & Action Items

We have identified the following technical debt across our data sources:

1. **API Redundancy**: 
   - There are two endpoints handling image uploads: `/api/UploadImage` (using authorization keys) and `/api/StoryImages` / `/api/stories?action=upload-image` (which operates without strict authorization validation).
2. **Schema & File Validation**:
   - Lack of server-side content-type validation for files uploaded to `story-images` and `memory-images`.
3. **No Database Index**:
   - We query and list files using `containerClient.listBlobsFlat()` inside `/api/cards` and `/api/AnalysePages`. While convenient for < 1,000 files, flat listings scale poorly (O(N) operations) compared to utilizing a database index or metadata catalog (like Azure Cosmos DB or Table Storage).
4. **CORS Configuration Consistency**:
   - Custom CORS headers are hardcoded (`Access-Control-Allow-Origin: *`) individually in each Azure Function rather than managed centrally via Azure API Management or App Service configuration.
5. **No Version Control on Blob Updates**:
   - Overwriting a card or story does not preserve historical backups in a structured git-like way (though blob-level snapshotting can be enabled on Azure Storage).
