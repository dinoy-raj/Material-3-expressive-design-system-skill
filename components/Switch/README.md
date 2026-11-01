# Switch

On/off toggle that applies immediately, with a check in the thumb when on.

**Provide:** `label` (renders the full settings row), optional `supportingText`, `checked` + `onChange` (or `defaultChecked`).

- Use for preferences that take effect without a save button ("Pit stops on map", "Storm Watch").
- The supporting line explains the consequence in plain words ("Watching the forecast. Nothing stormy in the next five days.").
- Inside a GroupedList, each switch row is its own segment.
