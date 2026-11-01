# ButtonGroup

Connected button group: single choice among two to five options, with the selected option growing into a full pill.

**Provide:** `options` (`[{value, label, icon?, sub?}]`), `value` + `onChange` (or `defaultValue`), `label` (accessible group name), optional `tone` (`secondary` for settings, `container` for a softer selection), `fit` to hug content instead of filling the width.

- Segments are 2px apart, outer ends fully round, inner corners `shape-sm`. The selected segment rounds fully: this is the M3 Expressive signature.
- Use for time ranges (1D · 1W · 1M), modes (Dollars / Shares, Calm / Balanced / Swift), sizes with prices (`sub`: "$4.50"), tips (None · 10% · 15% · 20%).
- More than five options, or multi-select: use Chips.
