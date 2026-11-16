# Working in an existing project

Expressive Kit is a complete design system, but most requests come from an app that already has a theme, components and conventions. Bring M3E's behaviour into that app. Don't replace the app with the kit.

## 1. Look before you change anything

Before editing, find out:

- **Platform and UI toolkit:** Jetpack Compose, Android Views (Material Components for Android), Flutter, a web framework, React Native or SwiftUI. See `docs/platforms.md` for what each can do.
- **Material version.** In Compose, check the `androidx.compose.material3` version or the Compose BOM in `libs.versions.toml` or `build.gradle(.kts)`. The expressive APIs (`MaterialExpressiveTheme`, `MotionScheme`, `ButtonGroup`, `LoadingIndicator`, wavy progress, `FloatingToolbar`, `MaterialShapes`) need 1.4 or later, and many are marked `@ExperimentalMaterial3ExpressiveApi`. On the web, check whether the app uses a Material library, Tailwind, CSS Modules or plain CSS.
- **Existing theme:** colour scheme (brand or dynamic), typography and fonts, shapes, spacing constants and any design tokens.
- **Shared components:** buttons, cards, list rows and app bars the app already wraps. Change the wrapper once rather than every call site.
- **Conventions:** state management, navigation library, file layout, naming, lint and format rules, tests, screenshot tests.
- **Constraints:** minimum SDK or browser support, brand guidelines, accessibility requirements, performance budgets.

## 2. Pick the right mode

| Situation | Mode | What you change |
| --- | --- | --- |
| New app or a prototype, no design system | **Adopt the kit** | Use the kit's tokens, components, `ExpressiveTheme`, fonts and screen patterns as described in `SKILL.md` |
| Existing Material 3 app | **Map onto their theme** | Keep their colour scheme, fonts and shapes. Add M3E behaviour (shape morphing, springs, emphasized type, new components) using their tokens |
| Existing app with its own non-Material design system | **Borrow behaviours only** | Bring over only the behaviours that fit: springs, grouped shapes, a single hero, containment by tone. Don't introduce Material components or the kit's palette |
| A review or audit | **Review** | Change nothing; report findings with `docs/review.md` |

If you can't tell which mode applies and it changes the outcome (for example, replacing the brand palette), ask. Otherwise choose the least disruptive mode and say which one you used.

## 3. Rules for an existing codebase

- **Don't replace the brand.** Keep their seed colour, palette, fonts and logo. The kit's Fraunces display face, `highlight` role and warm dark theme are Expressive Kit brand choices, not M3E requirements.
- **Don't upgrade dependencies as a side effect.** If an expressive API needs a newer `material3` than the project uses, say so, show the change, and get agreement before bumping the version or the BOM. Until then, build the behaviour with what's there (see the fallbacks below).
- **Don't swap libraries or migrate frameworks** (Views to Compose, one CSS approach to another) as part of design work. That's a separate project.
- **Use their tokens.** Map each kit token to the nearest role in their theme (table below). Add a missing role to their theme where everything can reach it, never as a hex value inside a screen.
- **Mark experimental APIs.** Put `@OptIn(ExperimentalMaterial3ExpressiveApi::class)` as narrowly as possible (a function, not the module) and mention it in the handoff.
- **Keep the diff small.** Touch the screens and shared components in scope. Leave unrelated code, formatting and files alone.
- **Run their checks:** formatter, lint, unit tests, screenshot tests, build. Report only the checks you actually ran.

## 4. Mapping kit tokens to a Material 3 theme

| Kit token | Compose `MaterialTheme` | Notes |
| --- | --- | --- |
| `primary`, `on-primary`, `*-container`, `surface-container-*`, `outline`, `inverse-*` | `colorScheme.<same role>` | Same Material roles; use theirs directly |
| `highlight` / `on-highlight` | No Material equivalent | Use `tertiaryContainer`, or add a custom role through a `CompositionLocal` |
| `positive` | No Material equivalent | Add an extended colour (`CompositionLocal` or a theme extension); keep `error` for losses |
| Type styles (`display-large` … `label-small`) | `typography.<style>` | Same 15 styles |
| `*-emphasized` | `typography.<style>Emphasized` (1.4+) | Before 1.4: `style.copy(fontWeight = FontWeight.Bold)` |
| `numeral-*`, `data-*`, `eyebrow` | No Material equivalent | Define them in their theme extension, using their font with tabular numerals (`fontFeatureSettings = "tnum"`) |
| `shape-xs` … `shape-xl` | `shapes.extraSmall` … `shapes.extraLarge` | Kit's `shape-lg-increased`, `shape-xl-increased`, `shape-xxl` exist only in 1.4+ (`largeIncreased`, `extraLargeIncreased`, `extraExtraLarge`) |
| `shape-full` | `CircleShape` or `RoundedCornerShape(50)` | |
| `space-*` | Their spacing constants, if any | Otherwise use dp values on the same 4dp grid |
| Motion tokens | `MaterialTheme.motionScheme` (1.4+) | Before 1.4: `spring(dampingRatio, stiffness)` with the values from the motion table in `SKILL.md` |

On the web, map the kit's CSS variable names onto the app's own variables (`--primary: var(--brand-primary)`) instead of loading `tokens/tokens.css` on top of their styles.

## 5. Fallbacks when expressive APIs aren't available

| Behaviour | Without the expressive API |
| --- | --- |
| Shape morph on press | Animate the corner size with `animateDpAsState` and a spring, driven by `interactionSource.collectIsPressedAsState()`; on the web, transition `border-radius` with the motion token |
| Connected button group | A `Row` of toggle buttons 2dp apart, each with per-position `RoundedCornerShape` (large outer corners, small inner ones) |
| `MotionScheme.expressive()` | `spring(dampingRatio = 0.8f, stiffness = 380f)` and the other values from `SKILL.md`; effects springs use a damping ratio of 1 |
| Wavy progress | Standard `LinearProgressIndicator`; or draw the wave on a `Canvas` |
| `LoadingIndicator` | `CircularProgressIndicator` |
| `MaterialShapes` and morphing | The `androidx.graphics:graphics-shapes` library (`RoundedPolygon`, `Morph`) works without material3 1.4 |
| Emphasized type | A heavier weight of the same style |
| Floating toolbar | A `Surface` with `shape = CircleShape` and elevation, placed in a `Box` over the content |

## 6. Handoff

Finish with the handoff template in `templates/implementation-handoff.md`: the mode you used, what changed, any experimental APIs or version requirements, the checks you actually ran, and what's left.
