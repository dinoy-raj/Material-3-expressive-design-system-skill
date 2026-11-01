# Slider

Expressive slider: a thick 16px track split by a bar handle, with a stop dot at the end.

**Provide:** `label`, `defaultValue` or `value` + `onChange`, optional `min`, `max`, `step`, `format` (renders the value, e.g. `v => v + '%'`), `supportingText`, `id`.

- Show the current value large beside the label; it is the answer the person is choosing.
- Use for one continuous value with a meaningful range (backup reserve, filter strength, budget). For three to five fixed stops use a ButtonGroup.
