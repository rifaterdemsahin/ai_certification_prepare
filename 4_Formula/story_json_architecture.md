# Story JSON Architecture

How the Visual Story Writer stores, syncs, and displays user study stories.

---

## Where the Story JSON Lives

```
Browser (localStorage)
        │
        │  auto-save every 45s + manual Save
        ▼
Azure Blob Storage
  container: stories
  filename:  story_{username}.json
  example:   story_rifat_erdem_sahin.json
  public URL: https://claudecertstore.blob.core.windows.net/stories/story_rifat_erdem_sahin.json
```

Two copies always exist — one local (fast, offline-capable), one in Azure (durable, cross-device).

---

## Story JSON Structure

```json
{
  "username": "Rifat Erdem Sahin",
  "nodes": [ ...array of node objects... ]
}
```

### Node Types

| type         | what it is                        | key fields                        |
|--------------|-----------------------------------|-----------------------------------|
| `concept`    | A core study concept (Analyse)    | `refId`, `title`, `referenceText` |
| `question`   | An exam question (Remember)       | `refId`, `checked`                |
| `memory-card`| A memory card (Understand)        | `qNum`, `referenceText`           |
| `transition` | Connective narrative between nodes| `notes`, `image` (blob URL)       |
| `custom`     | Free-form personal objective      | `title`, `notes`                  |

### Full Node Example

```json
{
  "id": "node-1780337108535-l85db6nji",
  "type": "transition",
  "title": "Connective Transition",
  "notes": "Write the connective narrative that bridges your story here...",
  "color": "orange",
  "image": "https://claudecertstore.blob.core.windows.net/story-images/story-img-rifat_erdem_sahin-1780337113812-utraro7d.png"
}
```

---

## Image Storage Rule

**Images are NEVER stored as base64 in the JSON.**  
Only Azure Blob URL references are allowed in `node.image`.

```
User pastes image (Ctrl+V)
        │
        ▼
POST api/stories?action=upload-image
  { imageData: "data:image/png;base64,...", contentType, username }
        │
        ▼
Azure Function (Stories/index.js)
  → uploads bytes to container: story-images
  → filename: story-img-{user}-{timestamp}-{8rand}.{ext}
  → returns { url: "https://claudecertstore.blob.core.windows.net/story-images/..." }
        │
        ▼
node.image = returned blob URL   ← stored in JSON, never base64
```

### Image filename format
```
story-img-rifat_erdem_sahin-1780337113812-utraro7d.png
           └── username ──┘  └── ms ts ─┘ └─ rand ─┘
```

---

## Save Flow

```
User clicks 💾 Save  (or 45s auto-save fires)
        │
        ├─1─▶ persistStory()  →  localStorage  (instant, offline)
        │         └── safety strip: removes any data: URL before writing
        │
        └─2─▶ POST api/stories  (storyData JSON)
                  │
                  ▼
              Stories/index.js POST handler
                  │
                  ├── if node.image starts with data:
                  │       → upload to story-images container
                  │       → replace with blob URL
                  │
                  └── write clean JSON to stories container
                          story_{username}.json
                  │
                  ▼
              returns { ok, nodes }  ← nodes now have blob URLs
                  │
                  ▼
              client syncs storyData.nodes with returned nodes
              persistStory() again  ← localStorage also updated with blob URLs
```

---

## Azure Blob Containers

| Container     | Contents                        | Access  | Example path                                   |
|---------------|---------------------------------|---------|------------------------------------------------|
| `stories`     | Story JSON files (one per user) | Private | `story_rifat_erdem_sahin.json`                 |
| `story-images`| Transition node images          | Public  | `story-img-rifat_erdem_sahin-{ts}-{rand}.png`  |
| `memory-cards`| Study memory card markdown      | Public  | `MEM-Q001.md`                                  |
| `memory-images`| Memory card artwork            | Public  | `MEM-Q001_v1.png`                              |

Storage account: `claudecertstore`  
Function App: `claude-cert-api.azurewebsites.net`

---

## Deployment Note

The `Stories` Azure Function handles **both** story saves and image uploads.  
It must be manually redeployed via the Azure Portal after code changes:

> Portal → Function App `claude-cert-api` → Functions → `Stories` → Code + Test → Save

See `6_Semblance/error_log.md` — [2026-06-01] entry for the full incident history.
