# Changelog

Versions refer to this skill and kit, not to Google's Material libraries.

## [0.2.0] - 2026-11-16

### Added
- `docs/accessibility.md`: touch targets, tap or keyboard alternatives for every gesture in the kit, screen reader semantics, 200% font scaling, non-text contrast, right-to-left layouts and localization.
- `docs/existing-projects.md`: how to bring M3E into an app that already has a theme (adopt, map or borrow), token mapping to `MaterialTheme`, and fallbacks when expressive APIs aren't available.
- `docs/platforms.md`: support for Compose, web, Views, Wear OS, Flutter, React Native and SwiftUI; spring conversions for each; official sources and how to check versions.
- `docs/review.md`: an audit procedure with severities, a finding format and a verdict.
- A "States" section in `docs/screen-patterns.md` (loading, empty, error, offline, permission, success, destructive and disabled).
- `templates/design-brief.md` and `templates/implementation-handoff.md`.
- "How much expression" guidance in `SKILL.md`, plus an existing-project step, state and accessibility steps, and new checklist items.
- `LICENSE` (MIT), Agent Skills frontmatter fields (`license`, `compatibility`, `metadata`), `scripts/validate_skill.py` and a CI workflow that runs it.
- New guides on the website; the downloadable skill now includes `templates/` and `LICENSE`.

### Changed
- Screen pattern 5: a swipe-to-confirm handle must also work with a tap and with a screen reader.
- `docs/screen-patterns.md` now says ten layouts (it said eight).

## [0.1.0]

- First release: tokens, 29 web components, Compose theme and helpers, brand book, motion recipes, screen patterns, seed palettes and website.
