# Platforms

M3 Expressive is a design language. Only some toolkits ship its components. This kit gives you a full implementation for **the web** (`components/bundle.js`) and **Jetpack Compose** (`android/`). On other platforms, use the tokens and behaviours and say clearly what's built by hand.

Never claim full M3E parity on a platform without checking its current release notes and API reference. Library support changes quickly; the notes below are a starting point, not a guarantee.

## Support at a glance

| Platform | Native M3E components | Springs | Shape library and morph | How to use this kit |
| --- | --- | --- | --- | --- |
| Jetpack Compose | Yes, in `androidx.compose.material3` 1.4+ (many still experimental) | `MotionScheme.expressive()` | `MaterialShapes` + `Morph` | `android/ExpressiveTheme.kt` and helpers |
| Web (React or HTML) | Not from Google; this kit's bundle provides them | Kit's `--motion-*` tokens (CSS `linear()` springs) and `Expressive.motion.animate` | `ShapeAvatar` | `tokens/tokens.css` + `components/bundle.*` |
| Android Views (MDC) | Partial; check Material Components for Android release notes | `SpringAnimation` (AndroidX DynamicAnimation) | `androidx.graphics:graphics-shapes` | Map tokens into XML themes |
| Wear OS | Wear Compose Material 3 has its own expressive components | Wear's motion scheme | Wear Compose shapes | Follow Wear guidance; don't port phone layouts |
| Flutter | Material 3 is the default; expressive components aren't in the core library at the time of writing | `SpringSimulation` + `SpringDescription.withDampingRatio` | Custom painter or a package | Map tokens into `ThemeData` and `ColorScheme` |
| React Native | No; React Native Paper implements Material 3, not M3E | Reanimated `withSpring` | `react-native-svg` paths from `ShapeAvatar.path()` | Map tokens into the theme |
| SwiftUI | No; use iOS-native controls where users expect them | `Spring` / `.interpolatingSpring` | `Shape` from SVG paths | Borrow tokens and behaviours sparingly |

## Converting the springs

The kit's springs are a damping ratio (ζ) and a stiffness (k), with a mass of 1. Some toolkits want a damping coefficient (c = ζ · 2√k) or a response time (2π / √k) instead:

| Token | ζ | k | Damping coefficient c | SwiftUI response (s) |
| --- | --- | --- | --- | --- |
| spatial fast | 0.6 | 800 | 33.9 | 0.222 |
| spatial default | 0.8 | 380 | 31.2 | 0.322 |
| spatial slow | 0.8 | 200 | 22.6 | 0.444 |
| effects fast | 1.0 | 3800 | 123.3 | 0.102 |
| effects default | 1.0 | 1600 | 80.0 | 0.157 |
| effects slow | 1.0 | 800 | 56.6 | 0.222 |

- **Compose:** `spring(dampingRatio = 0.8f, stiffness = 380f)`, or simply `MaterialTheme.motionScheme.defaultSpatialSpec()`.
- **Views:** `SpringForce().setDampingRatio(0.8f).setStiffness(380f)`.
- **Flutter:** `SpringDescription.withDampingRatio(mass: 1, stiffness: 380, ratio: 0.8)` driving a `SpringSimulation`.
- **React Native (Reanimated):** `withSpring(to, { mass: 1, stiffness: 380, damping: 31.2 })`.
- **SwiftUI:** `.spring(response: 0.322, dampingFraction: 0.8)` or `.interpolatingSpring(mass: 1, stiffness: 380, damping: 31.2)`.
- **Web:** use the `--motion-*` variables; they already contain the spring curve.

These values match Compose's expressive and standard motion schemes. Read the current `MotionScheme` source before treating them as the definitive Material values.

## Jetpack Compose

- Wrap the app in `ExpressiveTheme` (new apps) or map onto the existing theme (see `docs/existing-projects.md`).
- Check the `material3` version before using `ButtonGroup`, `SplitButtonLayout`, `FloatingToolbar`, `LoadingIndicator`, wavy progress, `MaterialShapes`, `MotionScheme` or the emphasized styles. Use the fallbacks in `docs/existing-projects.md` when they're missing.
- Go edge to edge with `enableEdgeToEdge()` and pad content with `WindowInsets`. Support predictive back (`PredictiveBackHandler`).
- Use `currentWindowAdaptiveInfo()` (the `material3-adaptive` library) for window size classes, and `NavigationSuiteScaffold` and `ListDetailPaneScaffold` where they fit, rather than measuring the screen.

## Web

