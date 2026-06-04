# Fix Log

Tracks specific bugs, broken links, and targeted fixes applied to the project.

---

## 2026-06-04 — Leftover `claude_certification_exam` links after repo rename

**Reported:** `https://rifaterdemsahin.github.io/claude_certification_exam/5_Symbols/pages/evaluate_certificates.html` still referenced throughout codebase after repo renamed to `ai_certification_prepare`.

**Root cause:** Bulk rename in a previous session missed docs, formula files, and scripts that contained hardcoded GitHub Pages and GitHub repo URLs.

**Files fixed:**

| File | References fixed |
|---|---|
| `README.md` | GitHub Pages link in header |
| `4_Formula/pro_exam_status.md` | 2 GitHub Pages URLs |
| `4_Formula/pro_exam_quick_start.md` | 1 GitHub Pages URL |
| `4_Formula/deploy/README.md` | GitHub repo + Pages URLs in table |
| `4_Formula/deployment_checklist.md` | 4 GitHub Pages URLs |
| `5_Symbols/docs/github-token-permissions.md` | Repository name in backtick reference |
| `5_Symbols/docs/PRO_EXAM_SETUP.md` | 2 GitHub Pages URLs |
| `5_Symbols/scripts/content-worker.js` | HTTP-Referer header URL |
| `5_Symbols/scripts/generate_notes.py` | 2 GitHub repo edit-link templates |
| `7_Testing_Known/sanity_check_review_v1.md` | GitHub repo edit link |
| `1_Real_Unknown/kanban.md` | 1 historical GitHub Pages URL |

**Not fixed (intentional):** All `file:///Users/rifaterdemsahin/projects/claude_certification_exam/...` local paths in `6_Semblance/`, `1_Real_Unknown/`, `3_Simulation/`, and `4_Formula/` — the local directory is still named `claude_certification_exam` so these remain valid on the local machine.

**Verified:** `grep -rn "rifaterdemsahin.github.io/claude_certification_exam\|github.com/rifaterdemsahin/claude_certification_exam"` returns zero results in tracked files after fix.

---
