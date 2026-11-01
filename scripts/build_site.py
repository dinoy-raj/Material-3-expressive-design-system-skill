#!/usr/bin/env python3
"""Build the GitHub Pages website into _site/.

Run after scripts/build.py:  python3 scripts/build_site.py
Needs the `markdown` package (pip install markdown).
"""
import html
import json
import re
import shutil
import zipfile
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
TOKENS = json.loads((ROOT / "tokens" / "tokens.json").read_text())
REPO_URL = "https://github.com/dinoy-raj/Material-3-expressive-design-system-skill"
SKILL_ZIP = "material-3-expressive-skill.zip"

MD = lambda text: markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])


def components():
    items = []
    for d in sorted((ROOT / "components").iterdir()):
        prev, readme = d / "preview.html", d / "README.md"
        if d.name == "Cover" or not prev.is_file():
            continue
        src = prev.read_text()
        js = re.search(r"\.render\((.*)\);\s*</script>", src, re.S).group(1)
        group = re.search(r'group="([^"]+)"', src).group(1)
        body = readme.read_text() if readme.is_file() else ""
        body = re.sub(r"^# .*\n+", "", body)
        summary = re.split(r"(?<=\.)\s", body.strip(), maxsplit=1)[0]
        items.append({"name": d.name, "group": group, "js": js, "summary": summary, "readme": body})
    return items


def page(title, body, depth=0, scripts=""):
    up = "../" * depth
    nav = [("Overview", f"{up}index.html#top"), ("Foundations", f"{up}index.html#foundations"), ("Components", f"{up}index.html#components"),
           ("Skill", f"{up}docs/skill.html"), ("Brand book", f"{up}docs/brand-book.html"), ("Patterns", f"{up}docs/screen-patterns.html"), ("Palettes", f"{up}docs/seed-palettes.html")]
    links = "".join(f'<a href="{href}">{name}</a>' for name, href in nav)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="Expressive Kit: a Material 3 Expressive design system and AI skill with tokens, components, a Compose theme and guidelines.">
<meta property="og:image" content="{up}assets/banner-light.png">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='-1 -1 2 2'%3E%3Cpath fill='%23a8330f' d='{shape_icon()}'/%3E%3C/svg%3E">
<link rel="stylesheet" href="{up}tokens/tokens.css">
<link rel="stylesheet" href="{up}components/bundle.css">
<link rel="stylesheet" href="{up}site.css">
</head>
<body>
<header class="s-top"><div class="s-in">
  <a class="s-brand" href="{up}index.html"><svg viewBox="-1 -1 2 2" aria-hidden="true"><path d="{shape_icon()}"/></svg>Expressive Kit</a>
  <nav class="s-nav" aria-label="Site">{links}</nav>
  <div id="theme-switch"></div>
</div></header>
<main id="top">
{body}
</main>
<footer class="s-foot"><div class="s-in">
  <span>Expressive Kit · Material 3 Expressive design system</span>
  <a href="{REPO_URL}">Source on GitHub</a>