- Use semantic HTML: real `<button>`, `<a>`, `<input>` and `<dialog>` elements. The kit's components already do this.
- Load `tokens/tokens.css`, then `components/bundle.css` and `components/bundle.js` (React 18), as described in `SKILL.md`.
- The CSS `linear()` spring curves need a recent browser. The tokens include a `cubic-bezier` fallback.
- Use container queries or media queries on the kit's window classes (600, 840, 1200px) for adaptive layouts.
- Support `prefers-reduced-motion`, `prefers-color-scheme`, `prefers-contrast` and `forced-colors`; see `docs/accessibility.md`.
- Google's own Material Web library (`@material/web`) is in maintenance mode and doesn't include the expressive components. Don't mix it with this kit in one screen.

## Android Views

- Use Material Components for Android themes (`Theme.Material3.*`) and map kit tokens to theme attributes (`colorPrimary`, `colorSurfaceContainerHigh`, `textAppearanceTitleLarge`, `shapeAppearanceCornerExtraLarge`).
- Recent MDC releases have started adding some expressive components and shapes. Check the release notes for the exact version in the project before using them.
- Build shape morphs with `androidx.graphics:graphics-shapes` and springs with `SpringAnimation`.
- Don't call Compose APIs from Views code, and don't start a Compose migration as part of design work.

## Wear OS

- Use `androidx.wear.compose:compose-material3`, not the phone `material3` library. It has its own expressive components (edge-hugging buttons, curved text, transforming lists) built for round screens.
- Design for glances: one hero value, one or two actions, large type, short sessions.
- Don't port phone screen patterns. Use Wear's list and pager patterns instead.

## Flutter

- Material 3 is on by default in current Flutter (`useMaterial3: true`). Build a `ColorScheme` from the kit's colour roles (or `ColorScheme.fromSeed` with the seed from `docs/seed-palettes.md`) and a `TextTheme` from the type scale.
- At the time of writing, the core Material library doesn't include M3E components such as button groups, wavy progress or the loading indicator. Build them as custom widgets with the kit's tokens, and give them proper `Semantics`.
- Use `SpringSimulation` for spatial springs and `AnimatedContainer` or `TweenAnimationBuilder` with a matching curve for effects.
- Don't copy Compose parameter names into Dart; follow Flutter conventions.

## React Native

- Map the kit's colour, type and shape tokens into the app's theme (React Native Paper's `MD3` theme works as a base).
- Use Reanimated `withSpring` with the converted values above, and respect `AccessibilityInfo.isReduceMotionEnabled()`.
- Draw library shapes with `react-native-svg` using `ShapeAvatar.path(name)` output.
- Check Android and iOS separately. iOS users expect iOS navigation and sheet behaviour.

## SwiftUI and iOS

- Prefer iOS controls, navigation and sheets where users expect them. Adopting Android conventions on iOS hurts usability.
- You can still borrow tokens (palette, type scale, shape scale) and behaviours (springs, a single hero, rolling digits, grouped shapes).
- Convert springs with the table above. Respect Reduce Motion (`@Environment(\.accessibilityReduceMotion)`) and Dynamic Type.

## Writing down what's supported

When a task covers more than one platform, include a small table in the handoff:

| Feature | Platform | Native or built by hand | Visible difference |
| --- | --- | --- | --- |
| Connected button group | Flutter | Built by hand | None |
| Loading indicator | Web | Kit component | Morph is CSS-only; no shape rotation under reduced motion |

## Sources and version checks

Check these before relying on a version-specific API. Last reviewed: 2026-11.

- Material Design 3 and M3 Expressive guidance: [m3.material.io](https://m3.material.io/)
- Material 3 in Compose: [developer.android.com/develop/ui/compose/designsystems/material3](https://developer.android.com/develop/ui/compose/designsystems/material3)
- Compose Material 3 release notes: [developer.android.com/jetpack/androidx/releases/compose-material3](https://developer.android.com/jetpack/androidx/releases/compose-material3)
- Compose Material 3 API reference (including `MotionScheme`): [developer.android.com/reference/kotlin/androidx/compose/material3/package-summary](https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary)
- Adaptive layouts and window size classes: [developer.android.com/develop/ui/compose/layouts/adaptive](https://developer.android.com/develop/ui/compose/layouts/adaptive)
- Material Components for Android releases: [github.com/material-components/material-components-android/releases](https://github.com/material-components/material-components-android/releases)
- Wear Compose Material 3: [developer.android.com/jetpack/androidx/releases/wear-compose](https://developer.android.com/jetpack/androidx/releases/wear-compose)
- Android accessibility: [developer.android.com/guide/topics/ui/accessibility](https://developer.android.com/guide/topics/ui/accessibility)
- WCAG 2.2: [w3.org/TR/WCAG22](https://www.w3.org/TR/WCAG22/)
- Agent Skills format: [agentskills.io/specification](https://agentskills.io/specification)

How to check:

1. Read the version the project actually uses.
2. Open that library's release notes and API reference.
3. Note whether the API is stable, experimental or deprecated, and its minimum SDK.
4. In the handoff, state the version you checked.
