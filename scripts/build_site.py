#!/usr/bin/env python3
"""Build the website into _site/.

Run after scripts/build.py:  python3 scripts/build_site.py
Needs the `markdown` package (pip install markdown).

The site is published by GitHub Pages at dinoy-raj.github.io/material-3-expressive-skill/ and served on
dinoyraj.com/material-3-expressive-skill through a Vercel rewrite in the portfolio-website repository.
Both hosts use the same path prefix, so every link is root-absolute under BASE and works on either host, with or
without a trailing slash. Page links have no `.html`: GitHub Pages and Vercel both resolve them.
The look follows dinoyraj.com: a floating dark island nav, poster headlines in Google Sans Flex, grouped rows with
small inner corners and a dark footer with a giant wordmark.
"""
import html
import json
import math
import os
import re
import shutil
import zipfile
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
TOKENS = json.loads((ROOT / "tokens" / "tokens.json").read_text())
REPO_URL = "https://github.com/dinoy-raj/material-3-expressive-skill"
HOME_URL = "https://dinoyraj.com"
BASE = os.environ.get("SITE_BASE", "/material-3-expressive-skill/")
CANONICAL = HOME_URL + BASE.rstrip("/")
SKILL_ZIP = "material-3-expressive-skill.zip"

MD = lambda text: markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])

DOCS = [  # slug, nav label, page title, card blurb, card shape, card tone
    ("skill", "Skill", "SKILL.md", "The skill file itself: the rules an AI follows to design in this style, and how to import it.", "cookie9", "primary"),
    ("brand-book", "Brand book", "Brand book", "Voice, colour, type and shape: the decisions behind every token.", "flower8", "tertiary"),
    ("motion", "Motion", "Motion recipes", "Springs, not durations. Recipes for press, morph and reveal on the web and in Compose.", "sunny", "highlight"),
    ("screen-patterns", "Patterns", "Screen patterns", "Whole screens assembled from the parts: dashboards, settings, detail and empty states.", "clover4", "secondary"),
    ("seed-palettes", "Palettes", "Seed palettes", "Swap one seed colour and rebuild every role in light and dark.", "softBurst", "primary"),
]


def u(path=""):
    """Root-absolute URL for a path inside the site."""
    return BASE + path if path else (BASE.rstrip("/") or "/")


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


# Shapes ---------------------------------------------------------------------------------------------------------------

def blob(lobes, amp, sharp=1.0, steps=180):
    """A rounded star path in a -1..1 box: `lobes` bumps, `amp` depth, `sharp` > 1 pinches the valleys."""
    pts = []
    for i in range(steps):
        t = i / steps * 2 * math.pi - math.pi / 2
        c = math.cos(lobes * (t + math.pi / 2))
        w = math.copysign(abs(c) ** (1 / sharp), c)
        r = (1 + amp * w) / (1 + amp)
        pts.append(f"{r * math.cos(t):.3f} {r * math.sin(t):.3f}")
    return "M" + "L".join(pts) + "Z"


SHAPES = {"cookie9": blob(9, .075), "sunny": blob(8, .1), "burst": blob(12, .2, 1.8), "flower8": blob(8, .16, .7),
          "clover4": blob(4, .22, .6), "softBurst": blob(10, .12, 1.3), "cookie4": blob(4, .12)}


def shape_svg(name, cls="", box="-1.05 -1.05 2.1 2.1"):
    return f'<svg class="{cls}" viewBox="{box}" aria-hidden="true"><path d="{SHAPES[name]}"/></svg>'


def shape_icon():
    return SHAPES["cookie9"]


# Page shell -----------------------------------------------------------------------------------------------------------