</div></footer>
<script src="https://cdn.jsdelivr.net/npm/react@18.3.1/umd/react.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/react-dom@18.3.1/umd/react-dom.production.min.js"></script>
<script src="{up}components/bundle.js"></script>
<script>
  var E = window.Expressive, h = React.createElement;
  var saved = null; try {{ saved = localStorage.getItem('ek-theme'); }} catch (e) {{}}
  if (saved && saved !== 'system') document.documentElement.dataset.theme = saved;
  ReactDOM.createRoot(document.getElementById('theme-switch')).render(h(E.ButtonGroup, {{ label: 'Theme', fit: true, defaultValue: saved || 'system',
    options: [{{ value: 'system', icon: 'contrast', label: 'Auto' }}, {{ value: 'light', icon: 'light_mode', label: 'Light' }}, {{ value: 'dark', icon: 'dark_mode', label: 'Dark' }}],
    onChange: function (v) {{ if (v === 'system') delete document.documentElement.dataset.theme; else document.documentElement.dataset.theme = v; try {{ localStorage.setItem('ek-theme', v); }} catch (e) {{}} }} }}));
{scripts}
</script>
</body>
</html>
"""


_ICON = None


def shape_icon():
    global _ICON
    if _ICON is None:
        import math
        pts = []
        for i in range(90):
            t = i / 90 * 2 * math.pi
            r = (1 + 0.075 * math.cos(9 * t)) / 1.075
            pts.append(f"{r * math.cos(t):.3f} {r * math.sin(t):.3f}")
        _ICON = "M" + "L".join(pts) + "Z"
    return _ICON


def foundations():
    rows = []
    groups = {}
    for c in TOKENS["color"]["tokens"]:
        stem = c["name"].replace("on-", "").split("-")[0]
        groups.setdefault(stem, []).append(c)
    sw = []
    for c in TOKENS["color"]["tokens"]:
        if c["name"] in ("scrim", "focus"):
            continue
        sw.append(f'<div class="sw"><span class="chip" style="background:var(--{c["name"]})"></span><span class="n">{c["name"]}</span></div>')
    type_rows = []
    for g in TOKENS["type"]["groups"]:
        for s in g["styles"]:
            type_rows.append(f'<div class="ty"><span class="meta">{s["name"]}<br>{s["fontSize"]} / {s["lineHeight"]} · {s["fontWeight"]}</span><span class="{s["name"]}">{html.escape(s.get("sample", s["name"]))}</span></div>')
    radii = "".join(f'<div class="rad"><span style="border-radius:var(--{r["name"]})"></span>{r["name"]}<em>{r["value"]}</em></div>' for r in TOKENS["radius"]["tokens"])
    space = "".join(f'<div class="sp"><span style="width:var(--{css(s["name"])})"></span>{s["name"]}<em>{s["value"]}</em></div>' for s in TOKENS["spacing"]["tokens"])
    shapes = "".join(f'<div class="shp" data-shape="{n}"></div>' for n in ["cookie4", "cookie6", "cookie9", "cookie12", "clover4", "flower5", "flower8", "sunny", "burst", "pebble", "circle"])
    return f"""
<section class="s-sec" id="foundations"><div class="s-in">
  <div class="eyebrow">Foundations</div>
  <h2 class="headline-large">Tokens that switch with the theme</h2>
  <p class="lede body-large">Every colour is a role, not a hex. Flip the theme in the top bar and watch each swatch change.</p>
  <h3 class="title-large">Colour roles</h3>
  <div class="swatches">{"".join(sw)}</div>
  <h3 class="title-large">Type scale</h3>
  <div class="types">{"".join(type_rows)}</div>
  <div class="two">
    <div><h3 class="title-large">Corner shapes</h3><div class="radii">{radii}</div></div>
    <div><h3 class="title-large">Spacing</h3><div class="spaces">{space}</div></div>
  </div>
  <h3 class="title-large">Shape library</h3>
  <p class="body-medium muted">Cut avatars, hero seats and masks from these. Each kind of thing keeps one shape.</p>
  <div class="shapes" id="shapes">{shapes}</div>
