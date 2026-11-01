# Card

Rounded container that separates content by tone, not by shadow.

**Provide:** `children`, optional `title`, `body`, `eyebrow`, `variant` (`low` default, `filled`, `outlined`, `elevated`, `primary`, `secondary`, `tertiary`, `highlight`), `padding="sm"`, `display` to set the title in the display serif, `onClick` to make the whole card pressable (it morphs its corners on press).

- Default cards use `surface-container-low` with `shape-xl` corners.
- Tonal cards (`primary`, `secondary`, `tertiary`) carry the hero content of a hub screen: Trill's Daily mix, Note Rush and Ear gym are three tonal cards in a stack, each with its own container colour, an icon in a shape and one action.
- Never put a coloured border stripe on one edge of a card.
