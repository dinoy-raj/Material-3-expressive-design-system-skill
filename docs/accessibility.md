# Accessibility and internationalization

An expressive screen that can't be read aloud, scaled, translated or used without a gesture isn't finished. Treat everything here as part of the design, not polish for later. These rules sit on top of the contrast rules already in `SKILL.md` (every `on-*` pair meets 4.5:1).

## Targets and input

| Rule | Android (Compose) | Web |
| --- | --- | --- |
| Minimum touch target | 48 × 48dp, even if the visible control is smaller (`Modifier.minimumInteractiveComponentSize()`; Material components do this already) | WCAG 2.2 SC 2.5.8 asks for at least 24 × 24 CSS px, or enough spacing around smaller targets. Keep the kit's 48px for touch-first layouts |
| Spacing between targets | 8dp between separate targets. Connected button groups keep their 2dp gaps, but each segment still meets the minimum size | Same |
| Keyboard | Arrow keys move inside radio groups and sliders; Tab moves between groups | Every control reachable with Tab, activated with Enter or Space, with a visible focus ring (`:focus-visible`, `--focus` token) |
| Focus visibility | Focus indicators on custom components | WCAG 2.4.7 (focus visible) and 2.4.11 (focus not hidden behind sticky bars, sheets or the floating toolbar) |

### Every gesture needs a plain alternative

WCAG 2.2 SC 2.5.7 says anything done by dragging must also work with a single tap or click. Several M3E patterns in this kit use gestures, so give each one a fallback:

| Gesture in this kit | Alternative to provide |
| --- | --- |
| Swipe-up confirm handle (screen pattern 5) | Make the handle a button too. A tap, or Enter or Space, opens a confirm step or fires after a short hold with visible progress. Screen readers get a single "Confirm" action |
| Swipe to reveal and delete | A visible overflow menu or delete action on the row, plus a custom accessibility action (`CustomAccessibilityAction` in Compose, a menu button on the web). Always offer Undo |
| Rotary dial drag or fling | Tap the step arrows or the value; arrow keys and Page Up/Down step on the web; Compose exposes `setProgress` semantics so TalkBack can adjust it |
| Time picker dial drag | The HH:MM fields accept typed input (`TimeInput` in Compose); the keyboard icon switches modes |
| Slider drag | Tapping the track jumps the value; arrow keys step it; the value is announced |
| Predictive back gesture | The back button in the top bar stays visible on full-screen panels |
| Long press to enter selection mode | A visible "Select" action in the top bar or overflow menu |

## Screen readers (TalkBack, VoiceOver, NVDA)

- **Name every icon-only control.** `contentDescription` in Compose, `aria-label` on the web. The kit's `IconButton`, `Fab` and `Switch` take a `label` prop for this. Decorative icons and shapes get `contentDescription = null` or `aria-hidden="true"`.
- **Expose state, not just looks.** A shape morph or colour change means nothing to a screen reader. Set `selected`, `stateDescription` and `toggleableState` in Compose, and `aria-pressed`, `aria-checked`, `aria-current` or `aria-expanded` on the web. Connected button groups are radio groups (`role="radiogroup"` with `role="radio"` children, as `ButtonGroup` already renders).
- **Merge rows.** A list row with an avatar, headline, supporting line and trailing value is read as one item (`Modifier.semantics(mergeDescendants = true)` or `clickable` on the whole row; one focusable element on the web).
- **Changing numbers.** A `DigitRoll` animates its digits, but assistive tech should hear the final value once. Put `aria-hidden` on the animated cells and give the container a text alternative. Announce live readouts (timers) no more than once every few seconds, never every tick (`liveRegion = LiveRegionMode.Polite` or `aria-live="polite"`).
- **Charts and progress.** Give a one-sentence summary ("Up 12% this month, high of $48 on Oct 3") and, for wavy or circular progress, a value (`progressBarRangeInfo` in Compose, `role="progressbar"` with `aria-valuenow`). Waves are decoration; the number is the content.
- **Reading order follows visual order.** Hero first, then content, then actions. Don't make the large hero number a heading unless it names the screen.
- **Announce outcomes.** A snackbar or celebration must also be announced (`LiveRegionMode.Polite`, `role="status"`). Celebrations must still make sense with motion turned off.

## Text scaling and zoom

- Android scales fonts up to 200% (Android 14+, non-linear above 100%). Browsers zoom to 200% and reflow at a 320 CSS px wide viewport (WCAG 1.4.4 and 1.4.10).
- **Use `sp` for text in Compose** and `rem` on the web, so the kit's type tokens scale. Never put fixed heights on anything that holds text: buttons, chips, list rows and nav labels grow vertically.
- **Hero numbers.** `numeral-large` and stacked `DigitRoll` readouts can overflow at large scales. Let them shrink to fit their width (keep them at least `display-small`) rather than clip or wrap mid-number.
- **Navigation bar labels** may wrap or truncate at large scales. Keep labels short (one word) rather than hiding them.
- Test with the largest font size plus display size, in both a compact and an expanded window.

