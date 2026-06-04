# 🎯 Objectives and Key Results (OKRs)

This document outlines the measurable goals for the **AI Certification** platform — a self-learning system to master AI concepts, close skill gaps, and collect industry-recognised AI certifications.

---

## 🎯 Objective 1: Learn AI Concepts Deeply Across Multiple Certification Domains
*Use active self-learning technologies to build genuine understanding of AI — not just pass exams.*

* **KR 1.1:** Maintain a growing question bank covering all active certification tracks on the platform (baseline: 124 seed questions for Claude Developer cert). Each learner authors their own questions as part of the study process — there is no fixed ceiling.
* **KR 1.2:** Every question has a corresponding visual mnemonic (SVG/emoji) in the Memory Palace style to reinforce conceptual retention beyond rote memorisation.
* **KR 1.3:** Build and maintain concept study guides in Azure Blob Storage covering 100% of core AI topics across all tracked certifications (agents, MCP, prompt engineering, MLOps, OpenShift AI, etc.).
* **KR 1.4:** Enable any learner to author and publish their own questions, memory cards, and study stories via `quick_memory.html`, `add_memory_card.html`, and `story.html` — measuring success by tooling availability, not a fixed content count.

---

## 🎯 Objective 2: Collect AI Certifications by Proving Real Skill
*Overcome certification anxiety by converting knowledge gaps into demonstrated, testable competency.*

* **KR 2.1:** Track a personal AI certificate roadmap covering at minimum: Anthropic Claude Developer → Red Hat OpenShift AI (EX267) → AWS AI Practitioner → Google Cloud ML Engineer → Azure AI Engineer → USAII CAIS™.
* **KR 2.2:** For each certification on the roadmap, build a dedicated study page (skill domains, exam logistics, personal checklist) before sitting the exam.
* **KR 2.3:** Achieve a target benchmark of **85%+ on practice exams** for each certification before attempting the real assessment.
* **KR 2.4:** Maintain cookie-based local progress tracking with **100% persistence** across sessions so every study session builds on the last.

---

## 🎯 Objective 3: Use Self-Learning Technologies to Close Skill Gaps Faster
*Leverage AI tools — audio, multiplayer, discussion boards, story canvas — to compress the learning loop.*

* **KR 3.1:** Multilingual audio (EN + TR) available for all memory cards so learners can study without a screen (commute, gym, etc.).
* **KR 3.2:** Multiplayer exam game and discussion board available so learners can test each other and surface gaps they didn't know existed.
* **KR 3.3:** Story canvas and visual architecture tools available to externalise mental models, not just consume content passively.
* **KR 3.4:** Gemini Live voice coach integration available as a study tactic for spoken recall practice.

---

## 🎯 Objective 4: Maintain a Zero-Friction, Always-Available Platform
*A fast, reliable, no-build static site that gets out of the way of learning.*

* **KR 4.1:** Single-file entry point (`index.html`) with CDN-based libraries — zero build steps, works offline from cache.
* **KR 4.2:** 100% automated deployment to GitHub Pages via GitHub Actions on every push to `main`.
* **KR 4.3:** Azure Blob Storage for all binary assets (audio, images, markdown) — nothing large committed to git.
* **KR 4.4:** Automated link and logic tests in `7_Testing_Known/` run on every commit to catch broken URLs before learners hit them.
