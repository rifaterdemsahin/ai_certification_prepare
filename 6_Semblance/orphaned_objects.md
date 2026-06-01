# 🔍 Orphaned and Unused Objects Report

This document records the orphaned, unreferenced, and unused files and scripts in the project. These files represent technical debt, redundant logic, or obsolete assets that are not linked or referenced by any other file in the workspace.

---

## Summary of Orphaned Objects

A codebase-wide search was conducted for incoming references (using filename and relative path matching). The following files have **0 active references** in the project:

### 🎨 1. Simulation & UI Assets
* **[story_creation_to_merge_all_stages.png](file:///Users/rifaterdemsahin/projects/claude_certification_exam/3_Simulation/story_creation_to_merge_all_stages.png)**
  * *Purpose:* Visually documenting story canvas creation mockup, but currently unlinked from any documentation.

### 📋 2. Formula & Deployment Guides
* **[dynamic-analysis-pages.md](file:///Users/rifaterdemsahin/projects/claude_certification_exam/4_Formula/deploy/dynamic-analysis-pages.md)**
  * *Purpose:* Deployment instruction or notes for dynamic analysis pages.
* **[multiplayer_report.md](file:///Users/rifaterdemsahin/projects/claude_certification_exam/4_Formula/game/multiplayer_report.md)**
  * *Purpose:* Notes or results of multiplayer testing/design.

### 📄 3. Project Documentation
* **[azure-deployment-collaboration-report.md](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/docs/azure-deployment-collaboration-report.md)**
  * *Purpose:* Legacy deployment collaboration report.
* **[azure-migration-report.md](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/docs/azure-migration-report.md)**
  * *Purpose:* Report on the migration to Azure.
* **[github-token-permissions.md](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/docs/github-token-permissions.md)**
  * *Purpose:* GitHub Actions / CLI token permission documentation.
* **[vote-worker-setup.md](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/docs/vote-worker-setup.md)**
  * *Purpose:* Documentation for voting worker environment setup.

### ⚙️ 4. Scripts (Redundant & Duplicated)
* **[generate-and-upload-pro-exam-images-final.js](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/scripts/generate-and-upload-pro-exam-images-final.js)**
* **[generate-and-upload-pro-exam-images.js](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/scripts/generate-and-upload-pro-exam-images.js)**
* **[generate-pro-exam-diagrams.js](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/scripts/generate-pro-exam-diagrams.js)**
* **[generate_notes.py](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/scripts/generate_notes.py)**
* **[generate_pro_audio.py](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/scripts/generate_pro_audio.py)**
* **[migrate_analysis_pages.js](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/scripts/migrate_analysis_pages.js)**
* **[remove_script_duplicates.py](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/scripts/remove_script_duplicates.py)**
* **[update_agent_references.py](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/scripts/update_agent_references.py)**
* **[update_edit_links.py](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/scripts/update_edit_links.py)**
* **[upload_grok_claude_comparison_to_azure.py](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/scripts/upload_grok_claude_comparison_to_azure.py)**
  * *Notes:* These scripts were created for migration, initial resource generation, or duplicate removal. They are no longer part of active build pipelines or workflows.

### 💾 5. Data & Backups
* **[backup_20260601_192319.zip](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/data/backups/backup_20260601_192319.zip)**
* **[backup_20260601_193129.zip](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/data/backups/backup_20260601_193129.zip)**
* **[backup_20260601_193213.zip](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/data/backups/backup_20260601_193213.zip)**
  * *Purpose:* Local ZIP backups.
* **[fixing_infinitecanvas_to_vertical_canvas_with_personal_stories.png](file:///Users/rifaterdemsahin/projects/claude_certification_exam/6_Semblance/fixing_infinitecanvas_to_vertical_canvas_with_personal_stories.png)**
  * *Purpose:* Local diagram for design reference.
* **[problematic_json_story_rifat_erdem_sahin (2).json](file:///Users/rifaterdemsahin/projects/claude_certification_exam/6_Semblance/problematic_json_story_rifat_erdem_sahin (2).json)**
  * *Purpose:* Diagnostics JSON dump.

### 🧪 6. Package Managers & Dependency Lockfiles
* **[5_Symbols/azure-api/package-lock.json](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/azure-api/package-lock.json)**
* **[7_Testing_Known/package-lock.json](file:///Users/rifaterdemsahin/projects/claude_certification_exam/7_Testing_Known/package-lock.json)**
  * *Notes:* Standard auto-generated lock files (uncallable and unreferenced in code, but standard).

---

## Recommendations

1. **Scripts:** Consider archiving older javascript/python scripts into an `archive/` or `_obsolete/` subfolder if they are not needed for day-to-day operations or CI.
2. **Docs & Images:** Unlinked markdown files in `5_Symbols/docs/` and `4_Formula/` should be linked in the respective index/readme structures (e.g. `README.md`) if they contain valuable architectural history.
3. **Backups:** Move local `.zip` backup files outside the repository workspace to minimize repository size.
