# Claude Code Project Guidelines

> **Single Source of Truth.** All other agent files (`agents.md`, `gemini.md`, `copilot.md`, `kilocode.md`, `mimo.md`, `antigravity.md`) defer to this file for shared rules. They may add agent-specific notes but must not duplicate content defined here.

## Project Overview

**Claude Developer Certification - Study Mastery App**

Interactive study guide for the Claude Developer Certification exam featuring 124 questions, visual hints, memory aids, and progress tracking.

## Core Architecture

- **Single-File Entry:** `index.html` at the repo root is the GitHub Pages entry point and app dashboard.
- **No Build Step:** Use CDNs for React, Mermaid, and other libraries. Never introduce npm, webpack, or vite.
- **Modular Pages:** Feature pages live in `5_Symbols/pages/` and share `5_Symbols/js/nav.js` for navigation.
- **State Management:** Browser cookies for progress tracking; `5_Symbols/js/state.js` manages shared state.
- **Vanilla CSS:** All styling in `5_Symbols/css/styles.css` and inline `<style>` tags.
- **Hosting:** Static site deployed to GitHub Pages; backend via Azure Functions.

## Design Tokens

```css
--bg-primary: #0f172a
--bg-secondary: #1e293b
--bg-card: #1e293b
--border: #334155
--text-primary: #e2e8f0
--text-secondary: #94a3b8
--accent-blue: #38bdf8
--accent-purple: #a855f7
--accent-green: #10b981
--accent-yellow: #fbbf24
--accent-red: #ef4444
--accent-orange: #f59e0b
```

## Content Structure

### Competencies (5 Core Areas)
1. **CAT01:** Agentic Architecture & Orchestration (27%)
2. **CAT02:** Tool Design & MCP Integration (18%)
3. **CAT03:** Claude Code Configuration & Workflows (20%)
4. **CAT04:** Prompt Engineering & Structured Output (20%)
5. **CAT05:** Context Management & Reliability (15%)

### Question IDs
Pattern: `CAT{NN}-Q{NNN}` (e.g., `CAT01-Q005`)

### Navigation Structure (Bloom's Taxonomy)
Pages are grouped by Bloom's level in `5_Symbols/data/menu.json` (hosted on Azure):
- **Remember** — flashcards, slideshow, mastery, quiz, memory cards
- **Understand** — discussion board
- **Analyse** — stats, concepts, video resources, analyse renderer
- **Evaluate** — pricing, multiplayer, certificates
- **Create** — story writer, creator, tactics, admin tools

## Directory Layout

