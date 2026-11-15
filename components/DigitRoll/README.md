# DigitRoll

A number that rolls digit by digit when it changes: countdowns, stopwatches, balances, scores.

**Provide:** `value` (string or number; an array of strings with `stacked` for one pair of digits per line), `className` for the type style (default `numeral-large`), optional `direction` (`auto`, `up`, `down`), `stagger` in ms (default 30), `blur={false}` to turn off motion blur, `label` for screen readers.

- Each character has its own cell, so only the digits that change move. Increasing values roll up and decreasing values roll down; when several digits change at once they start right to left, one `stagger-tight` apart, like a carry.
- The incoming digit moves on the `spatial-default` spring (it overshoots slightly and settles); the outgoing digit fades and blurs on `effects-default`. Cell edges are feathered so glyphs fade at the boundary rather than being cut.
- Use tabular numerals (the numeral styles already are) so the width never jumps.
- `stacked` puts each pair of digits on its own line, which roughly doubles the size a countdown can reach on a phone. Use it for the one hero readout on a timer screen.
- With reduced motion the digit swaps with a short fade.
- Give it a `label` that reads naturally ("4 minutes 9 seconds left"); the visible cells are hidden from screen readers.

**Compose:** `DigitRoll` in `android/ExpressiveMotion.kt` (one `AnimatedContent` per character with `motionScheme.defaultSpatialSpec()`).
