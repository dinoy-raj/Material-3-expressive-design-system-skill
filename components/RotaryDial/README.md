# RotaryDial

A drum you turn to set a value: timer length, temperature, zoom, a pomodoro.

**Provide:** `value` + `onChange` (or `defaultValue`), `min`, `max`, optional `step` (1), `majorEvery` (5), `label`, `format`, `height` (76), `haptics={false}`.

- The drum is drawn in perspective: graduations sit at equal angles around a cylinder, so they bunch toward the edges, and the ones near the centre are thicker and brighter. It uses the slider's anatomy: the drum is the track on `surface-container-highest`, and the graduation under the centre turns `primary` and acts as the handle.
- Drag or fling sideways. On release it carries on with your fling and snaps to the nearest step on the `spatial-fast` spring, so a flick feels physical.
- It ticks a haptic each time a step passes the centre. It never yanks the drum back to a whole number while you drag; only an outside change re-seats it.
- Show the value large above the drum, like the slider head. Keyboard: arrows step, Page Up/Down jump `majorEvery`, Home/End go to the limits.
- Prefer a `Slider` for plain settings; use a rotary dial when the thing being set feels like a physical control.

**Compose:** `RotaryDial` in `android/ExpressiveComponents.kt`.
