# SplitButton

A primary action joined to a menu of related actions: the trailing half rounds fully and its chevron turns when the menu is open.

**Provide:** `children` (the main action label), optional `icon`, `variant` (`filled`, `tonal`, `outlined`), `size="md"`, `items` (`[{label, icon, onClick}]`) for the menu, `menuLabel`, `defaultOpen`, `onClick` for the main action.

- Use when one action is the obvious choice but close alternatives exist: "Save" with Save as copy and Save as template; "Share" with Copy link and Send.
- The two halves sit 2px apart with small inner corners, exactly like a connected button group.
- Don't use it when the options are equal; use a ButtonGroup or a menu button.