def page(title, body, path="", description=None, scripts=""):
    description = description or "Expressive Kit: a Material 3 Expressive design system and AI skill with tokens, components, a Compose theme and guidelines."
    nav = [("Overview", u() + "#top"), ("Foundations", u() + "#foundations"), ("Components", u() + "#components")] + \
          [(label, u(f"docs/{slug}")) for slug, label, *_ in DOCS]
    links = "".join(
        f'<a class="lnk rv" style="--i:{i}" href="{href}"><span><span class="num">{i + 1:02d}</span>{name}</span>'
        f'<span class="go">{shape_svg("flower8")}<span class="ex-icon" aria-hidden="true">arrow_outward</span></span></a>'
        for i, (name, href) in enumerate(nav))
    canonical = CANONICAL + ("/" + path if path else "")
    menu_shape = SHAPES["cookie4"]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#fbf6ee">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="author" content="Dinoy Raj">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Dinoy Raj">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{CANONICAL}/assets/banner-light.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:creator" content="@dinoy_raj">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='-1 -1 2 2'%3E%3Cpath fill='%23a8330f' d='{shape_icon()}'/%3E%3C/svg%3E">
<script>try {{ var t = localStorage.getItem('ek-theme') || 'light'; if (t !== 'system') document.documentElement.dataset.theme = t; }} catch (e) {{ document.documentElement.dataset.theme = 'light'; }}</script>
<link rel="stylesheet" href="{u('tokens/tokens.css')}">
<link rel="stylesheet" href="{u('components/bundle.css')}">
<link rel="stylesheet" href="{u('site.css')}">
</head>
<body>
<a class="skip" href="#top">Skip to content</a>
<div class="nav-scrim" hidden></div>
<header class="nav">
  <div class="nav-row">
    <a class="nav-name" href="{u()}">Expressive <span>Kit</span></a>
    <button type="button" class="menu-btn" aria-expanded="false" aria-controls="nav-panel" aria-label="Open menu">
      <svg viewBox="-1.15 -1.15 2.3 2.3" aria-hidden="true"><path d="{menu_shape}"/></svg>
      <span class="ex-icon i-more" aria-hidden="true">more_horiz</span><span class="ex-icon i-close" aria-hidden="true">close</span>
    </button>
  </div>
  <div class="nav-panel" id="nav-panel" inert>
    <nav aria-label="Site">{links}</nav>
    <div class="nav-foot rv" style="--i:{len(nav)}">
      <div class="theme" role="group" aria-label="Theme">
        <button type="button" data-t="system" aria-label="Automatic theme"><span class="ex-icon" aria-hidden="true">contrast</span></button>
        <button type="button" data-t="light" aria-label="Light theme"><span class="ex-icon" aria-hidden="true">light_mode</span></button>
        <button type="button" data-t="dark" aria-label="Dark theme"><span class="ex-icon" aria-hidden="true">dark_mode</span></button>
      </div>
      <a href="{HOME_URL}">dinoyraj.com <span class="ex-icon" aria-hidden="true">arrow_outward</span></a>
    </div>
  </div>
