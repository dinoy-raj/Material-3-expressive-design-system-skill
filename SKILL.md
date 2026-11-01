---
name: material-3-expressive
description: Design and build Material 3 Expressive (M3E) apps and screens with the Expressive Kit design system. Use when asked to design, mock up, review or code UI in the Material 3 Expressive style for Android (Jetpack Compose), the web (React/HTML/CSS) or a design tool. Covers M3E tokens (colour roles, type scale, shape scale, spacing), the shape library and shape morphing, spring-based motion, component patterns (button groups, split buttons, FABs, floating toolbars, navigation bar and rail, wavy progress, loading indicator, sliders, cards, lists, sheets) and eight ready-made screen patterns.
---

# Material 3 Expressive design skill

This skill teaches you to design screens in **Material 3 Expressive (M3E)**, Google's 2025 evolution of Material You, using the **Expressive Kit** design system in this repository. M3E keeps Material 3's colour roles and components and adds expressive shape, springy motion, bolder type and new components so interfaces feel more emotional and easier to scan.

Read this file first. Go deeper only when you need to:

| Need | Read |
| --- | --- |
| Exact token values (colours per theme, type, spacing, radii) | `tokens/tokens.json` (source) or `tokens/tokens.css` |
| Brand rules: voice, colour, type, layout, motion, icons | `docs/brand-book.md` |
| Full screen recipes | `docs/screen-patterns.md` |
| A different product colour | `docs/seed-palettes.md` |
| One component's props and do's and don'ts | `components/<Name>/README.md` and `components/index.d.ts` |
| Android Compose theme | `android/ExpressiveTheme.kt` |

## How to work

1. **Pick the platform.** Web: load `tokens/tokens.css` and `components/bundle.css`, then React 18 and `components/bundle.js` (`window.Expressive`). Android: use `ExpressiveTheme` from `android/ExpressiveTheme.kt` and the Material 3 Compose components, with the mapping table below. A design tool: name styles after the tokens.
2. **Pick a screen pattern** from the list below before laying anything out.
3. **Use tokens, never raw values.** Colours come from roles (`primary`, `on-surface-variant`, `surface-container-high`), radii from the shape scale, spacing from `space-*`. If a value you need is missing, use the nearest token and say so.
4. **Apply the M3E behaviours** in this file: shape, motion, emphasis, containment.
5. **Check before you finish** with the checklist at the end.

## The seven M3 Expressive behaviours

### 1. Shape is expressive and it morphs

- **Corner scale:** `shape-none` 0, `shape-xs` 4, `shape-sm` 8, `shape-md` 12, `shape-lg` 16, `shape-lg-increased` 20, `shape-xl` 28, `shape-xl-increased` 32, `shape-xxl` 48, `shape-full` (pill).
- **Pressable things are round, containers are rounded rectangles.** Buttons, chips, segments, search bars, nav indicators and toolbars are `shape-full`. Cards, sheets and grouped lists are `shape-xl`.
- **Shape morph on press.** A pressed pill button tightens its corners (`shape-md` for small, `shape-lg` for medium, `shape-xl` for large) and springs back on release. Icon buttons and FABs do the same.
- **Shape morph on selection.** A selected segment in a connected button group becomes a full pill while its neighbours keep small inner corners. Selected toggle buttons switch between round and square; selected toolbar items become squircles.
- **Grouped shapes.** Items that belong together sit 2px apart (`space-0-5`) with large outer corners and small inner corners (`shape-sm` for buttons, `shape-xs` for list rows). This reads as one object with separately pressable parts.
- **The shape library.** Beyond rectangles, M3E has about 35 abstract shapes. This kit ships 11 as `ShapeAvatar`: `cookie4`, `cookie6`, `cookie9`, `cookie12`, `clover4`, `flower5`, `flower8`, `sunny`, `burst`, `pebble`, `circle`. Use them for avatars, hero-icon seats, scores and ratings, image masks and decorative blobs. Give each kind of thing one shape and keep it (tickers are always cookie9).
- **Shapes animate.** The loading indicator morphs between library shapes. Hero shapes may rotate slowly. Avatars may morph on selection.

### 2. Motion is physics-based

M3E replaces fixed durations and easing curves with **springs**. There are two kinds:

