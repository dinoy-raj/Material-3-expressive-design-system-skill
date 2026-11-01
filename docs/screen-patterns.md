# Screen patterns

Eight layouts cover nearly all of the 100 reference screens. Build new screens from these before inventing a new one.

## 1. Hub (home tab)

The screen the app opens to.

1. `TopBar` with `display` title: a greeting or the app name, plus a supporting line of facts ("Evening, Sam", "3 books on your shelves").
2. Optional attention banner: a `Card` in `error-container` or `primary-container` with an `eyebrow` (NEEDS YOU) and an arrow.
3. The hero: one big number (`numeral-large` balance with a `ValuePill inline` delta and a chart under it), or a tonal hero `Card` with the next thing to do ("Up next · Finding C, D and E", "Start your first lesson").
4. A horizontal carousel of cards (`shape-xl`, about 70% screen width so the next card peeks).
5. Lists of owned things as `ListItem`s.
6. `NavigationBar`, optionally a `Fab`.

Seen in: Sherwood Portfolio, Trill Learn, Magpie Studio, Shelfie Library, Dollop Discover, Heliotrope Now.

## 2. Tab list (Explore, Activity, Orders)

1. `TopBar` with `headline-large` title, no back button.
2. `SearchBar` directly under the title, or a row of filter `Chip`s / a `ButtonGroup` (Gainers · Losers).
3. Content grouped by an `eyebrow` header (TODAY, MON, OCT 5, OCTOBER 2026) or a `title-large` section head.
4. `ListItem` rows with `ShapeAvatar` leading and a value or `Button variant="outlined"` ("Reorder") trailing.

## 3. Detail

1. `TopBar` with back and one or two actions (star, share, more).
2. Identity: `ShapeAvatar` or hero image in a large shape, title (`headline-medium` or display face), mono metadata (ACRN · TECHNOLOGY).
3. The hero value (`numeral-medium` price, "4.4 km · 12 min · 0 m" stats with a burst score).
4. A chart with a `ButtonGroup` of ranges under it (1D 1W 1M 3M YTD 1Y ALL).
5. A `Card` "Your position" with `SummaryList` rows, then an About section in `body-large`.
6. Bottom action bar: `Button variant="outlined"` + `Button` side by side (Sell · Buy), or one full-width primary ("Add $4.50").

## 4. Amount entry (ticket, deposit, tip)

1. Small `TopBar` with close, the subject and live price.
2. `ButtonGroup`s for modes (Dollars / Shares, Market / Limit).
3. The amount in `numeral-large`, centred, with an ≈ conversion line below in `data-medium`.
4. Quick amounts as a `ButtonGroup` ($100 · $500 · $1,000 · $5,000).
5. A number keypad: a 3×4 grid of 64px-tall text buttons in `headline-medium`, backspace icon bottom-right.
6. Full-width primary `Button size="md"` ("Review order", "Deposit $500.00").

## 5. Review and confirm

1. Small `TopBar` with back. An `eyebrow` (REVIEW · MARKET ORDER) and a display-face sentence with the amount italicised in `primary` ("Buy *$100.00* of ACRN").
2. `SummaryList` of the terms; total row last.
3. A plain-language footnote about what happens next.
4. A deliberate confirm gesture for money: a swipe-up handle or a `size="lg"` button ("Book for 49,000 pts").

## 6. Outcome and celebration

1. `space-16` top padding, a centred illustration or a spinning `ShapeAvatar` behind a mascot.
2. A status `Badge` (mono + dot: PENDING) and a `display-large` sentence ("Your limit is set.", "Beautifully played.").
3. One line of facts, then a `SummaryList` or a row of `StatTile`s (100% first-try · +100 XP · 8/8).
4. Two stacked full-width buttons: outlined secondary path above, filled "Done" / "Continue" below.

## 7. Settings

1. `TopBar` with `headline-large` "Settings" or "You".
2. Optional profile hero: a `Card variant="primary"` with a shape avatar and a one-line status.
3. `GroupedList`s, each titled in `primary` (Riding, Map, Appearance, About). Each row is a `Switch` with a supporting line, a `ButtonGroup` (System · Light · Dark), or a `ListItem` with a trailing value.
4. A playful last group is welcome (Heliotrope's "Secrets · 0 of 3 found").

## 8. Bottom-sheet capture

1. The screen behind stays visible under the `scrim`.
2. `BottomSheet` with a mono `eyebrow` naming the type (PALETTE, TYPE, QUOTE) and a display-face title.
3. One or two `TextField`s, a choice row (`ButtonGroup` or `Chip`s), then destination `Chip`s ("Post to").
4. Full-width primary action at the bottom ("Post", "Create", "Add to library").

## Unfolded and tablet

- Hub and tab lists become list/detail: the list pane keeps phone layout at up to 420px; the detail pane fills the rest with `space-6` gutters.
- The `NavigationBar` becomes a leading navigation rail with the same items and the `Fab` at its top.
- Charts and maps take the extra width; forms stay at a readable 560px maximum.
