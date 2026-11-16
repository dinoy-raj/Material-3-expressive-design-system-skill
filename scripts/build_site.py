#!/usr/bin/env python3
"""Build the website into _site/.

Run after scripts/build.py:  python3 scripts/build_site.py
Needs the `markdown` package (pip install markdown).

The site is published by GitHub Pages at dinoy-raj.github.io/material-3-expressive-skill/ and served on
dinoyraj.com/material-3-expressive-skill through a Vercel rewrite in the portfolio-website repository.
Both hosts use the same path prefix, so every link is root-absolute under BASE and works on either host, with or
without a trailing slash. Page links have no `.html`: GitHub Pages and Vercel both resolve them.

The look and motion follow dinoyraj.com: a floating dark island nav, a progressive blur band under it, poster headlines
in Google Sans Flex that rise out of a blur, blur-in scroll reveals, spring press feedback, grouped rows with small inner
corners and a dark footer whose giant wordmark reacts to the pointer. Behaviour lives in scripts/site.js, layout in
scripts/site.css. Every page carries canonical, Open Graph, Twitter and JSON-LD metadata, and the build writes
sitemap.xml, llms.txt and a 404 page.
"""
import datetime
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
VERSION = json.loads((ROOT / "package.json").read_text())["version"]
TODAY = datetime.date.today().isoformat()
OG_IMAGE = CANONICAL + "/assets/og.png"
AUTHOR = {"@type": "Person", "name": "Dinoy Raj", "url": HOME_URL, "sameAs": ["https://github.com/dinoy-raj", "https://x.com/dinoy_raj"]}

MD = lambda text: markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "toc"])

DOCS = [  # slug, nav label, page title, card blurb, card shape, card tone, SEO title
    ("skill", "Skill", "SKILL.md", "The skill file itself: the rules an AI follows to design in this style, and how to import it.", "cookie9", "primary",
     "Material 3 Expressive Skill (SKILL.md) for Claude and AI tools"),
    ("brand-book", "Brand book", "Brand book", "Voice, colour, type and shape: the decisions behind every token.", "flower8", "tertiary",
     "Material 3 Expressive Brand Book: colour, type and shape"),
    ("motion", "Motion", "Motion recipes", "Springs, not durations. Recipes for press, morph and reveal on the web and in Compose.", "sunny", "highlight",
     "Material 3 Expressive Motion: spring recipes for web and Compose"),
    ("screen-patterns", "Patterns", "Screen patterns", "Whole screens assembled from the parts: dashboards, settings, detail and empty states.", "clover4", "secondary",
     "Material 3 Expressive Screen Patterns: dashboards, settings, empty states"),
    ("seed-palettes", "Palettes", "Seed palettes", "Swap one seed colour and rebuild every role in light and dark.", "softBurst", "primary",
     "Material 3 Expressive Seed Palettes: light and dark colour roles"),
    ("accessibility", "Accessibility", "Accessibility", "Touch targets, gesture alternatives, screen readers, font scaling, right-to-left and localization.", "burst", "secondary",
     "Material 3 Expressive Accessibility: targets, font scaling, RTL"),
    ("existing-projects", "Existing apps", "Existing projects", "Bring M3 Expressive into an app that already has a theme, without replacing its brand or libraries.", "cookie4", "tertiary",
     "Adopting Material 3 Expressive in an existing app"),
    ("platforms", "Platforms", "Platforms", "Compose, web, Views, Wear OS, Flutter, React Native and SwiftUI, with spring conversions and sources.", "cookie9", "highlight",
     "Material 3 Expressive on Compose, Flutter, React Native and SwiftUI"),
    ("review", "Review", "Reviewing a design", "An audit checklist with severities, a finding format and a verdict.", "flower8", "primary",
     "Material 3 Expressive Design Review Checklist"),
]
FIT_MIN = {"NavigationRail": 500, "TimePickerDial": 340}  # demos that need a wider layout box before they are scaled to fit
GROUPS = ["Actions", "Selection", "Inputs", "Navigation", "Containment", "Status", "Identity"]
SKILL_FOLDERS = ("tokens", "docs", "components", "android", "templates")  # keep in sync with scripts/validate_skill.py

FAQ = [
    ("What is Material 3 Expressive?",
     "Material 3 Expressive (M3E) is Google's 2025 evolution of Material Design 3. It adds expressive shape morphing, spring-based motion, "
     "emphasized type and new components such as connected button groups, split buttons, floating toolbars, the morphing loading indicator and wavy progress."),
    ("What is the Material 3 Expressive skill?",
     "It is an Agent Skill: a SKILL.md file plus the tokens, guidelines and component references it links to. Give it to Claude or another AI tool "
     "and it designs, builds and reviews screens in the Material 3 Expressive style instead of generic Material defaults."),
    ("How do I install the skill in Claude or Claude Code?",
     f"Download {SKILL_ZIP} from this page. In the Claude apps, open Settings, then Capabilities, and upload it under Skills. "
     "In Claude Code, unzip it into ~/.claude/skills/ for every project or .claude/skills/ for one project."),
    ("Does it work with Jetpack Compose?",
     "Yes. android/ExpressiveTheme.kt is generated from the same tokens and wraps MaterialExpressiveTheme with the expressive motion scheme, "
     "emphasized type, dynamic colour and true black, alongside motion helpers and extra components."),
    ("Can I use the components on the web?",
     "Yes. Link tokens/tokens.css and components/bundle.css, load React 18 and components/bundle.js, then use window.Expressive. "
     "All 29 components on this page are that bundle running live."),
    ("Does it work with AI tools other than Claude?",
     "Yes. Add SKILL.md to the tool's rules or context. It links to every token, guideline and component file it needs, so any assistant that reads files can follow it."),
    ("Is Expressive Kit free?",
     "Yes. It is open source under the MIT license. Material Design and Jetpack Compose are trademarks of Google LLC; this project isn't affiliated with or endorsed by Google."),
]