</header>
<main id="top">
{body}
</main>
{footer()}
<script src="https://cdn.jsdelivr.net/npm/react@18.3.1/umd/react.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/react-dom@18.3.1/umd/react-dom.production.min.js"></script>
<script src="{u('components/bundle.js')}"></script>
<script>
  var E = window.Expressive, h = React.createElement;
{NAV_JS}
{scripts}
</script>
</body>
</html>
"""


NAV_JS = """  (function () {
    var nav = document.querySelector('.nav'), btn = nav.querySelector('.menu-btn'), panel = nav.querySelector('.nav-panel'), scrim = document.querySelector('.nav-scrim');
    function set(open) {
      nav.classList.toggle('open', open); btn.setAttribute('aria-expanded', open); btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      nav.style.height = open ? (60 + panel.scrollHeight) + 'px' : '';
      if (open) { panel.removeAttribute('inert'); scrim.hidden = false; requestAnimationFrame(function () { scrim.classList.add('on'); }); }
      else { panel.setAttribute('inert', ''); scrim.classList.remove('on'); setTimeout(function () { if (!nav.classList.contains('open')) scrim.hidden = true; }, 300); }
    }
    nav.querySelector('.nav-row').addEventListener('click', function (e) { if (!e.target.closest('.nav-name')) set(!nav.classList.contains('open')); });
    scrim.addEventListener('click', function () { set(false); });
    panel.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { set(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('open')) { set(false); btn.focus(); } });
    var root = document.documentElement, cur = root.dataset.theme || 'system', themeBtns = nav.querySelectorAll('.theme button');
    function mark() { themeBtns.forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.t === cur); }); }
    themeBtns.forEach(function (b) { b.addEventListener('click', function (e) {
      e.stopPropagation(); cur = b.dataset.t;
      if (cur === 'system') delete root.dataset.theme; else root.dataset.theme = cur;
      try { localStorage.setItem('ek-theme', cur); } catch (err) {}
      mark();
    }); });
    mark();
  })();"""


def footer():
    quick = "".join(f'<a href="{href}">{name}</a>' for name, href in
                    [("Overview", u() + "#top"), ("Get started", u() + "#start"), ("Foundations", u() + "#foundations"),
                     ("Components", u() + "#components"), ("Guides", u() + "#guides")])
    docs = "".join(f'<a href="{u("docs/" + slug)}">{label}</a>' for slug, label, *_ in DOCS)
    ext = "".join(f'<a href="{href}" target="_blank" rel="noopener">{name}</a>' for name, href in
                  [("Source on GitHub", REPO_URL), ("Download skill", u(SKILL_ZIP)), ("Gallery", u("examples/gallery")),
                   ("Compose theme", u("android/ExpressiveTheme.kt"))])
    letters = "".join(f'<span class="wm-l" data-t="{c}"></span>' for c in "EXPRESSIVE")
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="foot-grid">
      <h2>Design it once,<br><span class="em">ship</span> it everywhere.</h2>
      <div><h3>/ Quick links</h3><div class="foot-links">{quick}</div></div>
      <div><h3>/ Guides</h3><div class="foot-links">{docs}</div></div>
      <div><h3>/ Get the kit</h3><div class="foot-links">{ext}</div></div>
    </div>
    <div class="wordmark" aria-hidden="true">{letters}</div>
  </div>
  <div class="wrap fine">
    <span>© 2026 Dinoy · Material 3 Expressive design system</span>
    <a class="kit" href="{HOME_URL}"><span class="kit-dot" aria-hidden="true">{shape_svg("softBurst")}<span class="ex-icon">waving_hand</span></span><span>More from <b>Dinoy</b></span><span class="ex-icon kit-go" aria-hidden="true">arrow_outward</span></a>
  </div>
</footer>"""


# Home sections --------------------------------------------------------------------------------------------------------

def sec_head(eyebrow, title, lede="", extra=""):
    lede_html = f'<p class="sec-lede">{lede}</p>' if lede else ""
    return f'<div class="sec-head"><div><div class="mono">/ {eyebrow}</div><h2 class="sec-title">{title}</h2>{lede_html}</div>{extra}</div>'


def foundations():
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
    shapes = "".join(f'<div class="shp" data-shape="{n}"></div>' for n in ["circle", "cookie4", "cookie6", "cookie7", "cookie9", "cookie12", "clover4", "clover8", "flower5", "flower8", "sunny",
                                                                  "softBurst", "burst", "boom", "pebble", "puffy", "square", "pill", "oval", "diamond",
                                                                  "triangle", "pentagon", "gem", "heart", "arch"])
    motion_rows = "".join(
        f'<div class="mo"><span class="meta">{t["name"]}<br>{t["dampingRatio"]} / {t["stiffness"]}</span><span class="mo-track"><span class="mo-ball" style="transition: left var(--motion-{t["name"]}), background-color var(--motion-{t["name"]})"></span></span></div>'
        for t in TOKENS["motion"]["schemes"][0]["tokens"])
    return f"""
<section class="sec" id="foundations"><div class="wrap">
  {sec_head("Tokens", "Foundations", "Every colour is a role, not a hex. Flip the theme from the menu and watch each swatch change.")}
  <h3 class="sub">/ Colour roles</h3>
  <div class="swatches">{"".join(sw)}</div>
  <h3 class="sub">/ Type scale</h3>
  <div class="types">{"".join(type_rows)}</div>
  <div class="two">
    <div><h3 class="sub">/ Corner shapes</h3><div class="radii">{radii}</div></div>
    <div><h3 class="sub">/ Spacing</h3><div class="spaces">{space}</div></div>
  </div>
  <h3 class="sub">/ Shape library</h3>
  <p class="note">Cut avatars, hero seats and masks from these. Each kind of thing keeps one shape, and any shape can morph into any other.</p>
  <div class="shapes" id="shapes">{shapes}</div>
  <h3 class="sub">/ Motion</h3>
  <p class="note">Springs, not durations. Hover or tap a row: spatial springs overshoot, effects springs never do. See the <a href="{u('docs/motion')}">motion recipes</a>.</p>
  <div class="motions">{motion_rows}</div>
</div></section>"""


