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


# ---------- springs ----------
def spring_curve(damping, stiffness, tolerance=0.001):
    """Step response of a unit-mass spring from 0 to 1.

    Returns (duration_ms, css_linear_easing). Duration is the time after which the curve stays
    within `tolerance` of its target; the easing samples the real curve so CSS can follow it.
    """
    import math
    w = math.sqrt(stiffness)

    def x(t):
        if damping < 1:
            wd = w * math.sqrt(1 - damping ** 2)
            return 1 - math.exp(-damping * w * t) * (math.cos(wd * t) + damping * w / wd * math.sin(wd * t))
        return 1 - math.exp(-w * t) * (1 + w * t)

    dt, t, settle = 0.001, 0.0, 0.0
    while t < 3:
        if abs(1 - x(t)) > tolerance:
            settle = t
        t += dt
    settle = max(0.05, settle)
    n = 40
    pts = [0.0] + [round(x(settle * i / n), 4) for i in range(1, n)] + [1.0]
    pts = ["0" if v == 0 else "1" if v == 1 else f"{v:g}" for v in pts]
    return round(settle * 1000 / 10) * 10, "linear(" + ", ".join(pts) + ")"


def motion_tokens():
    out = {}
    for scheme in TOKENS.get("motion", {}).get("schemes", []):
        out[scheme["id"]] = {}
        for tk in scheme["tokens"]:
            ms, easing = spring_curve(tk["dampingRatio"], tk["stiffness"])
            out[scheme["id"]][tk["name"]] = {"dampingRatio": tk["dampingRatio"], "stiffness": tk["stiffness"],
                                              "duration": f"{ms}ms", "easing": easing,
                                              "fallbackEasing": TOKENS["motion"]["fallback"][tk["name"]]}
    return out


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

    motion = motion_tokens()
    if motion:
        def motion_block(scheme, key):
            lines = []
            for name, m in motion[scheme].items():
                easing = m[key]
                lines.append(f"  --motion-{name}-duration: {m['duration']};")
                lines.append(f"  --motion-{name}-easing: {easing};")
                lines.append(f"  --motion-{name}: {m['duration']} {easing};")
            return "\n".join(lines)
        stagger = "\n".join(f"  --{t['name']}: {t['value']};" for t in TOKENS["motion"].get("stagger", []))
        out.append("/* Motion: springs from tokens.json. Fallback curves first, then the real spring sampled as linear(). */\n"
                   ":root {\n" + motion_block("expressive", "fallbackEasing") + "\n" + stagger + "\n}")
        out.append('[data-motion="standard"] {\n' + motion_block("standard", "fallbackEasing").replace("cubic-bezier(0.34, 1.56, 0.64, 1)", "cubic-bezier(0.2, 0, 0, 1)")
                   .replace("cubic-bezier(0.34, 1.4, 0.64, 1)", "cubic-bezier(0.2, 0, 0, 1)").replace("cubic-bezier(0.34, 1.3, 0.64, 1)", "cubic-bezier(0.2, 0, 0, 1)") + "\n}")
        out.append("@supports (transition-timing-function: linear(0, 1)) {\n  :root {\n"
                   + "\n".join("  " + l for l in motion_block("expressive", "easing").splitlines())
                   + '\n  }\n  [data-motion="standard"] {\n'
                   + "\n".join("  " + l for l in motion_block("standard", "easing").splitlines()) + "\n  }\n}")
        reduced = []
        for name in motion["expressive"]:
            if name.startswith("spatial"):
                reduced += [f"    --motion-{name}-duration: 0ms;", f"    --motion-{name}: 0ms linear;"]
        out.append("/* Reduced motion: movement becomes instant; colour and opacity changes stay. */\n"
                   "@media (prefers-reduced-motion: reduce) {\n  :root, [data-motion] {\n" + "\n".join(reduced) + "\n  }\n}")
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
            if "fontWeightEmphasized" in s:
                out.append(f".{s['name']}-emphasized {{ " + "; ".join(decl[:3] + [f"font-weight: {s['fontWeightEmphasized']}"] + decl[4:]) + "; }")
    (ROOT / "tokens" / "tokens.css").write_text("\n\n".join(out) + "\n")


