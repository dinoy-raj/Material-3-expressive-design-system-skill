# StatTile

A number with a short label, laid out in a row of two to four tiles.

**Provide:** `value` (pre-formatted: "56", "$4,375", "1/31"), `label` ("Treats", "total XP", "day streak"), optional `tone` (`primary`, `primary-container`, `positive`, `tertiary`), `display` for the serif numeral. Wrap tiles in a `div.ex-stats` grid.

- Give at most one tile a strong tone; it is the stat the screen celebrates.
- Labels are lowercase fragments, not sentences.
