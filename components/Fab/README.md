# Fab

Floating action button for the screen's signature action, anchored bottom-right above the navigation bar.

**Provide:** `icon`, optional `label` (makes it extended), `tone` (`primary` = primary-container, `highlight`, `secondary`, `surface`), `size="lg"` for the hero action, `ariaLabel` when there is no label.

- One FAB per screen, 16px from the right edge and 16px above the navigation bar.
- Use `tone="highlight"` with `size="lg"` only when the action is the product (Pinhole's Shoot).
- Extended FABs name what they create: "Add flights", "New collection". They collapse to icon-only while the list scrolls down and expand again on scroll up.
