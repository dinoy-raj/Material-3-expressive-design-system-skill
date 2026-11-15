# Motion recipes

How Expressive Kit moves, and copy-ready recipes for the moments most apps need. Every recipe uses the motion tokens, works on the web and in Compose, and says what to do when the person has turned animations off.

## The tokens

Motion is spring-based. **Spatial** springs move position, size, rotation and shape, and may overshoot. **Effects** springs change colour and opacity, and never overshoot. Pick the speed by how much of the screen moves.

| Token | Expressive (damping / stiffness) | Standard | Settles in | Use for |
| --- | --- | --- | --- | --- |
| `spatial-fast` | 0.6 / 800 | 0.9 / 1400 | ~360ms | Switch thumbs, pressed corners, nav indicators, icon micro-motion, a dial handle |
| `spatial-default` | 0.8 / 380 | 0.9 / 700 | ~430ms | A card expanding, list items making room, a digit rolling, a shape morph |
| `spatial-slow` | 0.8 / 200 | 0.9 / 300 | ~600ms | Screen transitions, a hero travelling across the screen |
| `effects-fast` | 1.0 / 3800 | same | ~150ms | State layers, icon fill, a label fading |
| `effects-default` | 1.0 / 1600 | same | ~230ms | A container changing tone, content cross-fading |
| `effects-slow` | 1.0 / 800 | same | ~330ms | Scrims, whole-screen fades |
| `stagger-tight` | 30ms | | | Between sibling digits or toolbar icons |
| `stagger-list` | 40ms | | | Between list rows entering, capped at six rows |

**Web.** `tokens/tokens.css` defines `--motion-<token>` (duration and easing together), plus `--motion-<token>-duration` and `--motion-<token>-easing`. Browsers that support `linear()` get the real spring curve, sampled from the damping and stiffness above; older ones get a cubic-bezier approximation. Put `data-motion="standard"` on `<html>` to switch the whole page to the standard scheme. For JS-driven motion use `Expressive.motion.animate(from, to, 'spatial-fast', onFrame)`, which runs a real spring and accepts a starting velocity.

```css
.card { transition: transform var(--motion-spatial-default), background-color var(--motion-effects-default); }
```

**Compose.** `ExpressiveTheme(motionScheme = MotionScheme.expressive())` installs the scheme. Read springs from it rather than writing numbers: `MaterialTheme.motionScheme.fastSpatialSpec<Float>()`, `defaultSpatialSpec()`, `slowSpatialSpec()`, `fastEffectsSpec()`, `defaultEffectsSpec()`, `slowEffectsSpec()`.

## Rules

1. **Springs for movement, not fixed timings.** Use a duration-and-curve tween only for oscillations (a wiggle) and loops.
2. **Interruptible.** A new input retargets the spring from where it is now, carrying its velocity. Never restart from the beginning. On the web, cancel the running `animate` and start a new one from the current value; in Compose, `Animatable.animateTo` already does this.
3. **Carry the gesture's velocity.** When a drag ends, pass its velocity into the settle spring (`initialVelocity` in Compose, the `velocity` argument on the web). A flick should keep going a little; a slow release should settle in place.
4. **One moment per transition.** The hero moves on a spatial spring; everything else fades on an effects spring.
5. **Movement overshoots, colour never does.** Don't put a spatial spring on a colour or an opacity.
6. **Reduced motion.** When `prefers-reduced-motion: reduce` is set (web) or the animator duration scale is 0 (Android, `rememberReducedMotion()`), drop movement, bounce, rotation and ambient loops, and keep short fades. The tokens already do this on the web: every spatial token becomes 0ms.

## Recipes

### Digit roll

For countdowns, stopwatches, balances and scores. Each character sits in its own cell and only changed digits move. Increasing values roll up and decreasing values roll down; when several digits change at once (09 → 10), they start right to left, one `stagger-tight` apart, like a carry. The incoming digit springs in on `spatial-default` with a slight overshoot; the outgoing digit fades and blurs out on `effects-default`; cell edges are feathered so glyphs fade at the boundary instead of being cut.

- Web: `<DigitRoll value="25:09" />`; `stacked` with `value={['00','25','09']}` puts one pair of digits per line, which roughly doubles the size a phone can fit.
- Compose: `DigitRoll(text, style = ExpressiveTextStyles.numeralLarge)` in `android/ExpressiveMotion.kt`.
- Reduced motion: a short fade.

### State-change pulse

When a single object changes state (an alarm switched on, a stopwatch starting, a task done), squash it to 0.96 and let it settle on `spatial-default`. It confirms the change on the object itself, without a toast. Not on first appearance, and never for routine taps.

