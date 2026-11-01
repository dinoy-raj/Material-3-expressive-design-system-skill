# Expressive Kit

A reusable Material 3 Expressive design system for designing and building apps. It was distilled from 100 reference screens (10 sample apps, light and dark) and packages:

- **Design tokens**: 36 colour roles in light and dark (every text pair meets WCAG AA), a 21-style type scale, spacing, corner shapes, elevation, sizes and state opacities.
- **22 web components** (React 18): buttons, connected button groups, chips, switches, an expressive slider, wavy progress, cards, list items, grouped settings lists, stat tiles, shape avatars, bottom sheets and more.
- **An Android Jetpack Compose theme** generated from the same tokens.
- **Guidelines**: a brand book, eight screen patterns and ten seed palettes for re-skinning.

## Repository layout

| Path | What |
| --- | --- |
| `tokens/tokens.json` | **Source of truth.** Edit tokens here only. |
| `tokens/tokens.css` | Generated CSS custom properties (light, dark, system) and type classes such as `.headline-large`. |
| `tokens/tokens.mjs` | Generated JS module with resolved values per theme. |
| `android/ExpressiveTheme.kt` | Generated Compose `ExpressiveTheme`, colour schemes, extended colours, shapes and typography. |
| `components/expressive.js` | The component library, a plain script that defines `window.Expressive` (needs React 18 on the page). |
| `components/expressive.css` | Component styles; loads Google Fonts and Material Symbols Rounded. |
| `components/index.d.ts` | TypeScript prop types for every component. |
| `components/<Name>/README.md` | Usage guideline for each component: what to provide, when to use it, do's and don'ts. |
| `components/<Name>/preview.html` | The example used to render that component. |
| `docs/brand-book.md` | Principles, content voice, colour, type, shape, layout, motion and iconography rules. |
| `docs/screen-patterns.md` | Eight screen layouts (hub, tab list, detail, amount entry, review, celebration, settings, sheet capture). |
| `docs/seed-palettes.md` | Ten product palettes to swap in for a different look. |
| `examples/gallery.html` | Every component on one page with a theme switch. |
| `scripts/build.py` | Regenerates every generated file from `tokens/tokens.json`. |

## Quick start

### Web

```html
<link rel="stylesheet" href="tokens/tokens.css">
<link rel="stylesheet" href="components/expressive.css">

<script src="https://cdn.jsdelivr.net/npm/react@18.3.1/umd/react.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/react-dom@18.3.1/umd/react-dom.production.min.js"></script>
<script src="components/expressive.js"></script>
<script>
  const { Button, NavigationBar } = window.Expressive;
  const h = React.createElement;
  ReactDOM.createRoot(document.getElementById('app')).render(
    h(Button, { size: 'md', fullWidth: true }, 'Review order')
  );
</script>
```

Theme follows the system by default. Force one with `<html data-theme="light">` or `data-theme="dark"`.

Only need the look, not the components? Load `tokens/tokens.css` and use the variables (`var(--primary)`, `var(--shape-xl)`, `var(--space-4)`) and type classes (`class="headline-large"`).

### Android (Jetpack Compose)

Copy `android/ExpressiveTheme.kt` into your app module (change the `package` line), then wrap your UI:

```kotlin
ExpressiveTheme {
    Button(onClick = { }) { Text("Review order") }
    // Extra roles Material 3 has no slot for:
    val highlight = Expressive.extendedColors.highlight
}
```

Swap `SansFamily`, `DisplayFamily` and `MonoFamily` for Google Sans Flex, Fraunces and Google Sans Code using downloadable Google Fonts.

### Design tools

Use `tokens/tokens.json` (or `tokens/tokens.mjs` for resolved hex values) to set up colour and text styles in Figma or another tool. Name styles after the tokens (`primary`, `on-primary`, `title-large`) so designs and code match.

## Preview locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000/examples/gallery.html.

## Changing the system

1. Edit `tokens/tokens.json` (keep the token names; change values). To re-skin for a product, take a row from `docs/seed-palettes.md`.
2. Run `python3 scripts/build.py`.
3. Check text contrast stays at 4.5:1 for each `on-*` pair in both themes.
4. Commit the source and generated files together.

## Using it in other projects

- **Git submodule:** `git submodule add <this repo's URL> design-system`, then link files from `design-system/`.
- **npm from Git (private):** `npm install git+ssh://git@github.com/<owner>/expressive-kit.git`, then import `expressive-kit/tokens/tokens.css`, `expressive-kit/components/expressive.css` and `expressive-kit/components/expressive.js`.

## Credits

Patterns and colours were studied from the Material 3 Expressive sample gallery at m3e.c5inco.dev. No illustrations, logos or assets from those apps are included. Fonts and icons load from Google Fonts under their own licences.
