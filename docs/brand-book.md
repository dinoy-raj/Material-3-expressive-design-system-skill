# Brand book

Expressive Kit is a Material 3 Expressive system for Android-first apps, distilled from ten sample apps (100 screens, light and dark): Sherwood, Trill, Greenwave, Magpie, Prime Meridian, Shelfie, Dollop, Tern, Pinhole and Heliotrope. It keeps what those screens share — tonal surfaces, pill controls that morph when pressed, a shape library, one big number per screen — and gives you one default palette to start from. Swap the palette with a seed from **Seed palettes** to give each product its own voice.

## Principles

1. **One hero per screen.** Every screen leads with the single thing it exists to show: a balance, a countdown, a book cover, a route score. Set it in `numeral-large` or `display-small` with `space-12` of air around it. Everything else is quieter.
2. **Tone, not lines.** Separate content with surface tones (`surface` → `surface-container-low` → `surface-container-high`), never with dividers or borders. Use `outline-variant` hairlines only inside a summary list or a chart.
3. **Round things are pressable.** Buttons, chips, segments, search bars and the nav indicator are `shape-full` pills. Containers are `shape-xl` rounded rectangles. When pressed, pills morph toward squarer corners (`shape-md` to `shape-xl` by size).
4. **Shapes carry identity.** Avatars, hero icons, badges and decorative seats use the shape library (cookie, clover, flower, sunny, burst, pebble). Pick one shape per kind of thing and keep it.
5. **Character lives in one place.** Each product picks one display face and one illustration style; the rest of the UI stays in Google Sans Flex. Never mix two display faces on one screen.
6. **Warm, specific copy.** The screens talk like a person who knows the subject. Keep that voice.

## Content

- Write in second person, present tense, sentence case everywhere, including buttons and titles: "Your limit is set.", "Riding carefully. Frosting is fragile."
- Buttons are verbs and say what they spend: "Review order", "Place order · $23.33", "Book for 49,000 pts", "Deposit $500.00".
- Explain consequences in the supporting line, plainly: "It fills on its own when the price crosses. Cancel it any time in Activity."
- Greetings can be playful once per screen ("Up late, Ada?", "Good evening, Ada.") and the supporting line returns to facts ("3 books on your shelves: 1 on the go, 1 waiting, 1 finished.").
- Units are explicit and spaced: 4.4 km, 12 min, 16.7 MWh, 5.8¢/pt. Use the real unit of the domain, not a generic one.
- Use ≈ for estimates, → for routes and transfers (SFO → JFK → LHR), · (middle dot) to join metadata ("Market · 10:50 PM").
- No emoji in UI copy. Use a Material Symbol or a shape instead.
- Empty states describe what will appear and how to make the first one, beside a small illustration ("Long-press a junction or street you'd rather skip and choose Avoid area.").

## Colour

- Page background is `surface`. Group content on `surface-container-low`; put interactive fills (search, unselected segments, stat tiles) on `surface-container-high`; use `surface-container` for the navigation bar.
- Text is `on-surface`; supporting text, captions and inactive icons are `on-surface-variant`. Both hold 4.5:1 on every surface token in both themes.
- `primary` is for the main action, the selected segment, the active slider and progress, and one emphasised word in a display title (set it italic). Text on a `primary` fill is `on-primary`.
- Containers come in matched pairs: `primary-container` / `on-primary-container`, `secondary-container` / `on-secondary-container`, `tertiary-container` / `on-tertiary-container`. Use them for tonal cards, the nav indicator, tonal buttons and selected chips.
- `secondary` is the second voice (settings selections, chart series two). `tertiary` is for playful accents and avatars.
- `highlight` is one loud fill per screen: the Shoot FAB, a streak, a score shape. It is never a text colour; content on it is `on-highlight`.
- Gains and success are `positive`, losses and errors are `error`. Always add an arrow or icon so the meaning doesn't rely on red versus green.
- Dark theme is not inverted light: surfaces are warm near-blacks, accents lighten (`primary` becomes a peach), and fills take dark text (`on-primary` is a deep brown). Use the tokens and it works.
- `focus` (2px solid, 2px offset) marks keyboard focus on every control.

## Type

