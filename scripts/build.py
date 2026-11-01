#!/usr/bin/env python3
"""Build Expressive Kit outputs from tokens/tokens.json.

Generates:
  tokens/tokens.css                  CSS custom properties, light + dark, plus type classes
  tokens/tokens.mjs                  the same tokens as a JS module
  android/ExpressiveTheme.kt         Jetpack Compose colour schemes, extended colours, shapes, type
  examples/gallery.html              every component preview on one page

Run from the repository root:  python3 scripts/build.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS = json.loads((ROOT / "tokens" / "tokens.json").read_text())
THEMES = [t["id"] for t in TOKENS["color"]["themes"]]
HEADER = "Expressive Kit, generated from tokens/tokens.json by scripts/build.py. Do not edit by hand."


def color_value(token, theme):
    v = token["value"]
    v = v if isinstance(v, str) else v.get(theme, v[THEMES[0]])
    m = re.fullmatch(r"\{(.+)\}", v)
    return f"var(--{m.group(1)})" if m else v


def resolved(name, theme):
    tok = next(t for t in TOKENS["color"]["tokens"] if t["name"] == name)
    v = tok["value"] if isinstance(tok["value"], str) else tok["value"].get(theme, tok["value"][THEMES[0]])
    m = re.fullmatch(r"\{(.+)\}", v)
    return resolved(m.group(1), theme) if m else v


def css_name(n):
    return n.replace(".", "\\.")


# ---------- tokens.css ----------
def build_css():
    light, dark = THEMES[0], THEMES[1]
    colors = TOKENS["color"]["tokens"]
    shadows = TOKENS.get("shadow", {}).get("tokens", [])

    def theme_block(theme):
        lines = [f"  --{c['name']}: {color_value(c, theme)};" for c in colors]
        for s in shadows:
            v = s["value"] if isinstance(s["value"], str) else s["value"].get(theme, s["value"][light])
            lines.append(f"  --{s['name']}: {v};")
        return "\n".join(lines)

    static = []
    for fam in ("spacing", "radius", "size", "opacity"):
        for t in TOKENS.get(fam, {}).get("tokens", []):
            static.append(f"  --{css_name(t['name'])}: {t['value']};")
    for key, stack in TOKENS["type"]["families"].items():
        static.append(f"  --font-{key}: {stack};")

    out = [f"/* {HEADER} */", ""]
    out.append(f':root, [data-theme="{light}"] {{\n  color-scheme: light;\n{theme_block(light)}\n}}')
    out.append(f'@media (prefers-color-scheme: dark) {{\n  :root:not([data-theme="{light}"]) {{\n    color-scheme: dark;\n'
               + "\n".join("  " + l for l in theme_block(dark).splitlines()) + "\n  }\n}")
    out.append(f'[data-theme="{dark}"] {{\n  color-scheme: dark;\n{theme_block(dark)}\n}}')
    out.append(":root {\n" + "\n".join(static) + "\n}")
    for g in TOKENS["type"]["groups"]:
        for s in g["styles"]:
            fam = s.get("family", g["family"])
            decl = [f"font-family: var(--font-{fam})", f"font-size: {s['fontSize']}", f"line-height: {s['lineHeight']}",
                    f"font-weight: {s['fontWeight']}"]
            if "letterSpacing" in s:
                decl.append(f"letter-spacing: {s['letterSpacing']}")
            if s["name"] == "eyebrow":
                decl.append("text-transform: uppercase")
            if g["name"] == "Hero numerals":
                decl.append("font-variant-numeric: tabular-nums")
            out.append(f".{s['name']} {{ " + "; ".join(decl) + "; }")
    (ROOT / "tokens" / "tokens.css").write_text("\n\n".join(out) + "\n")


# ---------- tokens.mjs ----------
def build_js():
    data = {
        "colors": {th: {c["name"]: resolved(c["name"], th) for c in TOKENS["color"]["tokens"]} for th in THEMES},
        "spacing": {t["name"]: t["value"] for t in TOKENS["spacing"]["tokens"]},
        "radius": {t["name"]: t["value"] for t in TOKENS["radius"]["tokens"]},
        "size": {t["name"]: t["value"] for t in TOKENS["size"]["tokens"]},
        "fonts": TOKENS["type"]["families"],
        "type": {s["name"]: {k: v for k, v in s.items() if k in ("fontSize", "lineHeight", "fontWeight", "letterSpacing")} | {"family": s.get("family", g["family"])}
                 for g in TOKENS["type"]["groups"] for s in g["styles"]},
    }
    (ROOT / "tokens" / "tokens.mjs").write_text(f"// {HEADER}\nexport const tokens = {json.dumps(data, indent=2)};\nexport default tokens;\n")


# ---------- Android Compose ----------
def kt_color(hexv):
    m = re.fullmatch(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)", hexv)
    if m:
        r, g, b, a = int(m[1]), int(m[2]), int(m[3]), float(m[4])
        return f"Color(0x{round(a * 255):02X}{r:02X}{g:02X}{b:02X})"
    h = hexv.lstrip("#")
    return f"Color(0xFF{h.upper()})"


def camel(n):
    parts = n.split("-")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


M3_ROLES = ["primary", "on-primary", "primary-container", "on-primary-container", "inverse-primary",
            "secondary", "on-secondary", "secondary-container", "on-secondary-container",
            "tertiary", "on-tertiary", "tertiary-container", "on-tertiary-container",
            "surface", "on-surface", "on-surface-variant", "inverse-surface", "inverse-on-surface",
            "error", "on-error", "error-container", "on-error-container", "outline", "outline-variant",
            "surface-container-lowest", "surface-container-low", "surface-container", "surface-container-high", "surface-container-highest"]
EXTENDED = ["highlight", "on-highlight", "positive", "positive-container", "on-positive-container"]


def build_android():
    def scheme(theme, fn):
        args = [f"    {camel(r)} = {kt_color(resolved(r, theme))}," for r in M3_ROLES]
        args.append(f"    background = {kt_color(resolved('surface', theme))},")
        args.append(f"    onBackground = {kt_color(resolved('on-surface', theme))},")
        args.append(f"    scrim = {kt_color(resolved('scrim', theme))},")
        builder = "lightColorScheme" if theme == THEMES[0] else "darkColorScheme"
        return f"val {fn} = {builder}(\n" + "\n".join(args) + "\n)"

    def ext(theme, name):
        args = [f"    {camel(r)} = {kt_color(resolved(r, theme))}," for r in EXTENDED]
        return f"val {name} = ExtendedColors(\n" + "\n".join(args) + "\n)"

    radius = {t["name"]: t["value"] for t in TOKENS["radius"]["tokens"]}
    dp = lambda v: v.replace("px", "")
    type_lines = []
    m3_type = {"display-large": "displayLarge", "display-medium": "displayMedium", "display-small": "displaySmall",
               "headline-large": "headlineLarge", "headline-medium": "headlineMedium", "headline-small": "headlineSmall",
               "title-large": "titleLarge", "title-medium": "titleMedium", "title-small": "titleSmall",
               "body-large": "bodyLarge", "body-medium": "bodyMedium", "body-small": "bodySmall",
               "label-large": "labelLarge", "label-medium": "labelMedium", "label-small": "labelSmall"}
    fam_kt = {"sans": "SansFamily", "display": "DisplayFamily", "mono": "MonoFamily"}
    extra_type = []
    for g in TOKENS["type"]["groups"]:
        for s in g["styles"]:
            fam = fam_kt[s.get("family", g["family"])]
            ls = s.get("letterSpacing", "0px").replace("px", "")
            style = (f"TextStyle(fontFamily = {fam}, fontSize = {dp(s['fontSize'])}.sp, lineHeight = {dp(s['lineHeight'])}.sp, "
                     f"fontWeight = FontWeight({s['fontWeight']}), letterSpacing = ({ls}).sp)")
            if s["name"] in m3_type:
                type_lines.append(f"    {m3_type[s['name']]} = {style},")
            else:
                extra_type.append(f"    val {camel(s['name'])} = {style}")
    kt = f"""// {HEADER}
