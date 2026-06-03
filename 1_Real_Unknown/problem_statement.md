# 📌 Problem Statement

## The Core Challenge
Preparing for the **Claude Developer Certification** exam requires more than rote memorization. The exam assesses a developer's ability to design, build, and deploy agentic workflows, model context protocols (MCP), prompt pipelines, and reliable token-efficient loops. 

Traditional study resources (e.g., static PDFs, text dumps, simple flashcards) fall short in four major ways:
1. **Passive Learning vs. Active Synthesis:** Static text fails to engage developers in active recall or structured reasoning.
2. **Context Window & Cost Bloat:** Developers struggle to understand context-window limitations, token optimization, and system-prompt compression in a tangible, visual way.
3. **No Progressive Mastery Tracking:** There is no easy, serverless way to track cognitive progression across different taxonomy levels (Bloom's Taxonomy) without complex logins.
4. **Fixed, One-Size-Fits-All Content:** A static question set cannot adapt to different learners' gaps, roles, or prior knowledge. The act of creating a question is a more powerful learning event than answering one.

---

## The Solution: Active Self-Learning App
This project provides a serverless, single-file React-based **Study Mastery App** that addresses these pain points directly:

```mermaid
graph TD
    A[Rote Memorization] -->|Inadequate for| B(Claude Certification Exam)
    C[Active Self-Learning App] -->|Solves with| D[Spaced Repetition & Cookie Progress]
    C -->|Solves with| E[Visual Mnemonics & Mindmaps]
    C -->|Solves with| F[Structured Reasoning Practice]
    D & E & F -->|Leads to| G[Deep Architectural Intuition]
```

### Key Solution Pillars:
* **Active Recall:** A growing, open-ended question bank mapped to the 5 core exam competencies. The count is not capped — learners are expected to add their own questions as part of the study process.
* **Personalised Content Creation:** Every learner can build their own questions, memory cards, and study stories via the admin tools. The act of authoring a question is a higher-order learning event than passively answering one (Bloom's Create tier).
* **Spaced Repetition & Spaced Retrieval:** Leveraging browser cookies to track mastered items and dynamically surface weak areas without backend server dependencies.
* **Visual Mnemonics:** Each question includes detailed SVG/emoji memory aids to associate dry concepts with memorable objects. New cards can be authored and published to Azure without a code deployment.
* **Structured Learning Path:** Concept documents mapping directly to Bloom's learning stages (Remembering via flashcards → Analysing via diagrams → Creating via active tool building and question authoring).