</div></section>"""


def inline_md(text):
    return re.sub(r"^<p>|</p>$", "", MD(text).strip())


def css(n):
    return n.replace(".", "\\.")


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "docs" / "components").mkdir(parents=True)
    for d in ("tokens", "components", "assets", "android", "examples"):
        shutil.copytree(ROOT / d, OUT / d)
    shutil.copy(ROOT / "scripts" / "site.css", OUT / "site.css")

    comps = components()

    # Downloadable skill: SKILL.md plus everything it references.
    with zipfile.ZipFile(OUT / SKILL_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        base = "material-3-expressive"
        z.write(ROOT / "SKILL.md", f"{base}/SKILL.md")
        for folder in ("tokens", "docs", "components", "android"):
            for f in sorted((ROOT / folder).rglob("*")):
                if f.is_file():
                    z.write(f, f"{base}/{f.relative_to(ROOT)}")

    # Home page
    cards = "".join(
        f'<article class="c-card" id="c-{c["name"]}"><header><a class="title-large" href="docs/components/{c["name"]}.html">{c["name"]}</a><span class="eyebrow">{c["group"]}</span></header>'
        f'<div class="c-live" id="live-{c["name"]}"></div><p class="body-medium muted">{inline_md(c["summary"])}</p></article>' for c in comps)
    renders = "\n".join(f"  ReactDOM.createRoot(document.getElementById('live-{c['name']}')).render({c['js']});" for c in comps)
    shapes_js = "  document.querySelectorAll('[data-shape]').forEach(function (el) { ReactDOM.createRoot(el).render(h(E.ShapeAvatar, { shape: el.dataset.shape, size: 64, tone: ['primary-container','secondary-container','tertiary-container','highlight'][Array.prototype.indexOf.call(el.parentNode.children, el) % 4], label: el.dataset.shape })); });"
    hero = f"""
<section class="s-hero"><div class="s-in hero-grid">
  <div class="hero-words">
    <div class="eyebrow">Material 3 Expressive · Design system · AI skill</div>
    <h1 class="hero-title">Expressive<br><em>Kit</em></h1>
    <p class="body-large lede">Tokens, {len(comps)} components, a Jetpack Compose theme and a skill file that teaches any AI tool to design in the Material 3 Expressive style.</p>
    <div class="ex-row hero-ctas" id="ctas"></div>
  </div>
  <div class="hero-art">
    <img class="only-light" src="assets/hero-light.png" alt="Expressive Kit components on a phone screen: stat tiles, a tonal card with wavy progress, a connected button group and a list row." width="680" height="640">
    <img class="only-dark" src="assets/hero-dark.png" alt="Expressive Kit components on a phone screen in the dark theme." width="680" height="640">
  </div>
</div></section>
<section class="s-sec"><div class="s-in">
  <div class="eyebrow">Get started</div>
  <h2 class="headline-large">Four ways to use it</h2>
  <div class="ways">
    <div class="way"><span class="way-ic" data-ws="flower5" data-icon="auto_awesome"></span><h3 class="title-large">As an AI skill</h3><p class="body-medium">Download the skill and upload it to Claude (Settings, Capabilities, Skills) or unzip it into <code>~/.claude/skills/</code> for Claude Code. Other AI tools can read <code>SKILL.md</code> directly.</p><a class="ex-btn v-tonal ex-press" href="{SKILL_ZIP}" download>Download skill</a></div>
    <div class="way"><span class="way-ic" data-ws="clover4" data-icon="palette"></span><h3 class="title-large">As a Claude design system</h3><p class="body-medium">Ask Claude to create a design system from this repository. <code>tokens/tokens.json</code>, <code>components/bundle.*</code> and each <code>preview.html</code> already follow Claude's design system format.</p><a class="ex-btn v-tonal ex-press" href="docs/skill.html#import">How to import</a></div>
    <div class="way"><span class="way-ic" data-ws="cookie9" data-icon="code"></span><h3 class="title-large">On the web</h3><p class="body-medium">Link <code>tokens/tokens.css</code> and <code>components/bundle.css</code>, load React 18 and <code>components/bundle.js</code>, then use <code>window.Expressive</code>.</p><a class="ex-btn v-tonal ex-press" href="examples/gallery.html">Open gallery</a></div>
    <div class="way"><span class="way-ic" data-ws="sunny" data-icon="android"></span><h3 class="title-large">On Android</h3><p class="body-medium">Copy <code>android/ExpressiveTheme.kt</code> into your app and wrap your UI in <code>ExpressiveTheme {{ }}</code>.</p><a class="ex-btn v-tonal ex-press" href="android/ExpressiveTheme.kt">View theme</a></div>
  </div>