def u(path=""):
    """Root-absolute URL for a path inside the site."""
    return BASE + path if path else (BASE.rstrip("/") or "/")


def esc(s):
    return html.escape(s, quote=True)


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def components():
    items = []
    for d in sorted((ROOT / "components").iterdir()):
        prev, readme = d / "preview.html", d / "README.md"
        if d.name == "Cover" or not prev.is_file():
            continue
        src = prev.read_text()
        js = re.search(r"\.render\((.*)\);\s*</script>", src, re.S).group(1)
        group = re.search(r'group="([^"]+)"', src).group(1)
        height = int((re.search(r"height=(\d+)", src) or [0, 240])[1])
        body = readme.read_text() if readme.is_file() else ""
        body = re.sub(r"^# .*\n+", "", body)
        summary = re.split(r"(?<=\.)\s", body.strip(), maxsplit=1)[0]
        items.append({"name": d.name, "group": group, "js": js, "summary": summary, "readme": body, "height": height,
                      "label": re.sub(r"(?<=[a-z])(?=[A-Z])", " ", d.name)})
    items.sort(key=lambda c: c["name"])
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
          "clover4": blob(4, .22, .6), "softBurst": blob(10, .12, 1.3), "cookie4": blob(4, .12), "cookie6": blob(6, .1)}


def shape_svg(name, cls="", box="-1.05 -1.05 2.1 2.1"):
    return f'<svg class="{cls}" viewBox="{box}" aria-hidden="true" focusable="false"><path d="{SHAPES[name]}"/></svg>'


def icon(name, cls=""):
    return f'<span class="ex-icon {cls}" aria-hidden="true">{name}</span>'


# SEO ------------------------------------------------------------------------------------------------------------------