- **Spatial springs** move position, size, rotation and shape. They may overshoot (bounce).
- **Effects springs** change colour and opacity. They never overshoot.

Each kind comes in fast (small components), default (partial-screen) and slow (full-screen) speeds. The expressive scheme's values (Compose `MotionScheme.expressive()`):

| Token | Damping ratio | Stiffness | CSS approximation |
| --- | --- | --- | --- |
| spatial fast | 0.6 | 800 | `350ms cubic-bezier(0.34, 1.56, 0.64, 1)` |
| spatial default | 0.8 | 380 | `500ms cubic-bezier(0.34, 1.4, 0.64, 1)` |
| spatial slow | 0.8 | 200 | `650ms cubic-bezier(0.34, 1.3, 0.64, 1)` |
| effects fast | 1.0 | 3800 | `150ms cubic-bezier(0.2, 0, 0, 1)` |
| effects default | 1.0 | 1600 | `200ms cubic-bezier(0.2, 0, 0, 1)` |
| effects slow | 1.0 | 800 | `300ms cubic-bezier(0.2, 0, 0, 1)` |

The standard scheme (`MotionScheme.standard()`) uses damping 0.9 with no visible bounce. Use it for productivity and utility apps, and the expressive scheme for consumer and playful apps.

Rules:
- Interruptible: a new gesture retargets the spring from its current position and velocity; it never restarts.
- Choreograph one moment per transition: the hero element moves with a spatial spring while content fades with an effects spring.
- Celebrate outcomes once (stars pop in sequence, a shape spins behind a mascot), never on routine actions.
- With `prefers-reduced-motion` (or Android's "Remove animations"), drop movement, bounce and rotation and keep simple fades.

### 3. Emphasis through type and colour

- One hero per screen: a balance, a countdown, a score or a cover. Set it in `numeral-large` (56/60, weight 700, tabular numerals) or `display-small` (36/44, display face) with `space-12` of air.
- The **emphasized** type styles are heavier weights of the base scale. This kit's headlines and titles are 600 to 700 and labels 600, so key text stands out at a glance.
- Pair a characterful display face (Fraunces by default) with Google Sans Flex for UI and Google Sans Code for data. Use one display face per screen at most.
- Emphasise a single word in a display headline with italic `primary`: "Buy *$100.00* of ACRN".
- Use an uppercase mono `eyebrow` above titles and list groups: `REVIEW · MARKET ORDER`, `TODAY`.

### 4. Containment and tone, not lines

- Separate content with surface tones: `surface` (page) → `surface-container-low` (grouped content) → `surface-container` (nav bar) → `surface-container-high` (fills of search bars, segments and tiles) → `surface-container-highest` (tracks).
- Use tonal containers to make a card a hero: `primary-container`, `secondary-container` and `tertiary-container`, each with its `on-*` text colour. A hub may stack three tonal cards, each a different container.
- No dividers between list rows. No coloured stripe on one edge of a card. Use elevation only for floating things (FABs, toolbars, menus).

### 5. Colour roles

- `primary` / `on-primary`: the main action, the selected segment, active slider and progress.
- `secondary`: the second voice (settings selections, a second chart series). `tertiary`: playful accents.
- `highlight` / `on-highlight`: one loud fill per screen (a large FAB, a streak). Never use it for text.
- `positive` and `error`: gain/success and loss/error. Always pair with an arrow or icon so meaning doesn't depend on hue alone.
- Every `on-*` pair meets 4.5:1 in both themes. The dark theme is a warm near-black with lighter accents and dark text on fills. Don't invert the light theme.
- Dynamic colour: on Android 12+ you may derive the scheme from the wallpaper, but keep brand moments (hero cards, illustrations) on the brand palette.

### 6. Adaptive layout

| Window class | Width | Navigation | Layout |
| --- | --- | --- | --- |
| Compact | < 600dp | Navigation bar (bottom) | One pane, 16dp gutters |
| Medium | 600–839dp | Navigation rail | One pane, or list and detail |
| Expanded | 840–1199dp | Navigation rail (expanded on demand) | List (≤ 420dp) and detail |
| Large / XL | ≥ 1200dp | Expanded navigation rail | Two or three panes, 24dp gutters |

Foldables: avoid placing content across the hinge; on unfolded posture, switch to list and detail.

### 7. Content voice

Second person, sentence case everywhere, warm and specific to the domain. Buttons are verbs that state what they spend: "Place order · $23.33". Supporting lines explain consequences plainly. Use the domain's real units (4.4 km, 16.7 MWh, 5.8¢/pt). No emoji in UI copy.

## Component patterns

Each entry gives the M3E behaviour, then this kit's component (web) and the Compose equivalent.

| Pattern | Behaviour | Web (`window.Expressive`) | Compose |
| --- | --- | --- | --- |
| Buttons | Five styles: filled (one per screen), tonal, outlined, text, elevated. Sizes XS to XL; the main action of a flow is medium (56dp) and full width. Corners morph on press. | `Button` (`variant`, `size`) | `Button`, `FilledTonalButton`, `OutlinedButton`, `TextButton`, `ElevatedButton` |
| Icon buttons | 48dp target; standard, filled, tonal and outlined; narrow, default and wide widths; toggles fill their icon when selected. | `IconButton` | `IconButton`, `FilledIconButton`, `FilledTonalIconButton`, `IconToggleButton` |
| Button groups | Standard groups space buttons apart. Connected groups join them with 2px gaps, and the selected option becomes a full pill. Use for 2–5 single-choice options such as time ranges, modes, sizes or tips. | `ButtonGroup` | `ButtonGroup`, connected `ToggleButton`s |
| Split button | A main action plus a menu trigger. The trailing half rounds fully and its chevron rotates when open. | `SplitButton` | `SplitButtonLayout` |
| FAB | One per screen, bottom-right above the nav bar; FAB, medium and large sizes; extended with a label; collapses on scroll. A FAB menu expands into a stack of related actions. | `Fab` | `FloatingActionButton`, `MediumFloatingActionButton`, `LargeFloatingActionButton`, `ExtendedFloatingActionButton`, `FloatingActionButtonMenu` |
| Floating toolbar | A pill of contextual actions floating above content, optionally beside a FAB; replaces the bottom app bar; hides on scroll. | `FloatingToolbar` | `HorizontalFloatingToolbar` |
| Navigation bar | 3–5 destinations; active item gets a pill indicator in `primary-container`, a filled icon and a bold label; labels always visible. | `NavigationBar` | `NavigationBar` / `ShortNavigationBar` |
| Navigation rail | Medium and larger windows; collapsed or expanded; same items as the bar, FAB at the top. | — | `NavigationRail` / `WideNavigationRail` |
| Top app bar | Large title block for top-level and detail screens; small bar with close for flows; optional subtitle. | `TopBar` | `LargeTopAppBar`, `MediumFlexibleTopAppBar`, `TopAppBar` |
| Search | Full-width pill on `surface-container-high`; expands to a full-screen search view. | `SearchBar` | `SearchBar` |
| Text fields | Outlined with the label in the border; filled inside sheets; errors say how to fix the problem. | `TextField` | `OutlinedTextField`, `TextField` |
| Chips | Filters (outlined, check when selected), suggestions (tonal), input. Filter rows scroll sideways. | `Chip` | `FilterChip`, `AssistChip`, `SuggestionChip`, `InputChip` |
| Switch | Applies immediately; thumb shows a check when on and grows while pressed. | `Switch` | `Switch` with a `thumbContent` icon |
| Slider | Thick 16dp track split by a bar handle with gaps, stop dot at the end, value shown large. | `Slider` | `Slider` |
| Progress | Wavy linear and circular indicators for goals and good news; flat for neutral quotas. | `WavyProgress` | `LinearWavyProgressIndicator`, `CircularWavyProgressIndicator` |
| Loading | Indeterminate waits under five seconds: a morphing, rotating shape, optionally contained. | `LoadingIndicator` | `LoadingIndicator`, `ContainedLoadingIndicator` |
| Cards | `shape-xl`; default on `surface-container-low`; tonal containers for hero content; whole card pressable with corner morph. | `Card` | `Card`, `ElevatedCard`, `OutlinedCard` |
| Lists | Rows of 56dp+ with a shape-avatar leading, headline, supporting line, mono meta and a trailing value; grouped by eyebrow headers, no dividers. | `ListItem` | `ListItem` |
| Grouped (segmented) lists | Settings rows stacked 2dp apart with big outer and small inner corners. | `GroupedList` | `Column` of `Surface`s with per-position shapes |
| Stats | 2–4 tiles of number and label; at most one strong tone. | `StatTile` | `Card` + text styles |
| Bottom sheet | Drag handle, `shape-xl` top corners, scrim, mono eyebrow + display title, primary action at the bottom. | `BottomSheet` | `ModalBottomSheet` |
| Receipt rows | Key/value rows, tabular numerals, total row last, "Free" in `positive`. | `SummaryList` | `Column` of `Row`s |
| Badges and value pills | Mono uppercase status with a dot (PENDING); tonal tags (Best, +30%); counts on icons; gain/loss pills with arrows. | `Badge`, `ValuePill` | `Badge`, `BadgedBox`, custom `Surface` |
| Snackbar | Past-tense confirmation on `inverse-surface`, one action, above the nav bar. | `Snackbar` | `Snackbar` |
| Shapes | Library shapes for avatars, seats and masks. | `ShapeAvatar` (`ShapeAvatar.path(name)` gives SVG paths) | `MaterialShapes.Cookie9Sided`, `Clover4Leaf`, `Sunny`, `SoftBurst`, `Flower`, `Pill`… via `toShape()` |

Compose notes: the expressive components and `MaterialExpressiveTheme` / `MotionScheme.expressive()` ship in `androidx.compose.material3` 1.4+ and may need `@OptIn(ExperimentalMaterial3ExpressiveApi::class)`. Check the version in the project before using them, and fall back to the standard component with the shape and motion rules above if they're missing.

## Screen patterns

Full recipes are in `docs/screen-patterns.md`. Choose one before laying out:

1. **Hub (home tab):** display greeting and a facts line → optional attention banner → one hero (big number with chart, or tonal "up next" card) → peeking carousel → owned items as list rows → nav bar (+ FAB).
2. **Tab list (Explore, Activity, Orders):** `headline-large` title → search bar or filter chips/button group → eyebrow-grouped list rows with shape avatars and trailing values.
3. **Detail:** back + actions → identity (shape avatar or hero image, title, mono meta) → hero value → chart with a range button group → position card with summary rows → about → bottom action pair (outlined + filled).
4. **Amount entry:** small bar with close → mode button groups → centred `numeral-large` amount with an ≈ conversion → quick-amount button group → 3×4 keypad → full-width primary.
5. **Review and confirm:** eyebrow + display sentence with the amount italic in `primary` → summary rows → plain-language footnote → deliberate confirm (swipe handle or large button).
6. **Outcome and celebration:** illustration or spinning shape → mono status badge → `display-large` sentence → stat tiles or summary → outlined secondary above filled "Done".
7. **Settings:** profile hero in a tonal card → grouped lists titled in `primary` with switches, button groups and value rows.
8. **Bottom-sheet capture:** scrim over the screen → sheet with mono eyebrow, display title, text fields, a choice row, destination chips, full-width primary.

## Do and don't

- **Do** make every pressable thing a pill or shape and every container a `shape-xl` card.
- **Do** keep one filled button and at most one `highlight` fill per screen.
- **Do** use library shapes for avatars and hero seats, consistently per entity type.
- **Do** design both light and dark themes, plus a compact and an expanded layout.
- **Don't** use dividers, drop shadows on cards, or a coloured border stripe on one edge of a card.
- **Don't** use more than one display face, or more than five colours in an illustration.
- **Don't** animate routine actions with bounce. Springs belong to spatial changes and celebrations.
- **Don't** hard-code hex values or radii; reference tokens.

## Final checklist

- [ ] The screen follows one of the eight patterns and has a single hero.
- [ ] All colours, radii, spacing and type come from tokens; light and dark both checked.
- [ ] Text meets 4.5:1 (3:1 for 24px+ text, icons and control borders); gain and loss carry arrows.
- [ ] Pressable elements are 48dp+ and morph on press; selections morph shape.
- [ ] Motion uses spatial springs for movement and effects springs for colour; reduced motion respected.
- [ ] Copy is sentence case, second person, verbs on buttons, real units.
- [ ] Compact and expanded layouts are both defined (bar ↔ rail, one pane ↔ list and detail).