// Fonts: add Google Sans Flex, Fraunces and Google Sans Code with downloadable fonts
// (androidx.compose.ui:ui-text-google-fonts) or as res/font files, then replace the families below.
package design.expressive.kit

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Shapes
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

val SansFamily: FontFamily = FontFamily.SansSerif
val DisplayFamily: FontFamily = FontFamily.Serif
val MonoFamily: FontFamily = FontFamily.Monospace

{scheme(THEMES[0], 'ExpressiveLightColors')}

{scheme(THEMES[1], 'ExpressiveDarkColors')}

/** Roles Material 3 has no slot for: the loud highlight fill and gain/success colours. */
@Immutable
data class ExtendedColors(
{chr(10).join(f'    val {camel(r)}: Color,' for r in EXTENDED)}
)

{ext(THEMES[0], 'ExpressiveLightExtended')}

{ext(THEMES[1], 'ExpressiveDarkExtended')}

val LocalExtendedColors = staticCompositionLocalOf {{ ExpressiveLightExtended }}

val ExpressiveShapes = Shapes(
    extraSmall = RoundedCornerShape({dp(radius['shape-xs'])}.dp),
    small = RoundedCornerShape({dp(radius['shape-sm'])}.dp),
    medium = RoundedCornerShape({dp(radius['shape-md'])}.dp),
    large = RoundedCornerShape({dp(radius['shape-lg'])}.dp),
    extraLarge = RoundedCornerShape({dp(radius['shape-xl'])}.dp),
)

