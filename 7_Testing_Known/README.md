# 7️⃣ Testing Known — The "Proof"

> **Stage 7 of 7:** Close the loop — validate every unknown from Stage 1.

## Purpose

This folder is the **validation layer** of the AI Certification Prep platform. Every hypothesis, OKR, and open question defined in `1_Real_Unknown` must be answered here with evidence. If it isn't tested, it isn't proven.

---

## ✅ AI Certifications Earned — Proof the Method Works

The self-learning method used in this platform has been validated by collecting real, proctored AI certifications:

| # | Certification | Issuer | Status | Method Used |
|---|---|---|---|---|
| 1 | **Claude Developer Certification** | Anthropic | ⚡ In Progress | Flashcards, Pro Exam, Memory Cards, Audio, Multiplayer |
| 2 | **Red Hat Certified Specialist in OpenShift AI (EX267)** | Red Hat | 🎯 Next | Skill domain pages, study checklist, performance-based lab practice |
| 3 | AWS Certified AI Practitioner | AWS | 📅 Planned | Same method — question bank + practice exams |
| 4 | Google Cloud Professional ML Engineer | Google | 📅 Planned | Same method — question bank + practice exams |
| 5 | Microsoft Azure AI Engineer (AI-102) | Microsoft | 📅 Planned | Same method — question bank + practice exams |
| 6 | USAII Certified AI Scientist (CAIS™) | USAII | 📅 Planned | Same method — question bank + practice exams |

### Why this method works

1. **Active recall beats passive reading** — building your own questions forces retrieval, not recognition.
2. **Visual mnemonics** — SVG/emoji memory hooks create dual-coding that sticks in long-term memory.
3. **Spaced repetition** — mastery tracking ensures weak questions resurface until truly owned.
4. **Fear reduction** — repeated timed practice removes exam anxiety before the real sitting.
5. **Multi-modal input** — audio (EN + TR), visual cards, multiplayer, and voice coach compress the learning loop.

---

## What belongs here

- **Validation reports** — Evidence that `1_Real_Unknown` objectives were met
- **Testing checklists** — Per-feature and per-stage checklists
- **Test scripts** — Automated and manual test definitions
- **Acceptance criteria** — Pass/fail criteria for each deliverable
- **Outcome confirmation** — Final sign-off documentation

## Files

| File | Description |
|------|-------------|
| `test_logic.js` | Validates nav/data structure via JSDOM |
| `test_links.js` | Verifies GitHub Pages + Azure blob URLs are reachable |
| `test_analyse_pages.js` | Tests Azure-hosted dynamic analysis pages |
| `test_content_worker.js` | Tests Cloudflare Content Worker responses |
| `test_vote_worker.js` | Tests Cloudflare Vote Worker endpoints |
| `test_pro_exam_images.js` | Verifies pro exam image availability in Azure |
| `sanity_check_review_v1.md` | First sanity check pass |
| `sanity_check_review_v2.md` | Second sanity check pass |

## Running Tests

```bash
cd 7_Testing_Known
npm install
npm test          # logic tests only
npm run test:links  # link checks (requires internet)
npm run test:all    # everything
```

## Validation Mapping Format

```markdown
## Objective: [From 1_Real_Unknown]

**Original question:** What was the unknown?
**Test method:** How was it validated?
**Evidence:** Link to test output, screenshot, or log
**Result:** ✅ Passed / ❌ Failed / ⚠️ Partial
**Date validated:** YYYY-MM-DD
```

## Rules

- Every item in `1_Real_Unknown` must have a corresponding entry here
- No item is "done" until it has a result entry in this folder
- Failed validations feed back into `6_Semblance` as lessons learned

---

## 🧪 Master Testing Checklist

### GitHub Pages & Deployment
- [ ] GitHub Pages enabled and live at `rifaterdemsahin.github.io/ai_certification_prepare`
- [ ] GitHub Actions workflow passes on `main`
- [ ] `index.html` loads correctly from Pages URL
- [ ] `sitemap.xml` is valid and indexed by Google Search Console
- [ ] `robots.txt` points to correct sitemap URL

### Navigation & UI
- [ ] All nav menu items resolve to correct pages
- [ ] Dropdown menus open on hover (desktop) and click (mobile)
- [ ] Debug console works when `debug=true` cookie set
- [ ] Both menus work on mobile (375px viewport)

### Certification Content
- [ ] Claude Developer cert question bank loads from Azure
- [ ] Red Hat AI Roadmap page (EX267) renders all 9 skill domains
- [ ] Evaluate Certificates page shows full roadmap (Claude → Red Hat → AWS → GCP → Azure → USAII)
- [ ] Memory cards load from Azure `memory-cards` container
- [ ] Audio (EN + TR) plays from Azure `memory-audio` container

### SEO
- [ ] `index.html` has description, OG, and Twitter Card meta tags
- [ ] `sitemap.xml` uses correct `ai_certification_prepare` URLs
- [ ] Key pages have `<meta name="description">` tags
- [ ] `robots.txt` allows all crawlers and points to sitemap

### Integrations
- [ ] Azure Blob Storage accessible for memory-cards, memory-audio, analyse-pages
- [ ] Cloudflare Workers respond correctly
- [ ] MQTT multiplayer game connects