def inline_md(text):
    return re.sub(r"^<p>|</p>$", "", MD(text).strip())


def css(n):
    return n.replace(".", "\\.")


def home(comps):
    n = len(comps)
    hero = f"""
<section class="hero"><div class="wrap">
  <h1 aria-label="Expressive Kit">
    <span class="l1">Expressive</span>
    <span class="l2">K<span class="i-pill"></span>t</span>
    {shape_svg("sunny", "float f1")}{shape_svg("burst", "float f2")}
  </h1>
  <div class="hero-base">
    <div class="count"><span class="big">{n}</span><span class="mono">/ live components</span></div>
    <div class="portrait">
      {shape_svg("burst", "p-burst")}
      <img class="only-light" src="{u('assets/hero-light.png')}" alt="Expressive Kit components on a phone screen: stat tiles, a tonal card with wavy progress, a connected button group and a list row." width="680" height="640">
      <img class="only-dark" src="{u('assets/hero-dark.png')}" alt="Expressive Kit components on a phone screen in the dark theme." width="680" height="640">
    </div>
    <div class="hero-ctas">
      <div class="ex-row">
        <a class="ex-press ex-btn v-filled" href="{u(SKILL_ZIP)}" download><span class="ex-icon" aria-hidden="true">download</span>Download skill</a>
        <a class="ex-press ex-btn v-outlined" href="{u('docs/skill')}">Read SKILL.md</a>
      </div>
      <span class="mono">/ teach any AI to design</span>
    </div>
  </div>
</div></section>

<section class="intro"><div class="wrap">
  <h2>One kit. {shape_svg("flower8", "hi")}</h2>
  <div class="intro-grid">
    <p class="intro-lead">A Material 3 Expressive design system that an AI can <span class="em">read</span> before it designs.</p>
    <div class="intro-body">
      <p>Tokens, {n} React components, a Jetpack Compose theme and a skill file, all built from the same colour roles, type scale, shapes and springs.</p>
      <p>It is the kit behind every app on <a href="{HOME_URL}">dinoyraj.com</a>, so the shapes, colours and motion stay consistent from the first screen to the last.</p>
      <a class="go-chip" href="{u('docs/brand-book')}">Read the brand book<span class="ex-icon" aria-hidden="true">arrow_outward</span></a>
    </div>
  </div>
</div></section>

<section class="statement"><div class="wrap">
  <p data-lit>Every colour is a role, not a hex. Motion runs on <span class="hl">springs</span>, not durations. Shapes morph, pressed corners tighten, and the same tokens drive the web and Compose.</p>
</div></section>

<section class="sec" id="start"><div class="wrap">
  {sec_head("Get started", "Four ways in")}
  <div class="rows">
    <div class="row"><span class="row-ic" data-ws="flower5" data-icon="auto_awesome" data-tone="primary-container"></span><div><h3>As an AI skill</h3><p>Download the skill and upload it to Claude (Settings, Capabilities, Skills) or unzip it into <code>~/.claude/skills/</code> for Claude Code. Other AI tools can read <code>SKILL.md</code> directly.</p></div><a class="row-go" href="{u(SKILL_ZIP)}" download>Download skill<span class="ex-icon" aria-hidden="true">download</span></a></div>
    <div class="row"><span class="row-ic" data-ws="clover4" data-icon="palette" data-tone="tertiary-container"></span><div><h3>As a Claude design system</h3><p>Ask Claude to create a design system from this repository. <code>tokens/tokens.json</code>, <code>components/bundle.*</code> and each <code>preview.html</code> already follow Claude's design system format.</p></div><a class="row-go" href="{u('docs/skill')}#import">How to import<span class="ex-icon" aria-hidden="true">arrow_outward</span></a></div>
    <div class="row"><span class="row-ic" data-ws="cookie9" data-icon="code" data-tone="secondary-container"></span><div><h3>On the web</h3><p>Link <code>tokens/tokens.css</code> and <code>components/bundle.css</code>, load React 18 and <code>components/bundle.js</code>, then use <code>window.Expressive</code>.</p></div><a class="row-go" href="{u('examples/gallery')}">Open gallery<span class="ex-icon" aria-hidden="true">arrow_outward</span></a></div>
    <div class="row"><span class="row-ic" data-ws="sunny" data-icon="android" data-tone="highlight"></span><div><h3>On Android</h3><p>Copy <code>android/ExpressiveTheme.kt</code> into your app and wrap your UI in <code>ExpressiveTheme {{ }}</code>.</p></div><a class="row-go" href="{u('android/ExpressiveTheme.kt')}">View theme<span class="ex-icon" aria-hidden="true">arrow_outward</span></a></div>
  </div>
</div></section>"""

    cards = "".join(
        f'<article class="c-card" id="c-{c["name"]}"><div class="c-live" id="live-{c["name"]}"></div>'
        f'<div class="c-meta"><h3><a href="{u("docs/components/" + c["name"])}">{c["name"]}</a></h3><span class="tag">{c["group"]}</span></div>'
        f'<p>{inline_md(c["summary"])}</p></article>' for c in comps)
    comp_sec = f"""
<section class="sec" id="components"><div class="wrap">
  {sec_head(f"{len(comps)} live, press them", "Components", "Press them: pills tighten their corners, selections round into full pills, the loading indicator morphs through the shape library.",
            f'<a class="go-chip ink" href="{u("examples/gallery")}">Open gallery<span class="ex-icon" aria-hidden="true">arrow_outward</span></a>')}
  <div class="c-grid">{cards}</div>
</div></section>"""

    guide_cards = "".join(
        f'<a class="guide" href="{u("docs/" + slug)}"><span class="g-art t-{tone}">{shape_svg(shape)}</span>'
        f'<span class="mono">Guide · {i + 1:02d}</span><h3>{title}</h3><p>{blurb}</p></a>'
        for i, (slug, _label, title, blurb, shape, tone) in enumerate(DOCS[1:]))
    guides = f"""
<section class="sec" id="guides"><div class="wrap">
  {sec_head("Read", "Guides")}
  <div class="guides">
    <a class="guide dark" href="{u('docs/skill')}"><span class="mono">Start here · SKILL.md</span><h3>Everything an AI needs to design in this style, in one file.</h3><span class="go-chip">Read SKILL.md<span class="ex-icon" aria-hidden="true">arrow_outward</span></span></a>
    {guide_cards}
  </div>
</div></section>"""

    renders = "\n".join(f"  ReactDOM.createRoot(document.getElementById('live-{c['name']}')).render({c['js']});" for c in comps)
    shapes_js = "  document.querySelectorAll('[data-shape]').forEach(function (el) { ReactDOM.createRoot(el).render(h(E.ShapeAvatar, { shape: el.dataset.shape, size: 64, tone: ['primary-container','secondary-container','tertiary-container','highlight'][Array.prototype.indexOf.call(el.parentNode.children, el) % 4], label: el.dataset.shape })); });"
    ways_js = "  document.querySelectorAll('[data-ws]').forEach(function (el) { ReactDOM.createRoot(el).render(h(E.ShapeAvatar, { shape: el.dataset.ws, size: 48, icon: el.dataset.icon, tone: el.dataset.tone })); });"
    lit_js = """  (function () {
    var p = document.querySelector('[data-lit]'); if (!p) return;
    p.innerHTML = p.innerHTML.replace(/(<span class="hl">)?([^\\s<>]+)(<\\/span>)?/g, function (m, a, w) { return '<span class="w' + (a ? ' hl' : '') + '">' + w + '</span>'; });
    var words = p.querySelectorAll('.w');
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) { words.forEach(function (w) { w.classList.add('on'); }); return; }
    function tick() { var r = p.getBoundingClientRect(), vh = innerHeight, f = (vh * .85 - r.top) / (r.height + vh * .35); words.forEach(function (w, i) { w.classList.toggle('on', i < f * words.length); }); }
    addEventListener('scroll', tick, { passive: true }); addEventListener('resize', tick); tick(); p.classList.add('ready');
  })();"""
    return hero + foundations() + comp_sec + guides, "\n".join([ways_js, shapes_js, lit_js, renders])


