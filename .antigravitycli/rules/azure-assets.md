# Azure Asset Management & Data Handling

## Azure Container Map
| Container | Purpose | Naming Pattern | Access |
|---|---|---|---|
| `memory-cards` | Flashcard markdown files | `MEM-Q{ID}.md` | Public read / Auth write |
| `memory-images` | Visual mnemonics for cards | `MEM-Q{ID}_v1.{ext}` | Public read / Auth write |
| `memory-audio` | Kokoro TTS audio (MP3) | `AUD-Q{ID}.mp3` | Public read / Direct URL |
| `exam-images` | Pro exam question diagrams | `q{NNN}.png` / `q{NNN}.svg` | Public read / Direct URL |
| `analyse-pages` | Dynamic analysis HTML pages | `{topic}.html` | Public read / Auth write |
| `stories` | Story writer graph JSON | `{story-id}.json` | Public read / Auth write |
| `story-images` | Story screenshot uploads | `story-img-{user}-{ts}.{ext}` | Public read / Public write |

## Data Loading Pattern
- Pages fetch question data via `5_Symbols/js/data_loader.js`, which loads `questions.json` from Azure and falls back to local `data.js`.
- The `dataReady` promise guards all rendering operations:
  ```js
  dataReady.then(questions => { /* render */ });
  ```

## Binary and Large File Convention
- **No Binaries in Git**: Never commit images, audio files, or large data sets to the git repository.
- Upload large files and assets directly to the `claudecertstore` Azure Blob Storage account, and reference them via public URLs.

## Edge Services
- **Cloudflare Workers**: Two edge workers handle custom dynamic behavior:
  - **Content Worker** (`5_Symbols/scripts/content-worker.js`): Serves and caches Azure blob content.
  - **Vote Worker**: Handles discussion board upvote/downvote operations.