val ExpressiveTypography = Typography(
{chr(10).join(type_lines)}
)

/** Styles beyond the Material type scale: hero numerals and mono data labels. */
object ExpressiveTextStyles {{
{chr(10).join(extra_type)}
}}

@Composable
fun ExpressiveTheme(darkTheme: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {{
    CompositionLocalProvider(LocalExtendedColors provides if (darkTheme) ExpressiveDarkExtended else ExpressiveLightExtended) {{
        MaterialTheme(
            colorScheme = if (darkTheme) ExpressiveDarkColors else ExpressiveLightColors,
            shapes = ExpressiveShapes,
            typography = ExpressiveTypography,
            content = content,
        )
    }}
}}

object Expressive {{
    val extendedColors: ExtendedColors
        @Composable get() = LocalExtendedColors.current
}}
"""
    (ROOT / "android" / "ExpressiveTheme.kt").write_text(kt)


# ---------- examples/gallery.html ----------
def build_gallery():
    blocks = []
    for d in sorted((ROOT / "components").iterdir()):
        p = d / "preview.html"
        if not p.is_file():
            continue
        html = p.read_text()
        m = re.search(r"\.render\((.*)\);\s*</script>", html, re.S)
        group = re.search(r'group="([^"]+)"', html)
        if not m:
            continue
        blocks.append((d.name, group.group(1) if group else "", m.group(1)))
    sections = "\n".join(
        f'<section class="g-card"><header><h2 class="title-large">{n}</h2><span class="eyebrow">{g}</span></header><div id="c-{n}"></div></section>'
        for n, g, _ in blocks)
    renders = "\n".join(f"  ReactDOM.createRoot(document.getElementById('c-{n}')).render({js});" for n, _, js in blocks)
    page = f"""<!doctype html>
<!-- {HEADER} -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Expressive Kit gallery</title>
<link rel="stylesheet" href="../tokens/tokens.css">
<link rel="stylesheet" href="../components/bundle.css">
<style>
  .g-wrap {{ max-width: 1100px; margin: 0 auto; padding: var(--space-8) var(--space-4); }}
  .g-top {{ display: flex; align-items: center; justify-content: space-between; gap: var(--space-4); flex-wrap: wrap; }}
  .g-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 480px), 1fr)); gap: var(--space-4); margin-top: var(--space-6); align-items: start; }}
  .g-card {{ background: var(--surface-container-lowest); border-radius: var(--shape-xl); overflow: hidden; min-width: 0; }}
  .g-card > header {{ display: flex; align-items: baseline; justify-content: space-between; padding: var(--space-4) var(--space-5) 0; }}
  .g-card > header h2 {{ margin: 0; }}
  .g-card > header .eyebrow {{ color: var(--on-surface-variant); }}
  .g-card > div {{ padding: var(--space-2) 0 var(--space-3); }}
</style>
</head>
<body>
<div class="g-wrap">
  <div class="g-top">
    <div><div class="eyebrow" style="color:var(--on-surface-variant)">Material 3 Expressive</div><h1 class="display-small" style="margin:0">Expressive Kit</h1></div>
    <div id="theme"></div>
  </div>
  <div class="g-grid">
{sections}
  </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/react@18.3.1/umd/react.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/react-dom@18.3.1/umd/react-dom.production.min.js"></script>
<script src="../components/bundle.js"></script>
<script>
  var E = window.Expressive, h = React.createElement;
  ReactDOM.createRoot(document.getElementById('theme')).render(h(E.ButtonGroup, {{ label: 'Theme', fit: true, defaultValue: 'system',
    options: [{{ value: 'system', label: 'System' }}, {{ value: 'light', label: 'Light' }}, {{ value: 'dark', label: 'Dark' }}],
    onChange: function (v) {{ if (v === 'system') delete document.documentElement.dataset.theme; else document.documentElement.dataset.theme = v; }} }}));
{renders}
</script>
</body>
</html>
"""
    (ROOT / "examples" / "gallery.html").write_text(page)


if __name__ == "__main__":
    build_css()
    build_js()
    build_android()
    build_gallery()
    print("Built tokens/tokens.css, tokens/tokens.mjs, android/ExpressiveTheme.kt, examples/gallery.html")