# Build ----------------------------------------------------------------------------------------------------------------

def doc_page(eyebrow, title, inner, back=None):
    back_html = f'<a class="go-chip back" href="{back[1]}"><span class="ex-icon" aria-hidden="true">arrow_back</span>{back[0]}</a>' if back else ""
    return f"""<section class="doc-hero"><div class="wrap"><div class="mono">/ {eyebrow}</div><h1 class="sec-title">{html.escape(title)}</h1></div></section>
<article class="wrap s-doc">{inner}{back_html}</article>"""


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

    body, js = home(comps)
    (OUT / "index.html").write_text(page("Expressive Kit | Material 3 Expressive design system and AI skill", body, "", scripts=js))

    # Docs pages
    skill = re.sub(r"^---.*?---\s*", "", (ROOT / "SKILL.md").read_text(), flags=re.S)
    skill = re.sub(r"^# .*\n+", "", skill)
    import_md = f"""
## Import into Claude {{#import}}

**As a skill.** Download [{SKILL_ZIP}]({u(SKILL_ZIP)}). In the Claude app, open Settings, then Capabilities, and upload it under Skills. In Claude Code, unzip it into `~/.claude/skills/` (personal) or `.claude/skills/` in a project.

**As a design system.** In a Claude conversation that can read this repository, ask: "Create a design system from {REPO_URL}". The repository already matches Claude's design system format: `tokens/tokens.json` is the token file, `components/bundle.js` (namespace `Expressive`, React 18) and `components/bundle.css` are the live bundle, each `components/<Name>/preview.html` is a component card, `components/<Name>/README.md` its guideline, `components/Cover/preview.html` the cover, and `docs/brand-book.md` the brand book.

**Any other AI tool.** Point it at `SKILL.md`; it links to every other file it needs.
"""
    sources = {"skill": skill + import_md}
    for slug, _label, title, blurb, *_ in DOCS:
        text = sources.get(slug) or re.sub(r"^# .*\n+", "", (ROOT / "docs" / f"{slug}.md").read_text())
        inner = MD(text).replace("{#import}", "").replace("<h2>Import into Claude", '<h2 id="import">Import into Claude')
        (OUT / "docs" / f"{slug}.html").write_text(page(f"{title} · Expressive Kit", doc_page("Guide", title, inner, ("Back to the kit", u() + "#guides")),
                                                        f"docs/{slug}", description=blurb))
    for c in comps:
        inner = f'<div class="c-card c-solo"><div class="c-live" id="live"></div></div>\n{MD(c["readme"])}'
        js = f"  ReactDOM.createRoot(document.getElementById('live')).render({c['js']});"
        (OUT / "docs" / "components" / f"{c['name']}.html").write_text(
            page(f"{c['name']} · Expressive Kit", doc_page(c["group"], c["name"], inner, ("All components", u() + "#components")),
                 f"docs/components/{c['name']}", description=re.sub(r"<[^>]+>", "", inline_md(c["summary"])), scripts=js))
    (OUT / ".nojekyll").write_text("")
    print(f"Built _site/ with {len(comps)} components and {SKILL_ZIP} (base {BASE})")


if __name__ == "__main__":
    build()
