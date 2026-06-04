# 📋 Claude Developer Certification - Kanban Board

## 📥 Backlog
- [ ] Add alerting for the cost management https://portal.azure.com/#view/Microsoft_Azure_CostManagement/Menu/~/costanalysis/openedBy/AzurePortal > requires manual Azure Portal setup


-> These backlog tasks are implemented in bulk by Claude and moved to done

## ⚙️ In Progress
### WIP 1 : Real time AI everything else goes to backlog

-> Manually getting implemented by Gemini and hands on implementation

## ⚙️ Maintenance

- [ ] Update the environment folder > 1_Real_Unknown
- [ ] Update the environment folder > 2_Environment
- [ ] Add new features incoming as visuals folder > 3_Simulation
- [ ] Add new ways of doing the implementation  to formula folder > 4_Formula
- [ ] Update the Symbols and pay technical debt > 5_Symbols
- [ ] Add new errors in semblance  > 6_Semblance
- [x] Update the tests folder > 7_Testing_Known — link checker added


## ✅ Done
- [x] Fix SEO — add OG/Twitter/description meta to index.html, fix sitemap.xml and robots.txt to ai_certification_prepare URLs, add 25+ pages to sitemap
- [x] Update 7_Testing_Known README with certifications earned table and proof the self-learning method works
- [x] Rebrand site to AI Certification Prep — update titles, footers, GitHub links, and git remote to ai_certification_prepare across all pages
- [x] Create Red Hat AI Roadmap page (EX267) in Analyse section with 9 skill domains, study checklist, and exam facts; add to nav menu
- [x] Add Red Hat EX267 certificate and personal AI certificate roadmap (Claude → Red Hat → AWS → GCP → Azure → USAII) to evaluate_certificates.html
- [x] Multilingual TTS audio — generate 102 Turkish MP3s locally via Kokoro, upload to Azure, dual EN/TR audio buttons in cards/remember/pro-exam, formula documented (`1b6e095`)
- [x] Open issue and implement Gemini Live for live training sessions (`f9d4d9b`)
- [x] Add Gemini Live two-choice voice quiz tactic to tactics page (`d66e34f`)
- [x] Add Azure Portal link for exam-notes container (`eab2a4f`)
- [x] Rewrite exam_notes_architecture with full storage map and save flows (`8fbe496`)
- [x] Persist image upload version so reloads always show the fresh image (`044df39`)
- [x] Image clipboard upload in popup + question ID in slideshow URL (`9e7f3b1`)
- [x] WhatsApp learning style in evaluate page (`78485d0`)
- [x] Sync view mode to URL param (?mode=scroll|slideshow) with history API (`4485d82`)
- [x] Display learner name badge in pro-exam header + add architecture doc (`e555715`)
- [x] Add personal notes editor and learner identity to pro-exam image popup (`50d5b7f`)
- [x] Center images and preserve scroll/view state on mastered + add repetitive exam runs tactic (`fa72cad`)
- [x] Prevent image stretching in pro-exam popup modal (`ebd6797`)
- [x] Display question text in image popup modal on pro-exam (`b3afddf`)
- [x] Image hover on story transitions shows 2x zoom and transition text (`04d229c`)
- [x] Implement keystroke debouncing for story editor saves and log in semblance (`1f2527a`)
- [x] Create story save cost estimation formula doc (`fd5c086`)
- [x] Document deployment tar failure and resolution in chronological error log (`4a485f0`)
- [x] Remove stale .antigravitycli symlink before Pages artifact upload (`4401bae`)
- [x] Remove agent state directories and .DS_Store from git tracking and restore .gitignore (`04151fc`)
- [x] Add high-contrast, prominent layout selection buttons to pro-exam page (`0bf8092`)
- [x] Update CLAUDE.md as single source of truth: fix question count (124), expand Azure container map (3→7), rebuild directory layout, add data-loading pattern and Cloudflare Workers section (`f800847`)
- [x] Align antigravity.md: remove generic template language, add deduplication + agent-file protocol, delegate shared rules to CLAUDE.md (`3b7aa85`)
- [x] Update bmad.html with dual meaning (Breakthrough Method Agile Delivery + Build Model Apply Deliver), upload to Azure, add Azure upload skill to claude.md, gitignore backups
- [x] Create a task to backup the data that is in the system, define the formula document in [backup_system_data.md](file:///Users/rifaterdemsahin/projects/claude_certification_exam/4_Formula/backup_system_data.md) and implement the Python utility in [backup_data.py](file:///Users/rifaterdemsahin/projects/claude_certification_exam/5_Symbols/scripts/backup_data.py)
- [x] Hide already used concepts, questions, and memory cards from the "Add Items to Outline" select pickers in the Visual Story Writer (`story.html`) and dynamically refresh them.
- [x] Highlight active menu group in navbar — active-group CSS on dropdown button, isActive handles query params, renderMenu updated (`077a3cc`+)
- [x] Fix menu.json trailing comma bug and add missing Story Canvas entry to Create menu
- [x] Move quick_memory, add_memory_card, and analyse_renderer?action=new into ⚙️ Admin group under Create menu; remove from Remember and Analyse menus; upload menu.json to Azure
- [x] Add top-down visual study story writer with AI text generator and JSON saving (`5408808`)
- [x] Migrate exam question markdown files to Azure Blob Storage and update references (`d9e1d4c`)
- [x] Migrate core concept markdown files to Azure Blob Storage and update references (`b2014d7`)
- [x] File removal for the assets (`00863ff`)
- [x] Add Generate the audio files upload to azure and add Kokoro audio play button to pro-exam.html > https://rifaterdemsahin.github.io/claude_certification_exam/5_Symbols/pages/pro-exam.html
- [x] Pro exam updates — navigation, styling, and content improvements (`9d9504d`)
- [x] Add Category selection + 🤖 Generate Template button + 📋 Copy AI Prompt button to analyse_renderer.html new-page creation form
- [x] Update remember.html: show Azure memory palace images when answer revealed, improved ⬅️/👁️/➡️ nav buttons with icons, 🔊 audio play button scaffold
- [x] Azure data loading: created data_loader.js (fetches questions.json from Azure, falls back to data.js); generated questions.json; remember.html and mastery.html now load via dataReady promise; loading state shown while fetching
- [x] Add AI spend, AI weak links, Jupiter Labs AI code, slash commands, AI mental health, World model (Gemini Omni) to the Analyse menu as 📹 Video Resources section in menu.json and nav.js; also added to search_index.json
- [x] Add history_of_ai_from_semi_conductors.html to the Analyse menu (Architectures & Loops section) and search_index.json
- [x] Add maintenance checklist to claude.md and antigravity.md covering all 7 stage folders (`cf2b9b2`)
- [x] Kokoro TTS pipeline: Dockerised `ghcr.io/remsky/kokoro-fastapi-cpu:latest`, generated all 100 MP3s, uploaded to Azure `memory-audio` container, wired `audioUrl` in data.js (`fabf3ca`)
- [x] Add Kokoro TTS pipeline — audio generation, Azure upload, and play button wiring initial setup (`c8c6ba5`)
- [x] Update costs.md with Gemini and Claude CLI monthly subscription details (`46ec704`)
- [x] Add 🔊 Play Audio button to memory cards — flip card back and modal in cards.html (`3217eff`)
- [x] Update costs.md with AI developer tools and maintenance checklist additions (`8707004`)
- [x] Add `2_Environment/kokoro.md` (Docker setup, API ref, Azure config, troubleshooting) and `4_Formula/kokoro_audio_pipeline.md` (end-to-end pipeline formula)
- [x] Update `2_Environment/azure.md` with `memory-audio` container row and portal link
- [x] Add debug console logging (page, session keys, cookies) when debug mode is active
- [x] Make analyse menu dropdowns open on click in addition to hover (click-toggle with .click-open class)
- [x] Auto-collapse Blooms guide by default (closed unless user explicitly opens it; cookie persists preference)
- [x] Dynamic Azure-hosted menu.json and search_index.json synced automatically upon page saving/deletion.
- [x] Ensure understand.html loads shared navigation menu (`02ca084`)
- [x] Fix: load new page editor when action=new query param is present (`13044e1`)
- [x] Move the Analyse pages to Azure
- [x] Implement Delivery Pilot Template
- [x] Update and rewrite bookmarks.md, register in layout trees, sidebar notes, and debug menus (`2c9bd58`)
- [x] Create sanity check review v2 and document project gaps (`3ab086f`)
- [x] Copy and upload generated mnemonics for questions 23-29, 33-39, 49-53 and fix security push blocker (`2fb081a`)
- [x] Update Semblance log with verification check at 13:12 (`558c228`)
- [x] Add `mnemonic_generation_blockage.md` Semblance document (`1acf6c3`)
- [x] Generate and upload initial batch of surreal memory palace images (q018-q022, q032, q045-q048) (`c0cfc08`)
- [x] Generate and upload memory palace diagrams for questions 18 to 58 and verify (`9a43cf5`)
- [x] Update hint images for questions 7 to 17 to PNG format and verify (`37c7531`)
- [x] Update hint images for questions 1 to 6 to PNG format and verify (`dde12bb`)
- [x] Add mastered functionality to pro-exam with cookie persistence and reset (`108737c`)
- [x] Find and remove duplicates, and create `antigravity.md` guidelines (`24f0b71`)
- [x] Move duplicate tactics sections from `index.html` to `tactics.html`, classify tactics.html under Category 5 (Create) and update emoji to temple (`e23ba16`)
- [x] Add Bloom's self-learning progress tracker widget with cookie persistence, self-reporting, and automatic hooks (`b6c4ecf`)
- [x] Update navigation labels with step numbers and add visual Bloom's self-learning loop guide banner (`41ff98e`)
- [x] Add `sanity_check_review_v1.md` to document project structure observations and suggestions (`da00e16`)
- [x] Add `user_experience.md` to debug drawer menu list and update tests (`f62511b`)
- [x] Create `user_experience.md`, document mockups, update layouts, and pass JSDOM tests (`2b8e59e`)
- [x] Link checker test: `7_Testing_Known/test_links.js` — checks 49 GitHub Pages + Azure blob URLs, generates fix prompt for broken links; 49/49 pass (`npm run test:links`)
- [x] Add Multi-Media Learning tactics page and register in navigation and search indexes (`a71531e`)
- [x] Embed 🔊 audio play button in remember.html — always visible below question, auto-stops on nav (`c91def0`+)
- [x] Add `2_Environment/azure.md` and expand environment directory trees (`a3a7402`)
- [x] Add Stage 1 problem_statement, okrs, questions, hypotheses and expand directory trees (`b01f12a`)
- [x] Update paths and references to align with the 7-Stage directory layout (5_Symbols and 7_Testing_Known) (`98645d3`)
- [x] Add Debug Menu Dashboard in delivery pilot template
- [x] Refactor project structure to follow Delivery Pilot Template layout — 7-stage folders (`eadf1e2`)
- [x] Update references to lowercase agent files and point all formula paths to 4_Formula (`b3776f7`)
- [x] Perform sanity check — execute link updates and agent rules case sanitization (`ec20114`)
- [x] Move concept images to Azure Blob Storage and update references (`535ee0c`)
- [x] Remove local SVG files and load all images from Azure Blob Storage (`7afd7b3`)
- [x] Generate and include 57 professional SVG diagrams for Pro Exam (`81fc91c`)
- [x] Add complete image generation pipeline for Pro Exam (`f8783ee`)
- [x] Fix Pro Exam data loading and add modal image viewer (`236ba57`)
- [x] Add Pro Exam page with 26 advanced questions and image reveal system (`ee9f674`)
- [x] Redesign Discussion Board to use exam database with cherry-pick (`c97ef57`)
- [x] Transform Understand into Discussion Board with cherry-pick & submission (`e18a686`)
- [x] Add AI-powered Understand page with dynamic question generation (`6febc76`)
- [x] Add incorrect answers summary page with export options (`b495eaf`)
- [x] Add filter for incorrect answers in practice exam (`96e75d8`)
- [x] Fix: remove invalid q.options.find() call causing data.js to fail (`083ff79`)
- [x] Add memory card modal popup to practice exam (`dc83a1d`)
- [x] Add admin authentication for delete/add operations (`b7aa19c`)
- [x] Add delete/edit functionality and dynamic card loading to memory cards (`c07dde4`)
- [x] Add DELETE method to Cards endpoint (`69cde21`)
- [x] Consolidate cards endpoints to resolve Azure Functions route conflict (`21b1c74`)
- [x] Fix CORS preflight failure on Azure Function API endpoints (`b875e29`)
- [x] Add Azure Function deployment guide (`8d9c09f`)
- [x] Add Azure content storage architecture document (`223a3a6`)
- [x] Migrate memory cards and images to Azure Blob Storage (`a7edfc1`)
- [x] Add Cloudflare Worker deployment guide with Mermaid diagrams (`02c5f9f`)
- [x] Wire memory card creation through Cloudflare Worker (`9521a72`)
- [x] Add memory card creation page and GitHub token docs (`5936a77`)
- [x] Add Practice Exam page with all exam source questions (`ea48430`)
- [x] Add Create page with 16 PoC video ideas and audience voting (`94411ef`)
- [x] Add LLM Context Size concept and implement concept mastery tracking with cookies (`41a01cd`)