## Colour and contrast beyond text

- Non-text contrast (WCAG 1.4.11): control borders, slider tracks, the switch track, focus rings and chart lines need 3:1 against what's next to them. `outline` on `surface` and `primary` on `surface-container-highest` meet this in the kit's palettes. Check them again when you change the seed.
- Disabled controls (38% opacity) are exempt but must still look disabled, not invisible.
- Dynamic colour can produce any palette. Don't rely on a particular hue meaning something; keep icons and labels on `positive` and `error` states.
- Respect `prefers-contrast: more` and `forced-colors: active` on the web. In forced colours, borders replace tonal fills, so give containers a transparent 1px border that becomes visible.

## Right-to-left layouts

M3E layouts mirror in Arabic, Hebrew, Persian and Urdu. Compose mirrors automatically through `LocalLayoutDirection`. On the web, set `dir="rtl"` on `<html>` and use logical properties.

- **Use start and end, never left and right.** In Compose use `padding(start = …)` and `Arrangement.Start`. In CSS use `margin-inline-start`, `padding-inline`, `inset-inline-end` and `text-align: start`. The kit's `bundle.css` still has some physical `left` and `right` values, so check mirrored screens visually.
- **Mirror directional icons:** back and forward arrows, chevrons, send, reply, undo and redo, list bullets, and the split-button chevron's position. In Compose use `Icons.AutoMirrored.*`. On the web, flip with `transform: scaleX(-1)` under `[dir="rtl"]`.
- **Don't mirror** clocks and the time picker dial (they run clockwise everywhere), media playback controls, checkmarks, logos, charts' time axes in most locales (follow the product's locale research), or the digits inside numbers.
- **Motion follows reading direction.** Pushed screens slide in from the end edge. Swipe to delete swipes toward the start edge. The `DigitRoll` up and down direction doesn't change, but its right-to-left stagger becomes left-to-right in RTL so it still starts at the last digit.
- **The FAB and the floating toolbar** sit at the bottom end corner (bottom-left in RTL). The navigation rail sits at the start edge.
- Test with real translated strings, not mirrored English. Check mixed text such as English product names, phone numbers and URLs inside Arabic sentences.

## Localization

- **Format with the locale**, never by hand: `Intl.NumberFormat`, `Intl.DateTimeFormat` and `Intl.RelativeTimeFormat` on the web; `NumberFormat`, `DateTimeFormatter` and `android.icu` on Android. That covers currency position, decimal separators, digit systems (Arabic-Indic digits), 12- or 24-hour time (the time picker follows `DateFormat.is24HourFormat`) and units.
- **Leave room for longer text.** German and Finnish can run 30–40% longer than English. Buttons stay pills but grow. Connected button groups with long labels switch to a scrolling chip row or a menu rather than truncating.
- **Don't concatenate sentences.** "Buy *$100.00* of ACRN" is one translatable string with placeholders. Mark the emphasized span inside the string (an annotated string or markup), not by joining three fragments.
- **Uppercase eyebrows.** Uppercasing doesn't exist in many scripts and breaks some (Turkish dotted i, German ß). Apply it with `text-transform` or a locale-aware `uppercase(locale)`, never in the source string, and drop the letter-spacing for scripts without case.
- **Display face fallback.** Fraunces and Google Sans Flex cover Latin, Greek and Cyrillic only. Set a fallback stack with a face for each supported script (Noto Sans Arabic, Noto Sans JP and so on). Italic emphasis doesn't exist in Arabic or CJK, so use weight (`*-emphasized`) or colour instead.
- Name languages in their own language ("Deutsch", "العربية"); don't use flags for them.

## Motion, sound and haptics

- Reduced motion is covered in `docs/motion.md`. Remember that a celebration under reduced motion still needs its static outcome state (status badge, sentence, summary).
- No flashing more than three times a second (WCAG 2.3.1). Ambient loops stay slow and small.
- Haptics and sound only confirm what's already visible. Never make them the only feedback.

## Checklist

- [ ] Every interactive element is at least 48dp (touch) or 24px with spacing (web pointer), with a visible focus state.
- [ ] Every gesture (swipe confirm, swipe delete, dial, slider, long press) has a tap or keyboard alternative.
- [ ] Icon-only controls have names; state is exposed (selected, checked, expanded), not only shown by shape or colour.
- [ ] Rolling numbers, charts and progress expose their value as text once.
- [ ] 200% font scale and 200% zoom: nothing clips or overlaps; hero numbers fit.
- [ ] Non-text elements (borders, tracks, focus rings) meet 3:1.
- [ ] RTL: layout mirrors, directional icons mirror, clocks and media don't; tested with real strings.
- [ ] Numbers, currency, dates and times use locale formatting; strings aren't concatenated.
- [ ] Fonts fall back properly for every supported script; italic emphasis has a non-Latin alternative.
- [ ] With reduced motion, outcomes are still clear without the animation.