```
├── index.html                      # App dashboard (GitHub Pages root)
├── CLAUDE.md                       # This file — single source of truth
├── agents.md                       # Multi-agent gateway (points to CLAUDE.md)
├── antigravity.md                  # Structural integrity & deduplication rules
├── gemini.md                       # Gemini CLI notes (points to CLAUDE.md)
├── copilot.md                      # GitHub Copilot notes
├── kilocode.md                     # Kilo Code notes
├── mimo.md                         # Mimo notes
├── prompts.md                      # Prompt log & PM framework
├── README.md                       # Human-facing project overview
├── robots.txt
├── sitemap.xml
├── 1_Real_Unknown/                 # Stage 1 — The "Why"
│   ├── kanban.md                   # Sprint board (update after every session)
│   ├── problem_statement.md
│   ├── okrs.md
│   ├── questions.md
│   ├── hypotheses.md
│   └── costs.md
├── 2_Environment/                  # Stage 2 — The "Context"
│   ├── azure.md                    # Azure storage, containers, deployment
│   ├── bookmarks.md                # Official study resources
│   ├── cloudflare_workers.md       # Vote & content Cloudflare Workers
│   ├── fly_io.md                   # Backend hosting guide
│   ├── github_pages.md             # Frontend static hosting guide
│   ├── kokoro.md                   # Kokoro TTS Docker setup & API ref
│   ├── kokoro_tts.md               # TTS audio pipeline details
│   └── navigation.md               # Navigation component docs
├── 3_Simulation/                   # Stage 3 — The "Vision"
│   └── user_experience.md          # UX mockups and documentation
├── 4_Formula/                      # Stage 4 — The "Recipe"
│   ├── backend_datasources.md      # Azure container registry & tech debt
│   ├── backup_system_data.md       # Backup strategy
│   ├── kokoro_audio_pipeline.md    # End-to-end TTS pipeline formula
│   ├── questions_json_schema.md    # questions.json schema & field reference
│   ├── story_json_architecture.md  # Story JSON graph architecture
│   ├── DEPLOYMENT_CHECKLIST.md
│   ├── INDEX_STRUCTURE.md
│   ├── PRO_EXAM_QUICK_START.md
│   └── PRO_EXAM_STATUS.md
├── 5_Symbols/                      # Stage 5 — The "Reality"
│   ├── css/
│   │   └── styles.css              # Shared stylesheet
│   ├── data/
│   │   ├── exam.json               # Core 124-question dataset (local source)
│   │   ├── questions.json          # Azure-hosted question data (fetched by data_loader.js)
│   │   ├── pro-exam.json           # Pro exam question dataset
│   │   ├── menu.json               # Navigation menu (Azure-hosted, fetched by nav.js)
│   │   └── search_index.json       # Full-text search index
│   ├── js/
│   │   ├── data.js                 # Static question data fallback
│   │   ├── data_loader.js          # Fetches questions.json from Azure; falls back to data.js
│   │   ├── nav.js                  # Shared navigation; loads menu.json from Azure
│   │   ├── state.js                # Shared state management
│   │   └── utils.js                # Shared utilities
│   ├── pages/                      # Feature pages
│   │   ├── remember.html           # Bloom's — Remember (flashcard slideshow)
│   │   ├── cards.html              # Memory card grid with audio/mastered
│   │   ├── memory_cards.html       # Memory cards index (loads from Azure API)
│   │   ├── mastery.html            # Mastery progress tracker
│   │   ├── quiz.html               # Quiz mode
│   │   ├── understand.html         # Discussion board (cherry-pick)
│   │   ├── analyse.html            # Stats and analysis
│   │   ├── analyse_renderer.html   # Dynamic Azure-hosted analysis pages
│   │   ├── exam.html               # Practice exam
│   │   ├── pro-exam.html           # Pro exam with image reveals & audio
│   │   ├── practice_exam.html      # Full exam source practice
│   │   ├── story.html              # Visual story writer (graph-based)
│   │   ├── multiplayer.html        # MQTT multiplayer exam game
│   │   ├── markdown_renderer.html  # Renders Azure-hosted markdown files
│   │   ├── add_memory_card.html    # Admin: create memory cards
│   │   ├── quick_memory.html       # Admin: quick memory card entry
│   │   ├── tactics.html            # Exam tactics & study strategies
│   │   ├── blooms_architecture.html
│   │   ├── claude_pricing.html
│   │   ├── create.html
│   │   ├── creator.html
│   │   ├── evaluate_certificates.html
│   │   ├── incorrect_summary.html
│   │   ├── mcp-before-after.html
│   │   ├── multi_media_learning.html
│   │   └── bmad.html               # BMAD page (served from Azure analyse-pages)
│   ├── azure-api/                  # Azure Functions backend
│   │   ├── host.json
│   │   └── package.json
│   ├── docs/                       # Technical deployment docs
│   │   ├── azure-content-architecture.md
│   │   ├── azure-function-deployment.md
│   │   └── github-pages-security-architecture.md
│   └── scripts/                    # Automation scripts
│       ├── backup_data.py          # Azure blob backup utility
│       ├── generate_audio.py       # Kokoro TTS audio generator
│       ├── generate_questions_json.js
│       └── content-worker.js       # Cloudflare Worker source
├── 6_Semblance/                    # Stage 6 — The "Scars"
│   └── error_log.md
└── 7_Testing_Known/                # Stage 7 — The "Proof"
    ├── test_links.js
    ├── test_logic.js
    ├── test_analyse_pages.js
    ├── test_content_worker.js
    └── test_vote_worker.js
```

