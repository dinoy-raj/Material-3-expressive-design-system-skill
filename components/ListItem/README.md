# ListItem

One row of a list: leading visual, headline, supporting text, optional mono meta line and a trailing value.

**Provide:** `headline`, optional `supporting`, `meta` (mono uppercase), `leading` (usually a ShapeAvatar), `trailing` (a value, ValuePill, Button or icon), `onClick`.

- Ticker and order rows: shape avatar with the first letter, ticker as headline, company as supporting, ValuePill trailing.
- Activity rows: date grouping uses an `eyebrow` header above the rows (TODAY, MON, OCT 5).
- Rows are 56px minimum; no dividers between rows; group with whitespace or a GroupedList.