def crumbs_ld(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": url} for i, (name, url) in enumerate(crumbs)]}


def jsonld(graph):
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    data = data.replace("</", "<\\/")
    return f'<script type="application/ld+json">{data}</script>'


# Page shell -----------------------------------------------------------------------------------------------------------

def page(title, body, path="", description="", scripts="", ld=None, og_type="website", preload=""):
    canonical = CANONICAL + ("/" + path if path else "/")
    nav = [("Overview", u() + "#top"), ("Foundations", u() + "#foundations"), ("Components", u() + "#components"),
           ("Gallery", u("gallery")), ("Guides", u() + "#guides"), ("FAQ", u() + "#faq")]
    links = "".join(
        f'<a class="lnk rv" style="--i:{i}" href="{href}"><span><span class="num">{i + 1:02d}</span>{name}</span>'
        f'<span class="go">{shape_svg("flower8")}{icon("arrow_outward")}</span></a>'
        for i, (name, href) in enumerate(nav))
    ld_html = jsonld(ld) if ld else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#fbf6ee" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#16120f" media="(prefers-color-scheme: dark)">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="author" content="Dinoy Raj">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="keywords" content="Material 3 Expressive, M3 Expressive, M3E, Material 3 Expressive skill, Claude skill, Agent Skill, design system, design tokens, Jetpack Compose theme, React components, spring motion, shape morphing">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Expressive Kit by Dinoy Raj">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Expressive Kit: a Material 3 Expressive design system and AI skill">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@dinoy_raj">
<meta name="twitter:creator" content="@dinoy_raj">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='-1 -1 2 2'%3E%3Cpath fill='%23a8330f' d='{SHAPES['cookie9']}'/%3E%3C/svg%3E">
<link rel="apple-touch-icon" href="{u('assets/touch-icon.png')}">
<link rel="sitemap" type="application/xml" href="{u('sitemap.xml')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
{preload}<script>(function(d){{d.classList.add('js');try{{var t=localStorage.getItem('ek-theme')||'light';if(t!=='system')d.dataset.theme=t;}}catch(e){{d.dataset.theme='light';}}if(matchMedia('(prefers-reduced-motion: reduce)').matches)d.classList.add('rm');}})(document.documentElement);</script>
<link rel="stylesheet" href="{u('tokens/tokens.css')}">
<link rel="stylesheet" href="{u('components/bundle.css')}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:opsz,wdth,wght@6..144,25..151,100..1000&display=swap">
<link rel="stylesheet" href="{u('site.css')}?v={VERSION}">
{ld_html}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="top-blur" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>
<div class="nav-scrim" hidden></div>
<header class="nav">
  <div class="nav-row">
    <a class="nav-name" href="{u()}">Expressive <span>Kit</span></a>
    <button type="button" class="menu-btn" aria-expanded="false" aria-controls="nav-panel" aria-label="Open menu">
      <svg viewBox="-1.15 -1.15 2.3 2.3" aria-hidden="true"><path d="{SHAPES['cookie4']}"/></svg>
      {icon("more_horiz", "i-more")}{icon("close", "i-close")}
    </button>
  </div>
  <div class="nav-panel" id="nav-panel" inert>
    <nav aria-label="Site">{links}</nav>
    <div class="nav-foot rv" style="--i:{len(nav)}">
      <div class="theme" role="group" aria-label="Theme">
        <button type="button" data-t="system" aria-label="Automatic theme">{icon("contrast")}</button>
        <button type="button" data-t="light" aria-label="Light theme">{icon("light_mode")}</button>
        <button type="button" data-t="dark" aria-label="Dark theme">{icon("dark_mode")}</button>
      </div>
      <a href="{REPO_URL}" rel="noopener">GitHub {icon("arrow_outward")}</a>
    </div>
  </div>
</header>
<main id="main">
{body}
</main>
{footer()}
<div class="toast" role="status" aria-live="polite"></div>
<script src="https://cdn.jsdelivr.net/npm/react@18.3.1/umd/react.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/react-dom@18.3.1/umd/react-dom.production.min.js"></script>
<script src="{u('components/bundle.js')}"></script>
<script>
  var E = window.Expressive, h = React.createElement;
  function mount(id, el) {{ var n = document.getElementById(id); if (n) ReactDOM.createRoot(n).render(el); }}
{scripts}
</script>
<script src="{u('site.js')}?v={VERSION}"></script>
</body>
</html>
"""


def footer():
    quick = "".join(f'<a href="{href}">{name}</a>' for name, href in
                    [("Overview", u() + "#top"), ("Get started", u() + "#start"), ("Foundations", u() + "#foundations"),
                     ("Components", u() + "#components"), ("Gallery", u("gallery")), ("FAQ", u() + "#faq")])
    docs = "".join(f'<a href="{u("docs/" + slug)}">{label}</a>' for slug, label, *_ in DOCS)
    ext = "".join(f'<a href="{href}"{attrs}>{name}</a>' for name, href, attrs in
                  [("Source on GitHub", REPO_URL, ' rel="noopener"'), ("Download skill", u(SKILL_ZIP), " download"),
                   ("Compose theme", u("android/ExpressiveTheme.kt"), ""), ("llms.txt", u("llms.txt"), "")])
    letters = "".join(f'<span class="wm-l" style="--i:{i}" data-t="{c}"></span>' for i, c in enumerate("EXPRESSIVE"))
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
    <span>© 2026 Dinoy Raj · Expressive Kit v{VERSION} · MIT · Not affiliated with Google</span>
    <a class="kit" href="{HOME_URL}"><span class="kit-dot" aria-hidden="true">{shape_svg("softBurst")}{icon("waving_hand")}</span><span>More from <b>Dinoy</b></span>{icon("arrow_outward", "kit-go")}</a>
  </div>
</footer>"""


# Home sections --------------------------------------------------------------------------------------------------------

def sec_head(eyebrow, title, lede="", extra=""):
    lede_html = f'<p class="sec-lede">{lede}</p>' if lede else ""
    return (f'<div class="sec-head"><div><div class="mono" data-rv>/ {eyebrow}</div><h2 class="sec-title" data-rv style="--d:1">{title}</h2>'
            f'<div data-rv style="--d:2">{lede_html}</div></div>{extra}</div>')


def inline_md(text):
    return re.sub(r"^<p>|</p>$", "", MD(text).strip())


def css(n):
    return n.replace(".", "\\.")


def foundations():
    sw = []
    for c in TOKENS["color"]["tokens"]:
        if c["name"] in ("scrim", "focus"):
            continue
        sw.append(f'<button type="button" class="sw tap" data-copy="var(--{c["name"]})"><span class="chip" style="background:var(--{c["name"]})"></span>'
                  f'<span class="n">{c["name"]}</span><span class="hex" data-var="--{c["name"]}"></span></button>')
    type_rows = []
    for g in TOKENS["type"]["groups"]:
        for s in g["styles"]:
            type_rows.append(f'<div class="ty"><span class="meta">{s["name"]}<br>{s["fontSize"]} / {s["lineHeight"]} · {s["fontWeight"]}</span>'
                             f'<span class="{s["name"]}">{esc(s.get("sample", s["name"]))}</span></div>')
    radii = "".join(f'<div class="rad tap"><span style="border-radius:var(--{r["name"]})"></span>{r["name"]}<em>{r["value"]}</em></div>' for r in TOKENS["radius"]["tokens"])
    space = "".join(f'<div class="sp"><span style="width:var(--{css(s["name"])})"></span>{s["name"]}<em>{s["value"]}</em></div>' for s in TOKENS["spacing"]["tokens"])
    shape_names = ["circle", "cookie4", "cookie6", "cookie7", "cookie9", "cookie12", "clover4", "clover8", "flower5", "flower8", "sunny",
                   "softBurst", "burst", "boom", "pebble", "puffy", "square", "pill", "oval", "diamond", "triangle", "pentagon", "gem", "heart", "arch"]
    shapes = "".join(f'<div class="shp" data-shape="{n}"><span class="shp-art"></span><span class="shp-n">{n}</span></div>' for n in shape_names)
    motion_rows = "".join(
        f'<button type="button" class="mo"><span class="meta">{t["name"]}<br>{t["dampingRatio"]} / {t["stiffness"]}</span>'
        f'<span class="mo-track"><span class="mo-ball" style="transition: transform var(--motion-{t["name"]}), background-color var(--motion-{t["name"]})"></span></span></button>'
        for t in TOKENS["motion"]["schemes"][0]["tokens"])
    tabs = [("colour", "Colour", "palette"), ("type", "Type", "text_fields"), ("shape", "Shape", "interests"),
            ("motion", "Motion", "animation"), ("space", "Corners & space", "rounded_corner")]
    tab_btns = "".join(f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}">'
                       f'{icon(ic)}<span>{label}</span></button>' for i, (k, label, ic) in enumerate(tabs))
    panels = {
        "colour": f'<p class="note">Every colour is a role, not a hex. Flip the theme from the menu and watch each swatch change. Tap a swatch to copy its variable.</p><div class="swatches">{"".join(sw)}</div>',
        "type": f'<p class="note">Google Sans Flex for interface text, Fraunces for display moments, Google Sans Code for data. Every style has an emphasized twin.</p><div class="types">{"".join(type_rows)}</div>',
        "shape": f'<p class="note">Cut avatars, hero seats and masks from these. Hover or tap a shape: any shape can morph into any other.</p><div class="shapes" id="shapes">{shapes}</div>',
        "motion": f'<p class="note">Springs, not durations. Tap a row: spatial springs overshoot, effects springs never do. See the <a href="{u("docs/motion")}">motion recipes</a>.</p><div class="motions">{motion_rows}</div>',
        "space": f'<div class="two"><div><h3 class="sub">/ Corner shapes</h3><div class="radii">{radii}</div></div><div><h3 class="sub">/ Spacing</h3><div class="spaces">{space}</div></div></div>',
    }
    panel_html = "".join(f'<div class="panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}" tabindex="0"{"" if i == 0 else " hidden"}>{panels[k]}</div>'
                         for i, (k, *_r) in enumerate(tabs))
    return f"""
<section class="sec" id="foundations" aria-labelledby="foundations-title"><div class="wrap">
  {sec_head("Design tokens", '<span id="foundations-title">Foundations</span>', "36 colour roles in light and dark, a 21-style type scale, M3 corner shapes, a 25-shape library and spring motion tokens, all from one tokens.json.")}
  <div class="tabs" data-rv style="--d:3"><div class="tablist" role="tablist" aria-label="Foundations"><span class="tab-ind" aria-hidden="true"></span>{tab_btns}</div></div>
  <div class="panels" data-rv style="--d:4">{panel_html}</div>
</div></section>"""