## Code Editing Rules

### When modifying `index.html` or any page
- Use **surgical edits** with targeted replacements
- Never rewrite large sections without explicit approval
- Preserve existing component structure and naming conventions
- Follow existing `questionsData` / `categories` patterns in data files

### JavaScript Conventions
- Use descriptive function names: `renderSomething`, `handleSomething`
- Keep functions focused and single-purpose
- Shared logic goes in `5_Symbols/js/`; page-specific logic stays inline

### CSS Conventions
- Maintain dark theme consistency using the design tokens above
- Ensure responsive design (mobile, tablet, desktop)
- Shared styles in `5_Symbols/css/styles.css`; page-specific overrides inline

## Data Loading Pattern

Pages load question data via `data_loader.js`, which fetches `questions.json` from Azure and falls back to `data.js` on failure. The `dataReady` promise guards all rendering:

```js
dataReady.then(questions => { /* render */ });
```

Navigation is loaded from the Azure-hosted `menu.json` by `nav.js`. To add or update nav items, edit and re-upload `5_Symbols/data/menu.json` to the `$web` or served container.

## Content Guidelines

- **Visuals:** Use SVG graphics and emojis for hints and mnemonics
- **Memory Cards:** Stored in Azure Blob Storage (`memory-cards` container), rendered via `markdown_renderer.html`
  - URL pattern: `markdown_renderer.html?url=https://claudecertstore.blob.core.windows.net/memory-cards/MEM-Q{ID}.md&title=Memory Card {ID}`
- **Exam Images:** `exam-images` container — `q{NNN}.png` or `q{NNN}.svg`
- **Audio:** `memory-audio` container — `AUD-Q{ID}.mp3` (generated by Kokoro TTS pipeline)

## Testing & Verification

- Run `npm test` in `7_Testing_Known/` to execute all link and logic checks
- `test_links.js` — verifies GitHub Pages + Azure blob URLs
- `test_logic.js` — verifies nav/data structure
- Always verify Mermaid chart syntax before committing
- Test responsive design across breakpoints

## Libraries (CDN)

- React 18
- Mermaid (for diagrams)
- No npm dependencies in the frontend

## Common Tasks

### Adding a New Question
1. Add to `questionsData` in `5_Symbols/data/exam.json` (and regenerate `questions.json` via `generate_questions_json.js`)
2. Follow the `CAT{NN}-Q{NNN}` ID pattern
3. Include visual hint (SVG/emoji)
4. Add memory card if applicable

### Creating Memory Cards
1. Use `5_Symbols/pages/quick_memory.html` or `5_Symbols/pages/add_memory_card.html`
2. Cards are stored in Azure Blob Storage `memory-cards` container (no GitHub deployment triggered)
3. Naming pattern: `MEM-Q{ID}.md`

### Uploading Analyse Pages
1. Create or edit the HTML file locally
2. Upload to `analyse-pages` container
3. It will be served via `analyse_renderer.html?page={name}`

## Nav Behaviour

- **Dropdowns:** Open on hover (desktop) and on click (adds `.click-open` class via JS). Click outside closes all.
- **Blooms Guide:** Collapsed by default. Cookie `learning_loop_open` persists user preference.
- **Debug Console:** When `debug` cookie is `'true'`, logs page path, sessionStorage keys, and cookies via `console.group`.
- **Video Resources:** External YouTube links live under `📹 Video Resources` in the Analyse section of `menu.json`.
- **Admin Group:** `quick_memory.html`, `add_memory_card.html`, and `analyse_renderer.html?action=new` are under `⚙️ Admin` in the Create menu.

## Kanban Discipline

After every session:
1. Run `git log --oneline` and compare every commit against `1_Real_Unknown/kanban.md` Done section.
2. Add any missing commits as `- [x] <description> (\`<hash>\`)` — newest at the top of Done.
3. Commit and push the kanban update.

