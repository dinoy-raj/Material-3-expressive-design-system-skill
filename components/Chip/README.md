# Chip

Compact, wrapping choices: filters, multi-select extras, suggestions.

**Provide:** `label`, optional `icon`, `count` (shown after the label), `selected` + `onClick` (or `defaultSelected`), `variant="tonal"` for filled chips on busy screens.

- Outlined chips filter a list (Want to read 1 · Reading 1 · Read 1). Selected chips fill with `secondary-container` and gain a check.
- Tonal chips work as suggestions or categories in a horizontally scrolling row (Board: All · Photos · Colour · Type); the selected one inverts to ink.
- Chips scroll horizontally and bleed off the right edge rather than wrapping when they are a filter bar.
