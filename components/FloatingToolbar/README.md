# FloatingToolbar

A pill of contextual actions that floats above content, often beside a FAB; the M3 Expressive replacement for a bottom app bar.

**Provide:** `items` (`[{icon, label, toggle?, onClick?}]`, three to six), optional `defaultValue`/`value` (index of the selected toggle), `vibrant` (primary-container instead of surface-container), `fab` (Fab props) to place a FAB beside it, `label`.

- Use for editing and viewing tools that act on what's on screen: a photo editor, a map's layers, a document's formatting.
- Centre it 16px above the bottom edge (above the nav bar if one is shown). Hide it on scroll down and bring it back on scroll up.
- Toggle items (layers, tools) take a squircle selection in `secondary-container`.
