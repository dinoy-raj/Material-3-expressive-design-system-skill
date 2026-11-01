# TextField

Outlined text field with its label notched into the border, or a filled variant for sheets.

**Provide:** `label`, optional `defaultValue`, `placeholder`, `supportingText`, `error` (a message string), `multiline`, `variant="filled"`, `trailingIcon`, `inputMode`, `id`.

- The label names the field in sentence case ("Title", "Author(s)", "What did it say?"); supporting text gives the format ("13 digits, or 10 for older books").
- Errors replace the supporting text and say how to fix it.
- On a container, set `--field-ground` on a wrapper to that container's colour so the notch blends.