def comp_card(c, i, big=False):
    group = c["group"]
    tools = ""
    if big:
        tools = (f'<div class="cc-tools"><button type="button" class="ib tap" data-theme-toggle aria-label="Show {c["label"]} in the other theme">{icon("contrast")}</button>'
                 f'<button type="button" class="ib tap" data-copy-code="code-{c["name"]}" aria-label="Copy {c["label"]} code">{icon("content_copy")}</button></div>'
                 f'<script type="text/plain" id="code-{c["name"]}">{esc(c["js"].strip())}</script>')
    return (f'<article class="cc spot" data-group="{group}" data-name="{c["name"].lower()} {c["label"].lower()} {group.lower()}" data-rv style="--d:{i % 3}">'
            f'<div class="cc-stage"><div class="fit" id="live-{c["name"]}"{fit_style(c)}></div>{tools}</div>'
            f'<div class="cc-body"><div class="cc-top"><span class="mono">{i + 1:02d}</span><span class="tag">{group}</span></div>'
            f'<h3><a href="{u("docs/components/" + c["name"])}">{c["label"]}</a></h3>'
            f'<p>{inline_md(c["summary"])}</p>'
            f'<a class="cc-go" href="{u("docs/components/" + c["name"])}" aria-label="{c["label"]} docs" tabindex="-1">{icon("arrow_outward")}</a></div></article>')


def fit_style(c):
    return f' style="--fit-min:{FIT_MIN[c["name"]]}px"' if c["name"] in FIT_MIN else ""


def filters(comps, search=False):
    counts = {g: sum(1 for c in comps if c["group"] == g) for g in GROUPS}
    chips = [f'<button type="button" class="fchip tap" data-f="all" aria-pressed="true">All<span>{len(comps)}</span></button>'] + \
            [f'<button type="button" class="fchip tap" data-f="{g}" aria-pressed="false">{g}<span>{n}</span></button>' for g, n in counts.items() if n]
    box = (f'<label class="search">{icon("search")}<input type="search" placeholder="Search components" aria-label="Search components" data-search>'
           f'</label>') if search else ""
    return f'<div class="filters" data-rv style="--d:3">{box}<div class="fchips" role="group" aria-label="Filter components by group">{"".join(chips)}</div></div>'


def faq_html():
    items = "".join(
        f'<details class="qa" data-rv style="--d:{i % 3}"><summary><h3>{esc(q)}</h3><span class="qa-ic" aria-hidden="true">{shape_svg("cookie6")}{icon("add")}</span></summary>'
        f'<div class="qa-a"><p>{esc(a)}</p></div></details>' for i, (q, a) in enumerate(FAQ))
    return f"""
<section class="sec" id="faq" aria-labelledby="faq-title"><div class="wrap faq-wrap">
  <div class="faq-side">{sec_head("Questions", '<span id="faq-title">FAQ</span>', "Everything people ask before they hand the kit to their AI or their app.")}</div>
  <div class="qas">{items}</div>
</div></section>"""


