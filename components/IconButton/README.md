# IconButton

Round 48px icon-only control for app-bar actions, favourites and card affordances.

**Provide:** `icon` (Material Symbols name), `label` (required: the accessible name), optional `variant` (`standard`, `filled`, `tonal`, `outlined`), `selected` for toggles, `size="sm"` (40px) inside dense cards.

- `standard` lives in top bars (back, close, more_vert).
- `tonal` floats over imagery and illustrations (Dollop's back arrow and heart over the treat photo).
- A toggle (favourite, watchlist star) fills its icon and turns `primary` when `selected`.

Don't use an icon button where the meaning isn't obvious from the glyph alone; use a Button with a label.