</div></section>"""
    comp_sec = f"""
<section class="s-sec" id="components"><div class="s-in">
  <div class="eyebrow">Components</div>
  <h2 class="headline-large">{len(comps)} live components</h2>
  <p class="lede body-large">Press them: pills tighten their corners, selections round into full pills, the loading indicator morphs through the shape library.</p>
  <div class="c-grid">{cards}</div>
</div></section>"""
    ways_js = "  document.querySelectorAll('[data-ws]').forEach(function (el) { ReactDOM.createRoot(el).render(h(E.ShapeAvatar, { shape: el.dataset.ws, size: 56, icon: el.dataset.icon, tone: 'primary-container' })); });"
    ctas_js = f"  ReactDOM.createRoot(document.getElementById('ctas')).render(h(React.Fragment, null, h('a', {{ className: 'ex-press ex-btn v-filled size-md', href: '{SKILL_ZIP}', download: true }}, h('span', {{ className: 'ex-icon' }}, 'download'), 'Download skill'), h('a', {{ className: 'ex-press ex-btn v-outlined size-md', href: 'docs/skill.html' }}, 'Read SKILL.md')));"
    (OUT / "index.html").write_text(page("Expressive Kit", hero + foundations() + comp_sec, 0, "\n".join([ctas_js, ways_js, shapes_js, renders])))

    # Docs pages
    skill = re.sub(r"^---.*?---\s*", "", (ROOT / "SKILL.md").read_text(), flags=re.S)
    import_md = f"""
## Import into Claude {{#import}}

**As a skill.** Download [{SKILL_ZIP}](../{SKILL_ZIP}). In the Claude app, open Settings, then Capabilities, and upload it under Skills. In Claude Code, unzip it into `~/.claude/skills/` (personal) or `.claude/skills/` in a project.

**As a design system.** In a Claude conversation that can read this repository, ask: "Create a design system from {REPO_URL}". The repository already matches Claude's design system format: `tokens/tokens.json` is the token file, `components/bundle.js` (namespace `Expressive`, React 18) and `components/bundle.css` are the live bundle, each `components/<Name>/preview.html` is a component card, `components/<Name>/README.md` its guideline, `components/Cover/preview.html` the cover, and `docs/brand-book.md` the brand book.

**Any other AI tool.** Point it at `SKILL.md`; it links to every other file it needs.
"""
    docs = {"skill": ("SKILL.md", skill + import_md), "brand-book": ("Brand book", (ROOT / "docs/brand-book.md").read_text()),
            "screen-patterns": ("Screen patterns", (ROOT / "docs/screen-patterns.md").read_text()),
            "seed-palettes": ("Seed palettes", (ROOT / "docs/seed-palettes.md").read_text())}
    for slug, (title, text) in docs.items():
        body = MD(text).replace("{#import}", "").replace("<h2>Import into Claude", '<h2 id="import">Import into Claude')
        (OUT / "docs" / f"{slug}.html").write_text(page(f"{title} · Expressive Kit", f'<article class="s-in s-doc">{body}</article>', 1))
    for c in comps:
        body = f"""<article class="s-in s-doc"><div class="eyebrow">{c['group']}</div><h1>{c['name']}</h1>
<div class="c-card c-solo"><div class="c-live" id="live"></div></div>
{MD(c['readme'])}
<p><a href="../../index.html#components">All components</a></p></article>"""
        js = f"  ReactDOM.createRoot(document.getElementById('live')).render({c['js']});"
        (OUT / "docs" / "components" / f"{c['name']}.html").write_text(page(f"{c['name']} · Expressive Kit", body, 2, js))
    (OUT / ".nojekyll").write_text("")
    print(f"Built _site/ with {len(comps)} components and {SKILL_ZIP}")


if __name__ == "__main__":
    build()
