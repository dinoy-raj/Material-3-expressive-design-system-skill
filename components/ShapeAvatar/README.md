# ShapeAvatar

Letter, icon or illustration seat cut from the M3 Expressive shape library.

**Provide:** `shape` (`cookie4`, `cookie6`, `cookie9`, `cookie12`, `clover4`, `flower5`, `flower8`, `sunny`, `burst`, `pebble`, `circle`), `text` (one letter) or `icon`, `tone`, `size` (px, default 40), `label` for a meaningful image, `spin` for a slow decorative rotation on hero moments.

- Give each entity type one shape and keep it (tickers are cookie9, collections are clover4, agents are flower5). Colour can vary per item; the shape stays.
- Use big shapes (96px+) behind hero icons, a book cover, a mascot, the app's icon.
- `ShapeAvatar.path(name)` returns the SVG path (viewBox -1 -1 2 2) for clipping images or drawing your own.
