# LoadingIndicator

Indeterminate loading shown as a shape that morphs through the shape library while it rotates.

**Provide:** optional `size` (px, default 48), `contained` to seat it in a `primary-container` circle (use over imagery or busy content), `label` (accessible name, default "Loading").

- Use for waits under about five seconds where progress can't be measured: pull-to-refresh, loading a screen, a search in flight. For measurable progress use WavyProgress.
- Show one per region, centred in the space the content will fill. Never put it inside a button; disable the button and change its label instead ("Placing order").
- With reduced motion it holds a still cookie shape.