def home(comps):
    n = len(comps)
    letters = "".join(f'<span class="ch" style="--i:{i}">{c}</span>' for i, c in enumerate("EXPRESSIVE"))
    ticker_items = ["Material 3 Expressive", "Spring motion", "Shape morphing", "Design tokens", "Jetpack Compose", "React 18",
                    "AI skill", "Button groups", "Wavy progress", "Split buttons", "Emphasized type", "Dynamic colour"]
    shapes_cycle = ["sunny", "flower8", "burst", "clover4", "cookie9", "softBurst"]
    tick = "".join(f'<span class="tk">{t}</span>{shape_svg(shapes_cycle[i % len(shapes_cycle)], "tk-s t" + str(i % 4))}' for i, t in enumerate(ticker_items))
    hero = f"""
<section class="hero" id="top"><div class="wrap">
  <p class="hero-eyebrow"><span class="dot" aria-hidden="true"></span>Material 3 Expressive · skill + design system<span class="ver"> · v{VERSION}</span></p>
  <h1 class="poster">
    <span class="sr">Expressive Kit: the Material 3 Expressive skill and design system</span>
    <span class="l1" aria-hidden="true">{letters}</span>
    <span class="l2" aria-hidden="true"><span class="ch" style="--i:10">K</span><span class="i-pill"></span><span class="ch" style="--i:12">T</span></span>
    <span class="float f1" data-par="-0.18">{shape_svg("sunny")}</span><span class="float f2" data-par="0.12">{shape_svg("burst")}</span>
  </h1>
  <div class="hero-base">
    <div class="count"><span class="big" data-count="{n}">{n}</span><span class="mono">/ live components</span></div>
    <div class="portrait" tabindex="-1">
      <span class="p-burst" data-par="-0.08">{shape_svg("burst")}</span>
      <span class="p-spark">{shape_svg("sunny")}</span>
      <div class="frame">
        <img class="only-light" src="{u('assets/hero-light.png')}" alt="Expressive Kit components on a phone screen: stat tiles, a tonal card with wavy progress, a connected button group and a list row." width="680" height="640" fetchpriority="high">
        <img class="only-dark" src="{u('assets/hero-dark.png')}" alt="Expressive Kit components on a phone screen in the dark theme." width="680" height="640" loading="lazy">
      </div>
    </div>
    <div class="hero-ctas">
      <div class="ex-row">
        <a class="ex-press ex-btn v-filled tap" href="{u(SKILL_ZIP)}" download>{icon("download")}Download skill</a>
        <a class="ex-press ex-btn v-outlined tap" href="{u('docs/skill')}">Read SKILL.md</a>
      </div>
      <span class="mono">/ teach any AI to design</span>
    </div>
  </div>
</div></section>

<div class="ticker" aria-hidden="true"><div class="tk-track">{tick}{tick}</div></div>

<section class="intro"><div class="wrap">
  <h2 data-rv>One kit. {shape_svg("flower8", "hi")}</h2>
  <div class="intro-grid">
    <p class="intro-lead" data-rv style="--d:1">A Material 3 Expressive design system that an AI can <span class="em">read</span> before it designs.</p>
    <div class="intro-body" data-rv style="--d:2">
      <p>Tokens, {n} React components, a Jetpack Compose theme and a skill file, all built from the same colour roles, type scale, shapes and springs.</p>
      <p>It is the kit behind every app on <a href="{HOME_URL}">dinoyraj.com</a>, so the shapes, colours and motion stay consistent from the first screen to the last.</p>
      <a class="go-chip tap" href="{u('docs/brand-book')}">Read the brand book{icon("arrow_outward")}</a>
    </div>
  </div>
  <div class="stats">
    <div class="stat tap" data-rv><span class="stat-n" data-count="36">36</span><span>colour roles, light and dark, every text pair WCAG AA</span></div>
    <div class="stat tap" data-rv style="--d:1"><span class="stat-n" data-count="21">21</span><span>type styles, each with an emphasized twin</span></div>
    <div class="stat tap" data-rv style="--d:2"><span class="stat-n" data-count="25">25</span><span>shapes that morph into one another</span></div>
    <div class="stat tap" data-rv style="--d:3"><span class="stat-n" data-count="{n}">{n}</span><span>live React components, plus a Compose theme</span></div>
  </div>
</div></section>

<section class="statement"><div class="wrap">
  <p data-lit>Every colour is a role, not a hex. Motion runs on <span class="hl">springs</span>, not durations. Shapes morph, pressed corners tighten, and the same tokens drive the web and Compose.</p>
</div></section>

<section class="sec" id="start" aria-labelledby="start-title"><div class="wrap">
  {sec_head("Get started", '<span id="start-title">Four ways in</span>')}
  <div class="rows">
    <div class="row" data-rv><span class="row-ic" data-ws="flower5" data-icon="auto_awesome" data-tone="primary-container"></span><div><h3>As an AI skill</h3><p>Download the skill and upload it to Claude (Settings, Capabilities, Skills) or unzip it into <code>~/.claude/skills/</code> for Claude Code. Other AI tools can read <code>SKILL.md</code> directly.</p></div><a class="row-go tap" href="{u(SKILL_ZIP)}" download>Download skill{icon("download")}</a></div>
    <div class="row" data-rv style="--d:1"><span class="row-ic" data-ws="clover4" data-icon="palette" data-tone="tertiary-container"></span><div><h3>As a Claude design system</h3><p>Ask Claude to create a design system from this repository. <code>tokens/tokens.json</code>, <code>components/bundle.*</code> and each <code>preview.html</code> already follow Claude's design system format.</p></div><a class="row-go tap" href="{u('docs/skill')}#import">How to import{icon("arrow_outward")}</a></div>
    <div class="row" data-rv style="--d:2"><span class="row-ic" data-ws="cookie9" data-icon="code" data-tone="secondary-container"></span><div><h3>On the web</h3><p>Link <code>tokens/tokens.css</code> and <code>components/bundle.css</code>, load React 18 and <code>components/bundle.js</code>, then use <code>window.Expressive</code>.</p></div><a class="row-go tap" href="{u('gallery')}">Open gallery{icon("arrow_outward")}</a></div>
    <div class="row" data-rv style="--d:3"><span class="row-ic" data-ws="sunny" data-icon="android" data-tone="highlight"></span><div><h3>On Android</h3><p>Copy <code>android/ExpressiveTheme.kt</code> into your app and wrap your UI in <code>ExpressiveTheme {{ }}</code>.</p></div><a class="row-go tap" href="{u('android/ExpressiveTheme.kt')}">View theme{icon("arrow_outward")}</a></div>
  </div>
</div></section>"""

    cards = "".join(comp_card(c, i) for i, c in enumerate(comps))
    comp_sec = f"""
<section class="sec" id="components" aria-labelledby="components-title"><div class="wrap">
  {sec_head(f"{n} live components", '<span id="components-title">Components</span>', "Every card is the real React bundle. Press them: pills tighten their corners, selections round into full pills, the loading indicator morphs through the shape library.",
            f'<a class="go-chip ink tap" href="{u("gallery")}" data-rv style="--d:2">Open gallery{icon("arrow_outward")}</a>')}
  {filters(comps)}
  <div class="c-grid" data-grid>{cards}</div>
  <p class="empty" hidden>No components match.</p>
</div></section>"""

    guide_cards = "".join(
        f'<a class="guide spot tap" href="{u("docs/" + slug)}" data-rv style="--d:{(i + 1) % 4}"><span class="g-art t-{tone}">{shape_svg(shape)}</span>'
        f'<span class="mono">Guide · {i + 1:02d}</span><h3>{title}</h3><p>{blurb}</p></a>'
        for i, (slug, _label, title, blurb, shape, tone, _seo) in enumerate(DOCS[1:]))
    guides = f"""
<section class="sec" id="guides" aria-labelledby="guides-title"><div class="wrap">
  {sec_head("Read", '<span id="guides-title">Guides</span>', "The decisions behind the tokens, recipes for motion, whole-screen patterns and a review checklist.")}
  <div class="guides">
    <a class="guide dark tap" href="{u('docs/skill')}" data-rv><span class="mono">Start here · SKILL.md</span><h3>Everything an AI needs to design in this style, in one file.</h3><span class="go-chip">Read SKILL.md{icon("arrow_outward")}</span>{shape_svg("softBurst", "dark-art")}</a>
    {guide_cards}
  </div>
</div></section>"""

    renders = "\n".join(f"  mount('live-{c['name']}', {c['js']});" for c in comps)
    ld = [
        {"@type": "WebPage", "@id": CANONICAL + "/#webpage", "url": CANONICAL + "/", "name": "Material 3 Expressive Skill and Design System",
         "description": HOME_DESC, "inLanguage": "en", "isPartOf": {"@type": "WebSite", "name": "Dinoy Raj", "url": HOME_URL + "/"},
         "primaryImageOfPage": OG_IMAGE, "about": {"@id": CANONICAL + "/#kit"}, "author": AUTHOR},
        {"@type": "SoftwareSourceCode", "@id": CANONICAL + "/#kit", "name": "Expressive Kit", "alternateName": ["Material 3 Expressive skill", "M3 Expressive design system"],
         "description": HOME_DESC, "url": CANONICAL + "/", "codeRepository": REPO_URL, "license": "https://opensource.org/licenses/MIT",
         "programmingLanguage": ["JavaScript", "Kotlin", "CSS"], "runtimePlatform": ["React 18", "Jetpack Compose", "Claude"], "version": VERSION,
         "keywords": "Material 3 Expressive, M3 Expressive, Agent Skill, Claude skill, design system, design tokens, Jetpack Compose, React",
         "author": AUTHOR, "image": OG_IMAGE, "isAccessibleForFree": True},
        {"@type": "FAQPage", "@id": CANONICAL + "/#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]
    return hero + foundations() + comp_sec + guides + faq_html(), renders, ld


HOME_DESC = "Free Material 3 Expressive skill and design system: tokens, 29 live React components, a Jetpack Compose theme, spring motion and M3E guidelines for Claude and AI tools."


# Inner pages ----------------------------------------------------------------------------------------------------------

def breadcrumb_html(crumbs):
    parts = []
    for i, (name, url) in enumerate(crumbs):
        if i < len(crumbs) - 1:
            parts.append(f'<a href="{url}">{esc(name)}</a>{icon("chevron_right")}')
        else:
            parts.append(f'<span aria-current="page">{esc(name)}</span>')
    return f'<nav class="crumbs mono" aria-label="Breadcrumb">{"".join(parts)}</nav>'


def doc_hero(crumbs, title, lede="", meta=""):
    lede_html = f'<p class="doc-lede" data-rv style="--d:2">{lede}</p>' if lede else ""
    return (f'<section class="doc-hero"><div class="wrap"><div data-rv>{breadcrumb_html(crumbs)}</div>'
            f'<h1 class="sec-title" data-rv style="--d:1">{esc(title)}</h1>{lede_html}{meta}</div></section>')


def toc(inner):
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', inner)
    if len(heads) < 3:
        return ""
    items = "".join(f'<a href="#{hid}">{strip_tags(t)}</a>' for hid, t in heads)
    return f'<aside class="toc" aria-label="On this page"><div class="mono">/ On this page</div>{items}</aside>'


def pager(prev, nxt):
    def card(item, label, cls):
        if not item:
            return '<span></span>'
        return f'<a class="pg {cls} tap" href="{item[1]}"><span class="mono">{label}</span><span class="pg-t">{esc(item[0])}</span></a>'
    return f'<nav class="pager" aria-label="More pages">{card(prev, "← Previous", "prev")}{card(nxt, "Next →", "next")}</nav>'


def reading_time(text):
    return max(1, round(len(re.findall(r"\w+", text)) / 220))


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "docs" / "components").mkdir(parents=True)
    for d in ("tokens", "components", "assets", "android", "examples"):
        shutil.copytree(ROOT / d, OUT / d)
    shutil.copy(ROOT / "scripts" / "site.css", OUT / "site.css")
    shutil.copy(ROOT / "scripts" / "site.js", OUT / "site.js")

    comps = components()
    urls = [("", "1.0")]

    # Downloadable skill: SKILL.md plus everything it references.
    with zipfile.ZipFile(OUT / SKILL_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        base = "material-3-expressive"
        z.write(ROOT / "SKILL.md", f"{base}/SKILL.md")
        z.write(ROOT / "LICENSE", f"{base}/LICENSE")
        for folder in SKILL_FOLDERS:
            for f in sorted((ROOT / folder).rglob("*")):
                if f.is_file():
                    z.write(f, f"{base}/{f.relative_to(ROOT)}")

    hero_preload = f'<link rel="preload" as="image" href="{u("assets/hero-light.png")}" fetchpriority="high">\n'
    body, js, ld = home(comps)
    (OUT / "index.html").write_text(page("Material 3 Expressive Skill and Design System | Expressive Kit", body, "", HOME_DESC, scripts=js, ld=ld, preload=hero_preload))

    # Gallery
    g_cards = "".join(comp_card(c, i, big=True) for i, c in enumerate(comps))
    g_body = (doc_hero([("Expressive Kit", u()), ("Gallery", u("gallery"))], "Gallery",
                       f"All {len(comps)} Material 3 Expressive components, live. Flip any card to the other theme, copy its code or open its guideline.")
              + f'<section class="sec gallery"><div class="wrap">{filters(comps, search=True)}<div class="c-grid big" data-grid>{g_cards}</div>'
                f'<p class="empty" hidden>No components match.</p></div></section>')
    g_js = "\n".join(f"  mount('live-{c['name']}', {c['js']});" for c in comps)
    g_crumbs = [("Expressive Kit", CANONICAL + "/"), ("Gallery", CANONICAL + "/gallery")]
    g_ld = [{"@type": "CollectionPage", "name": "Material 3 Expressive component gallery", "url": CANONICAL + "/gallery", "author": AUTHOR,
             "hasPart": [{"@type": "TechArticle", "headline": f"{c['label']} component", "url": f"{CANONICAL}/docs/components/{c['name']}"} for c in comps]},
            crumbs_ld(g_crumbs)]
    (OUT / "gallery.html").write_text(page("Material 3 Expressive Component Gallery: 29 live React components | Expressive Kit", g_body, "gallery",
                                           f"Browse all {len(comps)} Material 3 Expressive components live: button groups, split buttons, floating toolbars, wavy progress, loading indicator, dials and more, in light and dark.",
                                           scripts=g_js, ld=g_ld))
    urls.append(("gallery", "0.9"))

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
    for idx, (slug, _label, title, blurb, _shape, _tone, seo) in enumerate(DOCS):
        text = sources.get(slug) or re.sub(r"^# .*\n+", "", (ROOT / "docs" / f"{slug}.md").read_text())
        inner = MD(text.replace("{#import}", ""))
        inner = re.sub(r'<h2 id="[^"]*">Import into Claude', '<h2 id="import">Import into Claude', inner)
        crumbs = [("Expressive Kit", u()), ("Guides", u() + "#guides"), (title, u("docs/" + slug))]
        prev = (DOCS[idx - 1][2], u("docs/" + DOCS[idx - 1][0])) if idx > 0 else None
        nxt = (DOCS[idx + 1][2], u("docs/" + DOCS[idx + 1][0])) if idx < len(DOCS) - 1 else None
        meta = f'<div class="doc-meta" data-rv style="--d:3"><span class="tag">{reading_time(text)} min read</span><span class="tag">Guide {idx + 1:02d} of {len(DOCS):02d}</span></div>'
        side = toc(inner)
        body = (doc_hero(crumbs, title, blurb, meta) +
                f'<div class="wrap doc-wrap{" has-toc" if side else ""}">{side}<article class="s-doc" data-rv style="--d:3">{inner}{pager(prev, nxt)}</article></div>')
        url = f"{CANONICAL}/docs/{slug}"
        ld = [{"@type": "TechArticle", "headline": seo, "name": title, "description": blurb, "url": url, "image": OG_IMAGE, "inLanguage": "en",
               "author": AUTHOR, "publisher": AUTHOR, "isPartOf": {"@id": CANONICAL + "/#kit"}, "about": "Material 3 Expressive",
               "mainEntityOfPage": url, "wordCount": len(re.findall(r"\w+", text))},
              crumbs_ld([("Expressive Kit", CANONICAL + "/"), ("Guides", CANONICAL + "/#guides"), (title, url)])]
        (OUT / "docs" / f"{slug}.html").write_text(page(f"{seo} | Expressive Kit", body, f"docs/{slug}", blurb, ld=ld, og_type="article"))
        urls.append((f"docs/{slug}", "0.8"))

    for idx, c in enumerate(comps):
        prev = (comps[idx - 1]["label"], u("docs/components/" + comps[idx - 1]["name"])) if idx > 0 else None
        nxt = (comps[idx + 1]["label"], u("docs/components/" + comps[idx + 1]["name"])) if idx < len(comps) - 1 else None
        related = [r for r in comps if r["group"] == c["group"] and r["name"] != c["name"]]
        rel_html = ""
        if related:
            rel_html = ('<h2 id="related">More ' + c["group"].lower() + ' components</h2><div class="rel">' +
                        "".join(f'<a class="tap" href="{u("docs/components/" + r["name"])}">{r["label"]}{icon("arrow_outward")}</a>' for r in related) + "</div>")
        stage_h = max(240, min(620, c["height"] + 80))
        summary_txt = strip_tags(inline_md(c["summary"]))
        crumbs = [("Expressive Kit", u()), ("Components", u() + "#components"), (c["label"], u("docs/components/" + c["name"]))]
        inner = (f'<div class="cc solo spot" data-rv style="--d:3"><div class="cc-stage" style="--stage-h:{stage_h}px"><div class="fit" id="live"{fit_style(c)}></div>'
                 f'<div class="cc-tools"><button type="button" class="ib tap" data-theme-toggle aria-label="Show in the other theme">{icon("contrast")}</button></div></div></div>'
                 f'{MD(c["readme"])}'
                 f'<h2 id="code">Live demo code</h2><p>The demo above is this call to the bundle (<code>E = window.Expressive</code>, <code>h = React.createElement</code>).</p>'
                 f'<div class="code"><button type="button" class="ib tap" data-copy-code="code-live" aria-label="Copy code">{icon("content_copy")}</button>'
                 f'<pre><code id="code-live">{esc(c["js"].strip())}</code></pre></div>{rel_html}{pager(prev, nxt)}')
        meta = f'<div class="doc-meta" data-rv style="--d:3"><span class="tag">{c["group"]}</span><span class="tag">React 18</span><span class="tag">Light + dark</span></div>'
        side = toc(inner)
        body = doc_hero(crumbs, c["label"], inline_md(c["summary"]), meta) + \
            f'<div class="wrap doc-wrap{" has-toc" if side else ""}">{side}<article class="s-doc">{inner}</article></div>'
        url = f"{CANONICAL}/docs/components/{c['name']}"
        desc = f"{c['label']}: {summary_txt} A live Material 3 Expressive React component with usage guidance, in light and dark."
        if len(desc) > 165:
            desc = f"{c['label']}, a Material 3 Expressive component: {summary_txt}"
        ld = [{"@type": "TechArticle", "headline": f"{c['label']}: Material 3 Expressive component", "description": summary_txt, "url": url,
               "image": OG_IMAGE, "author": AUTHOR, "publisher": AUTHOR, "isPartOf": {"@id": CANONICAL + "/#kit"}, "about": ["Material 3 Expressive", c["label"]],
               "mainEntityOfPage": url, "programmingLanguage": "JavaScript"},
              crumbs_ld([("Expressive Kit", CANONICAL + "/"), ("Components", CANONICAL + "/#components"), (c["label"], url)])]
        (OUT / "docs" / "components" / f"{c['name']}.html").write_text(
            page(f"{c['label']}: Material 3 Expressive Component | Expressive Kit", body, f"docs/components/{c['name']}", desc,
                 scripts=f"  mount('live', {c['js']});", ld=ld, og_type="article"))
        urls.append((f"docs/components/{c['name']}", "0.6"))

    # 404
    nf = (f'<section class="nf"><div class="wrap"><div class="nf-art" aria-hidden="true">{shape_svg("burst")}<span>404</span></div>'
          f'<h1 class="sec-title">This page morphed away.</h1><p class="sec-lede">The link is old or mistyped. Everything in the kit is one tap from home.</p>'
          f'<div class="ex-row"><a class="ex-press ex-btn v-filled tap" href="{u()}">{icon("home")}Back to the kit</a>'
          f'<a class="ex-press ex-btn v-outlined tap" href="{u("gallery")}">Open gallery</a></div></div></section>')
    (OUT / "404.html").write_text(page("Page not found | Expressive Kit", nf, "404", "This page does not exist. Head back to Expressive Kit, the Material 3 Expressive skill and design system.")
                                  .replace('content="index, follow, max-image-preview:large, max-snippet:-1"', 'content="noindex, follow"'))

    # sitemap.xml, robots.txt (for hosts that serve this folder at their root) and llms.txt
    sm = "".join(f"<url><loc>{CANONICAL}/{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>" for p, pr in urls)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {CANONICAL}/sitemap.xml\n")
    llms = [f"# Expressive Kit: Material 3 Expressive skill and design system", "",
            f"> {HOME_DESC}", "",
            f"- Skill download: {CANONICAL}/{SKILL_ZIP}", f"- Source: {REPO_URL}", f"- SKILL.md: {CANONICAL}/docs/skill", "", "## Guides", ""]
    llms += [f"- [{t}]({CANONICAL}/docs/{s}): {b}" for s, _l, t, b, *_ in DOCS]
    llms += ["", "## Components", ""]
    llms += [f"- [{c['label']}]({CANONICAL}/docs/components/{c['name']}): {strip_tags(inline_md(c['summary']))}" for c in comps]
    (OUT / "llms.txt").write_text("\n".join(llms) + "\n")
    (OUT / ".nojekyll").write_text("")
    print(f"Built _site/ with {len(comps)} components, {len(urls)} sitemap URLs and {SKILL_ZIP} (base {BASE})")


if __name__ == "__main__":
    build()
