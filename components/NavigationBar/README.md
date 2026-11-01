# NavigationBar

Bottom navigation for three to five top-level destinations.

**Provide:** `items` (`[{icon, label, badge?}]`), `value` + `onChange` (or `defaultValue`), optional `label`.

- The active destination gets a 56×32 pill in `primary-container`, a filled icon and a bold label. Inactive items are outlined icons in `on-surface-variant`.
- Labels are one word, nouns, never hidden: Home · Explore · Activity · Account; Learn · Practice · Studio · Progress.
- The bar sits on `surface-container` and reaches the screen edge; add the gesture inset below it.
- On unfolded and tablet widths, switch to a navigation rail on the leading edge with the same items.