- **Google Sans Flex** (`font-sans`) sets all UI: headlines, titles, body, labels and hero numerals.
- **Fraunces** (`font-display`) is the default display face for `display-*` styles, greetings, card titles on hub screens and celebration moments. Products may swap it (see Seed palettes): Instrument Serif for editorial products, Big Shoulders Display for travel, DynaPuff or Shrikhand for food, Doto for clocks and departure boards.
- **Google Sans Code** (`font-mono`) sets `eyebrow`, `data-medium` and `data-small`: kickers, codes, timestamps, hex values, flight numbers.
- Hero figures use `numeral-large` / `numeral-medium` / `numeral-small` with tabular numerals. Put the unit beside a numeral in `title-small`.
- Tab titles are `headline-large`; pushed screens `headline-medium`; sections `headline-small` or `title-large`.
- An `eyebrow` (uppercase mono, letter-spaced) sits above titles and list sections: REVIEW · MARKET ORDER, TODAY, LATELY SPOTTED 12.

## Shape

- Corner scale: `shape-xs` 4 · `shape-sm` 8 · `shape-md` 12 · `shape-lg` 16 · `shape-lg-increased` 20 · `shape-xl` 28 · `shape-xl-increased` 32 · `shape-xxl` 48 · `shape-full`.
- Cards, sheets and settings groups use `shape-xl`. List cards and tiles use `shape-lg-increased`. FABs use `shape-lg` (large FAB `shape-xl`).
- Grouped segments (settings rows, connected buttons) use big outer corners and small inner corners (`shape-xs` for list segments, `shape-sm` for buttons) with `space-0-5` gaps.
- The shape library (`ShapeAvatar`): cookie4, cookie6, cookie9, cookie12, clover4, flower5, flower8, sunny, burst, pebble, circle. Use them for avatars, hero-icon seats, ratings and score badges (Greenwave's "87" sits in a burst), and decorative background blobs behind product imagery.

## Layout and spacing

- Phone gutter is `space-4`; unfolded/tablet gutter is `space-6`. Cards inside a screen are `space-3` apart; sections are `space-6` apart; a screen title has `space-8` above it.
- Card padding is `space-4` (dense) or `space-5` (hero and tonal).
- The primary action of a flow is a `size="md"` full-width Button pinned above the gesture area, `space-4` from the sides.
- Touch targets are at least `touch-target` (48px).
- On unfolded layouts, use a two-pane list/detail: list on the left (max 420px), detail on the right; the navigation bar becomes a rail.

## Elevation

- Default is flat (`elevation-0`); tone does the separating.
- `elevation-1` for an elevated button or a dragged card. `elevation-3` for FABs and floating bars (a cart bar that follows the scroll).
- Sheets and dialogs sit above a `scrim`.

## Motion

- M3 Expressive motion is springy. Spatial changes (position, size, shape) overshoot slightly: use `cubic-bezier(0.34, 1.4, 0.64, 1)` over 300–500ms. Effects (colour, opacity) never overshoot: `cubic-bezier(0.2, 0, 0, 1)` over 150–200ms.
- Pressed pills morph their corners over 220ms. The nav indicator grows in from the centre. Switch thumbs grow when pressed and spring across.
- Celebrate outcomes once: stars pop in sequence, a shape rotates slowly behind a mascot, a wavy progress bar travels. Respect `prefers-reduced-motion` by removing travel and rotation.

## Iconography

- Use **Material Symbols Rounded** (Google Fonts), weight 400, optical size 24. Icons are outlined by default and switch to filled (`FILL 1`) when selected (nav items, toggled favourites).
- Write icons as ligatures inside an element with the `ex-icon` class: `<span class="ex-icon">arrow_back</span>`. Add `is-filled` for the filled form.
- Icons in fills take the fill's `on-` colour; standalone icons are `on-surface-variant`.
- Product illustrations are flat, warm vector scenes with soft gradients (a finch on a wire, a magpie, a lighthouse at dusk, an isometric solar house). This kit ships no illustrations; commission one style per product and keep it consistent.

## Components

Load `components/bundle.css` after tokens, then React 18 and `components/bundle.js`; components live on `window.Expressive`. Each component's guideline says what to provide. The main ones:

- Actions: `Button`, `IconButton`, `Fab`, `ButtonGroup`
- Selection: `Chip`, `Switch`, `Slider`
- Status: `Badge`, `ValuePill`, `WavyProgress`, `Snackbar`
- Navigation: `NavigationBar`, `TopBar`
- Inputs: `SearchBar`, `TextField`
- Containment: `Card`, `ListItem`, `GroupedList`, `StatTile`, `BottomSheet`, `SummaryList`
- Identity: `ShapeAvatar`

See **Screen patterns** for how the screens combine them.
