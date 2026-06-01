# Antigravity — Structural Integrity & Deduplication

Antigravity is the agent responsible for keeping the project structurally clean. Its job is to enforce the 7-stage framework, eliminate duplication, and ensure CLAUDE.md remains the single source of truth.

> All project-wide rules (architecture, design tokens, Azure setup, conventions, kanban discipline) live in **CLAUDE.md**. This file handles only what Antigravity specifically owns.

---

## 🗺 7-Stage Self-Learning System

| Stage | Folder | Purpose |
|-------|--------|---------|
| 1 | `1_Real_Unknown` | **The "Why"** — Problem definitions, OKRs, core questions, hypotheses |
| 2 | `2_Environment` | **The "Context"** — Setup guides, Azure, Cloudflare, navigation docs |
| 3 | `3_Simulation` | **The "Vision"** — UI mockups, design vision, UX documentation |
| 4 | `4_Formula` | **The "Recipe"** — Concepts, checklists, pipelines, architecture docs |
| 5 | `5_Symbols` | **The "Reality"** — Source code, pages, data, scripts, Azure API |
| 6 | `6_Semblance` | **The "Scars"** — Error logs, workarounds, gap analysis |
| 7 | `7_Testing_Known` | **The "Proof"** — Validation checklists, test scripts, outcome confirmation |

---

## 🛸 Antigravity-Specific Rules

### Deduplication Enforcement
- Scan all agent files (`agents.md`, `gemini.md`, `copilot.md`, `kilocode.md`, `mimo.md`) for content that duplicates CLAUDE.md. Replace duplicated sections with a pointer: _"See CLAUDE.md for [topic]."_
- Remove duplicate script tags, nav imports, or resource references across HTML files in `5_Symbols/pages/`.
- If two files serve the same purpose, identify the canonical one and remove or stub the other.

### Structural Integrity
- Every new feature page belongs in `5_Symbols/pages/`.
- Every new formula/concept doc belongs in `4_Formula/`.
- Every new error or workaround gets logged in `6_Semblance/error_log.md`.
- Every new test file belongs in `7_Testing_Known/`.
- Never place content at the wrong stage level.

### Agent File Protocol
Agent files at the project root (`agents.md`, `gemini.md`, etc.) are **thin wrappers**, not full copies of CLAUDE.md. Each file should:
1. State the agent's name and its specific role
2. Link to CLAUDE.md: _"Shared rules: see CLAUDE.md"_
3. Add only what is unique to that agent (e.g., Gemini-specific syntax, Copilot prompt style)

### Commit Discipline
- After every command, commit and push — do not batch unrelated changes.
- After every session, update `1_Real_Unknown/kanban.md` (see Kanban Discipline in CLAUDE.md).
- Log every significant prompt in `prompts.md`.

### `index.html` Integrity
- `index.html` stays at the repo root — GitHub Pages requires it there.
- It is the app dashboard, not a feature page. Feature pages live in `5_Symbols/pages/`.
- Keep `index.html` lightweight: no inline feature logic; delegate to shared JS in `5_Symbols/js/`.

---

## 🔁 Maintenance Checklist

For the full per-stage checklist, see **CLAUDE.md → Maintenance Checklist**.

Antigravity-specific checks:
- [ ] No design tokens, architecture rules, or Azure config duplicated outside CLAUDE.md
- [ ] No orphaned `<script src="nav.js">` tags in `5_Symbols/pages/` HTML files
- [ ] All agent files are thin wrappers, not full copies
- [ ] `1_Real_Unknown/kanban.md` Done section is current with `git log --oneline`
- [ ] `prompts.md` has an entry for the current session
- [ ] No committed binaries, images, or audio — Azure Blob Storage only
