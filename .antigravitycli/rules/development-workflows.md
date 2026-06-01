# Development Workflows & Conventions

## Code Editing
- **Surgical Edits**: Use targeted replacements when modifying `index.html` or other pages.
- Avoid rewriting large blocks of code without explicit review.
- Preserve existing functions, naming structures, and the structure of `questionsData` / `categories`.

## Naming Conventions
- JavaScript: Use descriptive, single-purpose functions (e.g., `renderSomething`, `handleSomething`).
- Shared scripts live in `5_Symbols/js/`; page-specific scripts must remain inline.

## Common Operations
- **Adding a Question**: Add to `5_Symbols/data/exam.json`, run `generate_questions_json.js`, follow the ID format `CAT{NN}-Q{NNN}`, and include a visual mnemonic.
- **Memory Cards**: Create memory cards via `quick_memory.html` or `add_memory_card.html` (uploaded to Azure storage container, naming pattern `MEM-Q{ID}.md`).

## Kanban Discipline
- At the end of every workspace session:
  1. Compare recent commits (`git log --oneline`) against `1_Real_Unknown/kanban.md`.
  2. Document completed work in the Kanban `Done` section (`- [x] <desc> (<hash>)`).