- Web: add `.ex-pulse` (re-trigger by changing the element's `key` or toggling the class).
- Compose: `Modifier.statePulse(key = alarm.enabled)`.

### Animated weight

With a variable font, weight can carry state: an alarm that is off reads lighter than one that is on. Animate `wght` on an effects spring (it's a change of ink, not of position).

- Web: `font-variation-settings` can't use tokens directly, so transition `font-weight` with `var(--motion-effects-default)`; Google Sans Flex interpolates smoothly.
- Compose: `fontFamily = animateVariableWeight(R.font.google_sans_flex, opticalSize = 57f, targetWeight = if (on) 600 else 300)`.

### Icon micro-motion

A tapped icon can make one small motion that fits its meaning: a bell or alarm wiggles, an hourglass flips half a turn, a stopwatch or sync icon spins once. Use it on navigation items and toolbar buttons, at most one per tap, never on a loop.

- Web: `.ex-wiggle`, `.ex-flip` (`spatial-fast`), `.ex-spin-once` (`spatial-default`).
- Compose: `Modifier.iconMotion(trigger = tapCount, motion = IconMotion.Wiggle)`.

### List placement

When rows are added, removed or reordered, the other rows slide to their new places on `spatial-default` instead of jumping. New rows fade and scale in from 0.96; rows entering together are `stagger-list` apart (cap at six). When a new row is added at the end of a long list, scroll it into view with the same spring.

- Web: `.ex-enter` with `style="--i: 3"` for the stagger index; animate reorders with FLIP (measure, invert, then transition `transform` with `var(--motion-spatial-default)`).
- Compose: `Modifier.animateItem(placementSpec = MaterialTheme.motionScheme.defaultSpatialSpec())` on each `LazyColumn` item; `listState.animateScrollToItem(index)`.

### Swipe to reveal and delete

Swipe a row toward the start to reveal one action on `error`; swipe past about 55% or fling fast to delete. The row follows the finger exactly, then settles with the drag's velocity. A haptic tick marks the moment a release would delete. Remove the item only after the row has left, so the rows below make one smooth placement move. The first time someone adds a row, slide it open and closed once to teach the gesture.

- Compose: `SwipeToRevealRow(onDelete = …, showHint = isFirstItem) { Row… }`, or Material 3 `SwipeToDismissBox` when no partial reveal is needed.
- Always offer the same action somewhere visible (a menu, selection mode); swiping is a shortcut, not the only way.

### Selection mode

A long press on a row enters selection mode: haptic `LongPress`, the row's container turns `primary-container`, a check appears in its leading shape (morph the avatar), and the top bar becomes "3 selected" with Delete and Close. Taps then toggle rows; Back or Close leaves the mode. Use a `FloatingToolbar` for the bulk actions on phones.

### Predictive back

On Android 14+, a full-screen panel (settings, a detail view) follows the back gesture before it commits: it shrinks to about 90%, moves a little toward the gesture and rounds its corners. Releasing past the threshold closes it; cancelling springs it back on `spatial-fast`.

- Compose: `val p = rememberPredictiveBackProgress(enabled = open) { open = false }`, then `Modifier.predictiveBack(p.value)` on the panel. Add `android:enableOnBackInvokedCallback="true"` to the manifest.

### Shape morph

Library shapes can morph into each other: a circle becomes a cookie when selected, a pebble becomes a flower when a task is done, a loading shape cycles. Morph on `spatial-default`; one morph per moment.

- Web: change `ShapeAvatar`'s `shape` prop and it morphs; `ShapeAvatar.morph(a, b, k)` gives the in-between path.
- Compose: `val morph = remember { Morph(MaterialShapes.Circle, MaterialShapes.Cookie9Sided) }`, animate a progress float with `defaultSpatialSpec()`, and draw `morph.toPath(progress)` (or use the `toShape()` helpers in material3 1.4).

### Haptics

Pair touch feedback with the motion it confirms. Use the semantic kinds, not raw constants.

| Moment | Kind | Android constant | Web (`Expressive.motion.haptic`) |
| --- | --- | --- | --- |
| A dial or drum passes a step | `tick` | `CLOCK_TICK` | 4ms |
| A keypad digit, a segment change | `tap` | `KEYBOARD_TAP` | 8ms |
| Saved, reset, dismissed | `confirm` | `CONFIRM` (API 30+) | short double pulse |
| Refused, invalid | `reject` | `REJECT` (API 30+) | two firm pulses |
| Entering selection mode, drag to reorder | `longPress` | `LONG_PRESS` | 18ms |
| A timer or stopwatch starts | `start` | `GESTURE_START` (API 30+) | 12ms |
| It stops or pauses | `stop` | `GESTURE_END` (API 30+) | soft double pulse |

Compose: `val haptic = rememberHaptics(); haptic(ExpressiveHaptic.Tick)`. On the web vibration only works on Android browsers; it's skipped under reduced motion.

### Ambient loops

Something on screen may move continuously only when it represents something live: the selected marker on a map breathes, a ringing alarm wiggles every few seconds, a recording dot pulses. One per screen at most, slow (2 seconds or more), small, and never behind text. Stop it entirely under reduced motion.

- Web: `.ex-breathe`.
- Compose: `val b = rememberBreathing()` and scale or fade with it.

### Animated splash

The launch animation is the app icon assembling itself in under a second: the container pops in with a slight overshoot, then the inner parts (the hands of a clock, the play triangle) rotate or slide into place, then a small detail pops last. Use an animated vector drawable on Android 12+ (`windowSplashScreenAnimatedIcon`), keep it under 1000ms, and never block the app on it.

## Choreography checklist

- [ ] Each transition has one hero moving on a spatial spring; the rest fades.
- [ ] Springs come from the tokens or `MaterialTheme.motionScheme`, not hand-tuned numbers.
- [ ] Gestures hand their velocity to the settle spring and can be interrupted.
- [ ] Bounce appears on movement and celebrations only, never on colour.
- [ ] Haptics mark detents and outcomes, not every tap.
- [ ] Reduced motion: no movement, bounce, rotation or loops; short fades remain.
