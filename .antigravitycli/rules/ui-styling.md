# Styling & UI Guidelines

## CSS Conventions
- **Vanilla CSS**: All styling must be written in plain CSS.
- Shared styles live in `5_Symbols/css/styles.css`.
- Page-specific styles should be defined inline within `<style>` tags.
- Do NOT use CSS preprocessors (Sass, Less) or frameworks (TailwindCSS) unless explicitly instructed otherwise.

## Design Tokens
Maintain a dark theme using these design tokens:
```css
--bg-primary: #0f172a
--bg-secondary: #1e293b
--bg-card: #1e293b
--border: #334155
--text-primary: #e2e8f0
--text-secondary: #94a3b8
--accent-blue: #38bdf8
--accent-purple: #a855f7
--accent-green: #10b981
--accent-yellow: #fbbf24
--accent-red: #ef4444
--accent-orange: #f59e0b
```

## Responsive Layouts
- All interfaces must be designed with mobile-first or fully responsive approaches.
- Test design layouts across all standard breakpoints (mobile, tablet, desktop).
