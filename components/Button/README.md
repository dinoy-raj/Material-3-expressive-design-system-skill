# Button

Pill-shaped action button that morphs to a squarer corner while pressed.

**Provide:** `children` (the label, a verb: "Review order", "Place order · $23.33"), optional `icon` (a Material Symbols name), `variant`, `size`, `tone`, `fullWidth`, and the usual button props (`onClick`, `disabled`).

- `filled` (default) is the one primary action on a screen. It sits at the bottom of a flow at `size="md"` and `fullWidth`.
- `tonal` is a secondary action that still needs weight (Trill's "Hear it", Shelfie's "Find on Google Books").
- `outlined` pairs with a filled button for the alternative path (Sell beside Buy, View in Activity above Done).
- `text` is for low-stakes inline actions (Apply, Change).
- `size="lg"` is reserved for a single climactic action such as "Book for 49,000 pts".
- `tone="error"` is for destructive confirmations; `tone="ink"` gives the near-black button Magpie uses for neutral-first brands.

Do: put the price or count in the label when the action spends something. Don't: place two filled buttons side by side; make the second `outlined`.