# ---------- tokens.mjs ----------
def build_js():
    data = {
        "colors": {th: {c["name"]: resolved(c["name"], th) for c in TOKENS["color"]["tokens"]} for th in THEMES},
        "spacing": {t["name"]: t["value"] for t in TOKENS["spacing"]["tokens"]},
        "radius": {t["name"]: t["value"] for t in TOKENS["radius"]["tokens"]},
        "size": {t["name"]: t["value"] for t in TOKENS["size"]["tokens"]},
        "fonts": TOKENS["type"]["families"],
        "type": {s["name"]: {k: v for k, v in s.items() if k in ("fontSize", "lineHeight", "fontWeight", "fontWeightEmphasized", "letterSpacing")} | {"family": s.get("family", g["family"])}
                 for g in TOKENS["type"]["groups"] for s in g["styles"]},
        "motion": motion_tokens(),
        "stagger": {t["name"]: t["value"] for t in TOKENS.get("motion", {}).get("stagger", [])},
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
    type_lines, emph_lines, extra_type = [], [], []
    m3_type = {"display-large": "displayLarge", "display-medium": "displayMedium", "display-small": "displaySmall",
               "headline-large": "headlineLarge", "headline-medium": "headlineMedium", "headline-small": "headlineSmall",
               "title-large": "titleLarge", "title-medium": "titleMedium", "title-small": "titleSmall",
               "body-large": "bodyLarge", "body-medium": "bodyMedium", "body-small": "bodySmall",
               "label-large": "labelLarge", "label-medium": "labelMedium", "label-small": "labelSmall"}
    fam_kt = {"sans": "SansFamily", "display": "DisplayFamily", "mono": "MonoFamily"}
    for g in TOKENS["type"]["groups"]:
        for s in g["styles"]:
            fam = s.get("family", g["family"])
            ls = s.get("letterSpacing", "0px").replace("px", "")
            size = dp(s["fontSize"])

            def style(weight, family_expr):
                return (f"TextStyle(fontFamily = {family_expr}, fontSize = {size}.sp, lineHeight = {dp(s['lineHeight'])}.sp, "
                        f"fontWeight = FontWeight({weight}), letterSpacing = ({ls}).sp)")
            if s["name"] in m3_type:
                type_lines.append(f"    {m3_type[s['name']]} = {style(s['fontWeight'], f'{fam}({size}f)')},")
                emph_lines.append(f"    {m3_type[s['name']]}Emphasized = {style(s['fontWeightEmphasized'], f'{fam}({size}f)')},")
            else:
                extra_type.append(f"    val {camel(s['name'])} = {style(s['fontWeight'], fam_kt[fam])}")
    motion = motion_tokens()
    motion_rows = "\n".join(
        f" *   {name:<16} expressive {motion['expressive'][name]['dampingRatio']} / {motion['expressive'][name]['stiffness']:<5}"
        f" standard {motion['standard'][name]['dampingRatio']} / {motion['standard'][name]['stiffness']:<5}"
        f" -> MaterialTheme.motionScheme.{ {'fast': 'fast', 'default': 'default', 'slow': 'slow'}[name.split('-')[1]] }{name.split('-')[0].capitalize()}Spec()"
        for name in motion["expressive"])
    kt = f"""// {HEADER}
// Fonts: add Google Sans Flex, Fraunces and Google Sans Code as res/font files (or downloadable fonts),
// then pass them to expressiveTypography(), e.g.
//   expressiveTypography(sans = {{ size -> variableFontFamily(R.font.google_sans_flex, size) }})
// Requires androidx.compose.material3 1.4 or later for MaterialExpressiveTheme and MotionScheme.
@file:OptIn(ExperimentalMaterial3ExpressiveApi::class)

package design.expressive.kit

import android.os.Build
import androidx.annotation.FontRes
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.ColorScheme
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.LocalTonalElevationEnabled
import androidx.compose.material3.MaterialExpressiveTheme
import androidx.compose.material3.MotionScheme
import androidx.compose.material3.Shapes
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.remember
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.lerp
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontVariation
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

val SansFamily: FontFamily = FontFamily.SansSerif
val DisplayFamily: FontFamily = FontFamily.Serif
val MonoFamily: FontFamily = FontFamily.Monospace

private val familyCache = HashMap<Pair<Int, Int>, FontFamily>()

/**
 * A variable font pinned to one optical size, with real cuts at each weight.
 *
 * M3 type tokens set the `opsz` axis equal to the font size, so small text gets the sturdier
 * text cut and large text the tighter display cut from one font file. Pass the result to
 * [expressiveTypography] per size.
 */
fun variableFontFamily(
    @FontRes resId: Int,
    opticalSize: Float,
    weights: IntArray = intArrayOf(400, 500, 600, 700, 800),
): FontFamily = familyCache.getOrPut(resId to opticalSize.toInt()) {{
    FontFamily(
        weights.map {{ w ->
            Font(
                resId = resId,
                weight = FontWeight(w),
                variationSettings = FontVariation.Settings(
                    FontVariation.weight(w),
                    FontVariation.Setting("opsz", opticalSize.coerceIn(6f, 144f)),
                ),
            )
        }},
    )
}}

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

/**
 * True-black variant of a dark scheme for OLED screens. The page goes black and the low
 * containers darken, so cards on `surfaceContainer` and above separate more, not less.
 */
fun ColorScheme.toAmoledBlack(): ColorScheme = copy(
    background = Color.Black,
    surface = Color.Black,
    surfaceDim = Color.Black,
    surfaceContainerLowest = Color.Black,
    surfaceContainerLow = lerp(surfaceContainerLow, Color.Black, 0.6f),
    surfaceContainer = lerp(surfaceContainer, Color.Black, 0.35f),
    scrim = Color.Black,
)

val ExpressiveShapes = Shapes(
    extraSmall = RoundedCornerShape({dp(radius['shape-xs'])}.dp),
    small = RoundedCornerShape({dp(radius['shape-sm'])}.dp),
    medium = RoundedCornerShape({dp(radius['shape-md'])}.dp),
    large = RoundedCornerShape({dp(radius['shape-lg'])}.dp),
    largeIncreased = RoundedCornerShape({dp(radius['shape-lg-increased'])}.dp),
    extraLarge = RoundedCornerShape({dp(radius['shape-xl'])}.dp),
    extraLargeIncreased = RoundedCornerShape({dp(radius['shape-xl-increased'])}.dp),
    extraExtraLarge = RoundedCornerShape({dp(radius['shape-xxl'])}.dp),
)

/**
 * The type scale with all fifteen emphasized twins. Each family lambda receives the style's
 * font size so a variable font can pin its optical size to it (see [variableFontFamily]).
 */
fun expressiveTypography(
    sans: (Float) -> FontFamily = {{ SansFamily }},
    display: (Float) -> FontFamily = {{ DisplayFamily }},
): Typography {{
    return Typography(
{chr(10).join('    ' + l for l in type_lines)}
{chr(10).join('    ' + l for l in emph_lines)}
    )
}}

val ExpressiveTypography = expressiveTypography()

/** Styles beyond the Material type scale: hero numerals and mono data labels. */
object ExpressiveTextStyles {{
{chr(10).join(extra_type)}
}}

/**
 * The Expressive Kit theme.
 *
 * Uses [MaterialExpressiveTheme], which installs the expressive motion scheme, shapes and
 * emphasized type. Motion tokens map onto the scheme's springs (damping ratio / stiffness):
{motion_rows}
 * Read them from `MaterialTheme.motionScheme` rather than hard-coding springs.
 *
 * @param motionScheme [MotionScheme.expressive] for consumer and playful apps (overshoot), or
 *   [MotionScheme.standard] for productivity and utility apps (no visible bounce).
 * @param dynamicColor derive colours from the wallpaper on Android 12+. Off by default so the
 *   brand palette shows; keep brand moments (hero cards, illustrations) on brand colours either way.
 * @param amoledBlack in dark theme, use a true-black page for OLED screens.
 */
@Composable
fun ExpressiveTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    motionScheme: MotionScheme = MotionScheme.expressive(),
    dynamicColor: Boolean = false,
    amoledBlack: Boolean = false,
    typography: Typography = ExpressiveTypography,
    content: @Composable () -> Unit,
) {{
    val context = LocalContext.current
    val base = when {{
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S ->
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        darkTheme -> ExpressiveDarkColors
        else -> ExpressiveLightColors
    }}
    val amoled = darkTheme && amoledBlack
    val colorScheme = remember(base, amoled) {{ if (amoled) base.toAmoledBlack() else base }}
    CompositionLocalProvider(
        LocalExtendedColors provides if (darkTheme) ExpressiveDarkExtended else ExpressiveLightExtended,
        // Tonal elevation would paint grey back over a true-black page.
        LocalTonalElevationEnabled provides !amoled,
    ) {{
        MaterialExpressiveTheme(
            colorScheme = colorScheme,
            motionScheme = motionScheme,
            shapes = ExpressiveShapes,
            typography = typography,
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
  .g-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 480px), 1fr)); gap: var(--space-4); margin-top: var(--space-6); }}
  .g-card {{ display: flex; flex-direction: column; background: var(--surface-container-lowest); border-radius: var(--shape-xl); overflow: hidden; min-width: 0; min-height: 360px; }}
  .g-card > header {{ display: flex; align-items: baseline; justify-content: space-between; padding: var(--space-4) var(--space-5) 0; }}
  .g-card > header h2 {{ margin: 0; }}
  .g-card > header .eyebrow {{ color: var(--on-surface-variant); }}
  .g-card > div {{ flex: 1; display: flex; flex-direction: column; justify-content: center; padding: var(--space-2) 0 var(--space-3); overflow-x: auto; }}
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
