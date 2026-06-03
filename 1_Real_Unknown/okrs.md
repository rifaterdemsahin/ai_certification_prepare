# 🎯 Objectives and Key Results (OKRs)

This document outlines the measurable goals for the **Claude Developer Certification Study Mastery App** to ensure development efforts translate to learning success.

---

## 🎯 Objective 1: Optimize Candidate Preparedness for Core Competencies
*Enable candidates to achieve high proficiency and pass the certification exam on their first attempt.*

> **Note on question counts:** The question bank is intentionally open-ended and growing. A fixed number is not the goal — every learner is expected to author their own questions as part of the study process. Counts below are baselines, not ceilings.

* **KR 1.1:** Maintain a growing, community-extensible question bank aligned to all 5 official exam weights (baseline: 124 seed questions). Each learner can add personalised questions via the admin tools without a code deployment:
  * Agentic Architecture & Orchestration (27%)
  * Tool Design & MCP Integration (18%)
  * Claude Code Configuration & Workflows (20%)
  * Prompt Engineering & Structured Output (20%)
  * Context Management & Reliability (15%)
* **KR 1.2:** Implement robust cookie-based local state tracking that maintains **100% progress persistence** across browser refreshes and sessions, regardless of total question count.
* **KR 1.3:** Build a practice mock exam mode that samples questions dynamically and yields a target benchmark of **85%+ score capability** for active users.

---

## 🎯 Objective 2: Maximize Conceptual Retention via Rich Visuals, Active Recall & Content Creation
*Move candidates from passive reading to active evaluation and creation — including authoring their own questions and memory cards.*

* **KR 2.1:** Every question in the bank has a corresponding visual mnemonic (SVG/emoji) in the Memory Palace style. New questions authored by learners should also get a visual aid — the tooling supports this without a code push.
* **KR 2.2:** Build an interactive **SVG-based Mindmap** that traces conceptual relationships between key certification areas (e.g., how prompt caching connects to context window management).
* **KR 2.3:** Maintain detailed concept study guides in Azure Blob Storage covering 100% of core topics (MCP, Claude Code, Spaced Memory).
* **KR 2.4:** Enable any learner to author and publish their own questions, memory cards, and study stories via `quick_memory.html`, `add_memory_card.html`, and `story.html` — measuring success by the availability of the authoring tools, not by a fixed content count.

---

## 🎯 Objective 3: Maintain a Seamless, Zero-Maintenance Deployment Architecture
*Ensure a fast-loading, highly reliable static app with minimal deployment overhead.*

* **KR 3.1:** Leverage CDN-based library delivery (React, Mermaid) to maintain a **single-file main architecture (`index.html`)** with zero build compilation steps.
* **KR 3.2:** Achieve 100% test coverage for the JSDOM test runner logic inside `/7_Testing_Known/` on every commit.
* **KR 3.3:** Maintain **100% automated deployment** to GitHub Pages via GitHub Actions upon push to `main`.