## Maintenance Checklist

Run these checks regularly to keep the project healthy:

- [ ] Update stage 1 — `1_Real_Unknown` (problem statements, OKRs, open questions, hypotheses)
- [ ] Update stage 2 — `2_Environment` (setup guides, azure, cloudflare, navigation docs)
- [ ] Add new features as visuals — `3_Simulation` (UI mockups, design vision, UX documentation)
- [ ] Document new approaches — `4_Formula` (concepts, exam questions, checklists, research notes)
- [ ] Update implementation & pay tech debt — `5_Symbols` (source code, assets, scripts, data, pages)
- [ ] Log new errors — `6_Semblance` (error logs, workarounds, gap analysis)
- [ ] Update tests — `7_Testing_Known` (validation checklists, test scripts, outcome confirmation)

## Azure Asset Management

### Storage Account
- **Account:** `claudecertstore` (Azure Storage)
- **Key retrieval:** `az storage account keys list --account-name claudecertstore --query "[0].value" -o tsv`

### Azure Container Map

| Container | Purpose | Naming Pattern | Access |
|---|---|---|---|
| `memory-cards` | Flashcard markdown files | `MEM-Q{ID}.md` | Public read / Auth write |
| `memory-images` | Visual mnemonics for cards | `MEM-Q{ID}_v1.{ext}` | Public read / Auth write |
| `memory-audio` | Kokoro TTS audio (MP3) | `AUD-Q{ID}.mp3` | Public read / Direct URL |
| `exam-images` | Pro exam question diagrams | `q{NNN}.png` / `q{NNN}.svg` | Public read / Direct URL |
| `analyse-pages` | Dynamic analysis HTML pages | `{topic}.html` | Public read / Auth write |
| `stories` | Story writer graph JSON | `{story-id}.json` | Public read / Auth write |
| `story-images` | Story screenshot uploads | `story-img-{user}-{ts}.{ext}` | Public read / Public write |

### Uploading Files to Azure Blob Storage

```bash
STORAGE_KEY=$(az storage account keys list --account-name claudecertstore --query "[0].value" -o tsv)
az storage blob upload \
  --account-name claudecertstore \
  --account-key "$STORAGE_KEY" \
  --container-name <container-name> \
  --name <blob-name> \
  --file <local-file-path> \
  --content-type "text/html" \
  --overwrite
```

### Binary & Large File Convention

**Never embed binaries or large data in git.** Use Azure Blob Storage and reference by URL:
- Don't commit image files, audio files, or large JSON blobs to git
- Upload to Azure Blob Storage and reference the public URL
- In JSON: `"imageUrl": "https://claudecertstore.blob.core.windows.net/memory-images/IMG-Q001.png"`
- In HTML: `<img src="https://claudecertstore.blob.core.windows.net/...">` directly

### Backups

Local backup snapshots (under `5_Symbols/data/backups/`) are **gitignored** — local working copies only. Source of truth for Azure-hosted content is Azure Blob Storage, not git. See `4_Formula/backup_system_data.md` for the backup runbook.

### Cloudflare Workers

Two Workers handle edge-side logic (not auto-deployed from git — must update via Cloudflare dashboard):
- **Content Worker** (`5_Symbols/scripts/content-worker.js`) — serves and caches Azure blob content
- **Vote Worker** — handles upvote/downvote for discussion board

See `2_Environment/cloudflare_workers.md` for deployment steps.

## Don'ts

- Don't introduce build tools (npm, webpack, vite)
- Don't use CSS preprocessors (Sass, Less)
- Don't add external dependencies without CDN approval
- Don't break the single-file architecture of `index.html`
- Don't modify cookie structure without a migration plan
- Don't commit binary files, images, audio, or local backup snapshots to git — use Azure Blob Storage
- Don't duplicate rules from this file in other agent files (`agents.md`, `gemini.md`, etc.)
