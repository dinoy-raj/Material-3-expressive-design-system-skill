# TopBar

Screen header: a large title block for top-level and detail screens, or a small single-line bar for flows.

**Provide:** `title`, optional `eyebrow` (mono kicker), `subtitle`, `leading` (`back` or `close`) with `onLeading`, `actions` (`[{icon, label, onClick}]`), `size="small"` for the compact bar, `display` to set the title in the display serif.

- Top-level tabs: large `headline-large` title, no leading icon ("Explore", "Activity").
- Detail and home screens: `display` title with a supporting line ("Good evening, Ada." / "3 books on your shelves"). Emphasise one word with an italic primary span.
- Modal flows: `size="small"` with `close` ("Review and book", "New trip").
