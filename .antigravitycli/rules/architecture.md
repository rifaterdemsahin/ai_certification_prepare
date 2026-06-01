# Core Architecture & Structure

## Single-File Entry
- The main entry point is `index.html` at the repository root.
- It serves as the main dashboard and is hosted directly via GitHub Pages.
- No build steps: Do not introduce npm, webpack, vite, or any build compilation tools. All external libraries (React 18, Mermaid, etc.) must be loaded via CDNs in `index.html`.

## Page Structure
- Feature pages reside in the `5_Symbols/pages/` directory.
- All auxiliary pages share `5_Symbols/js/nav.js` for dynamic navigation.

## Navigation & Bloom's Taxonomy
- Pages are organized and grouped by Bloom's Taxonomy levels inside `5_Symbols/data/menu.json` (stored on Azure storage and loaded dynamically):
  - **Remember**: flashcards, slideshow, mastery, quiz, memory cards.
  - **Understand**: discussion board.
  - **Analyse**: stats, concepts, video resources, analyse renderer.
  - **Evaluate**: pricing, multiplayer, certificates.
  - **Create**: story writer, creator, tactics, admin tools.

## State Management
- State is managed via browser cookies to persist user progress (e.g., mastery, learning loop preference).
- Shared state logic is defined in `5_Symbols/js/state.js`.
