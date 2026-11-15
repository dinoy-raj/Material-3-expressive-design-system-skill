# TimePickerDial

Pick a time on a circular dial: hour first, then minutes, with large tappable fields above.

**Provide:** `hour` (0–23) and `minute` with `onChange({hour, minute})`, or `defaultHour` / `defaultMinute`; `is24h` for a two-ring 24-hour dial; optional `defaultMode` (`hour` or `minute`), `label`, `haptics={false}`.

- The handle springs to a tapped number on `spatial-fast` and follows the finger exactly while dragging. It always takes the short way round (11 to 12 turns forward).
- Lifting your finger on an hour moves straight to minutes. Minutes snap to 1; a dot in the handle marks minutes between the labelled fives.
- 12-hour: AM/PM is a vertical connected toggle. 24-hour: the outer ring is 12 and 1–11, the inner ring is 00 and 13–23.
- The active field is `primary-container` with larger corners; the other sits on `surface-container-highest`.
- Each step ticks a light haptic where the browser supports it. The dial is a keyboard slider (arrow keys step by one).
- Use it in a bottom sheet or dialog with Cancel and OK below. Offer a keyboard entry mode for accessibility.

**Compose:** use Material 3 `TimePicker(state)` (or `TimeInput`) inside the expressive theme; `TimeDial` in `android/ExpressiveComponents.kt` shows a custom dial with haptic ticks.
