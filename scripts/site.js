/* Expressive Kit website behaviour. Plain ES5-ish, no build step. Loaded after React, the component bundle and each page's
   mount() calls. Every effect respects prefers-reduced-motion (html.rm) and degrades to a static page without JS. */
(function () {
  var root = document.documentElement, RM = root.classList.contains('rm');
  var E = window.Expressive, h = window.React && React.createElement;
  var fine = matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* Lets :active fire on iOS Safari, so press feedback works on touch. */
  document.addEventListener('touchstart', function () {}, { passive: true });

  /* Island nav ------------------------------------------------------------------------------------------------------- */
  var nav = document.querySelector('.nav'), btn = nav.querySelector('.menu-btn'), panel = nav.querySelector('.nav-panel'), scrim = document.querySelector('.nav-scrim');
  function setNav(open) {
    nav.classList.toggle('open', open); btn.setAttribute('aria-expanded', open); btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    nav.style.height = open ? (60 + panel.scrollHeight) + 'px' : '';
    if (open) { panel.removeAttribute('inert'); scrim.hidden = false; requestAnimationFrame(function () { scrim.classList.add('on'); }); }
    else { panel.setAttribute('inert', ''); scrim.classList.remove('on'); setTimeout(function () { if (!nav.classList.contains('open')) scrim.hidden = true; }, 300); }
  }
  nav.querySelector('.nav-row').addEventListener('click', function (e) { if (!e.target.closest('.nav-name')) setNav(!nav.classList.contains('open')); });
  scrim.addEventListener('click', function () { setNav(false); });
  panel.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setNav(false); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('open')) { setNav(false); btn.focus(); } });

  var cur = root.dataset.theme || 'system', themeBtns = nav.querySelectorAll('.theme button');
  function markTheme() { themeBtns.forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.t === cur); }); }
  themeBtns.forEach(function (b) { b.addEventListener('click', function (e) {
    e.stopPropagation(); cur = b.dataset.t;
    var apply = function () { if (cur === 'system') delete root.dataset.theme; else root.dataset.theme = cur; };
    if (document.startViewTransition && !RM) { root.classList.add('vt-theme'); document.startViewTransition(apply).finished.then(function () { root.classList.remove('vt-theme'); }); } else apply();
    try { localStorage.setItem('ek-theme', cur); } catch (err) {}
    markTheme();
  }); });
  markTheme();

  /* Scroll: progressive blur band, nav shadow, parallax ------------------------------------------------------------- */
  var blur = document.querySelector('.top-blur'), pars = [].slice.call(document.querySelectorAll('[data-par]')), ticking = false;
  function onScroll() {
    ticking = false;
    var y = scrollY;
    blur.classList.toggle('on', y > 8);
    nav.classList.toggle('scrolled', y > 8);
    if (!RM) pars.forEach(function (el) { el.style.setProperty('--py', (y * parseFloat(el.dataset.par)).toFixed(1) + 'px'); });
  }
  addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  /* Reveal: elements rise out of a blur as they enter, staggered by --d. Count-ups start when theirs is revealed. ------ */
  function countUp(el) {
    var to = parseInt(el.dataset.count, 10), t0 = null, dur = 1100;
    if (RM || !to) return;
    function step(t) { if (!t0) t0 = t; var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 4); el.textContent = Math.round(to * e); if (k < 1) requestAnimationFrame(step); }
    el.textContent = '0'; requestAnimationFrame(step);
  }
  var rvs = document.querySelectorAll('[data-rv]');
  if (RM || !('IntersectionObserver' in window)) rvs.forEach(function (el) { el.classList.add('in'); });
  else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var t = en.target; t.classList.add('in'); io.unobserve(t);
        t.querySelectorAll('[data-count]').forEach(countUp);
        /* once revealed, drop the reveal styles so the element's own hover and press transitions take over again */
        setTimeout(function () { t.removeAttribute('data-rv'); }, 1100 + (parseFloat(t.style.getPropertyValue('--d')) || 0) * 80);
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.08 });
    rvs.forEach(function (el) { io.observe(el); });
  }
  var heroCount = document.querySelector('.hero [data-count]'); if (heroCount) setTimeout(function () { countUp(heroCount); }, 500);

  /* Pointer spotlight on cards (mouse only) --------------------------------------------------------------------------- */
  if (fine) document.addEventListener('pointermove', function (e) {
    var el = e.target.closest && e.target.closest('.spot'); if (!el) return;
    var r = el.getBoundingClientRect();
    el.style.setProperty('--mx', (e.clientX - r.left) + 'px'); el.style.setProperty('--my', (e.clientY - r.top) + 'px');
  }, { passive: true });

  /* Hero portrait: tilts toward the pointer; a tap morphs the frame and spins the burst. ----------------------------- */
  var portrait = document.querySelector('.portrait');
  if (portrait && !RM) {
    if (fine) {
      portrait.addEventListener('pointermove', function (e) {
        var r = portrait.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        portrait.style.setProperty('--rx', (-y * 14).toFixed(2) + 'deg'); portrait.style.setProperty('--ry', (x * 16).toFixed(2) + 'deg');
      });
      portrait.addEventListener('pointerleave', function () { portrait.style.setProperty('--rx', '0deg'); portrait.style.setProperty('--ry', '0deg'); });
    }
    portrait.addEventListener('click', function () { portrait.classList.remove('pop'); void portrait.offsetWidth; portrait.classList.add('pop'); });
  }

  /* Scroll-lit statement --------------------------------------------------------------------------------------------- */
  var lit = document.querySelector('[data-lit]');
  if (lit) {
    lit.innerHTML = lit.innerHTML.replace(/(<span class="hl">)?([^\s<>]+)(<\/span>)?/g, function (m, a, w) { return '<span class="w' + (a ? ' hl' : '') + '">' + w + '</span>'; });
    var words = lit.querySelectorAll('.w');
    if (RM) words.forEach(function (w) { w.classList.add('on'); });
    else {
      var litTick = function () { var r = lit.getBoundingClientRect(), vh = innerHeight, f = (vh * .85 - r.top) / (r.height + vh * .35); words.forEach(function (w, i) { w.classList.toggle('on', i < f * words.length); }); };
      addEventListener('scroll', litTick, { passive: true }); addEventListener('resize', litTick); litTick(); lit.classList.add('ready');
    }
  }

  /* Shape icons in the get-started rows, and the shape library that morphs on hover or tap. --------------------------- */
  if (E && h) {
    document.querySelectorAll('[data-ws]').forEach(function (el) { ReactDOM.createRoot(el).render(h(E.ShapeAvatar, { shape: el.dataset.ws, size: 48, icon: el.dataset.icon, tone: el.dataset.tone })); });
    var tones = ['primary-container', 'secondary-container', 'tertiary-container', 'highlight'];
    var all = [].map.call(document.querySelectorAll('[data-shape]'), function (el) { return el.dataset.shape; });
    document.querySelectorAll('[data-shape]').forEach(function (el, i) {
      var home = el.dataset.shape, art = el.querySelector('.shp-art'), r = ReactDOM.createRoot(art), tone = tones[i % 4];
      function draw(s) { r.render(h(E.ShapeAvatar, { shape: s, size: 64, tone: tone, label: home })); }
      function other() { var s; do { s = all[Math.floor(Math.random() * all.length)]; } while (s === home); return s; }
      draw(home);
      el.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') { draw(other()); el.classList.add('on'); } });
      el.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') { draw(home); el.classList.remove('on'); } });
      el.addEventListener('click', function () { var on = el.classList.toggle('on'); draw(on ? other() : home); });
    });
  }

  /* Motion rows: tap to send the ball across with that spring. ------------------------------------------------------- */
  document.querySelectorAll('.mo').forEach(function (m) { m.addEventListener('click', function () { m.classList.toggle('go'); }); });

  /* Tabs (Foundations): roving focus, a sliding pill indicator, panels that fade in from a blur. --------------------- */
  document.querySelectorAll('.tablist').forEach(function (list) {
    var tabs = [].slice.call(list.querySelectorAll('[role=tab]')), ind = list.querySelector('.tab-ind');
    function place(t) { ind.style.width = t.offsetWidth + 'px'; ind.style.transform = 'translateX(' + t.offsetLeft + 'px)'; }
    function select(t, focus) {
      tabs.forEach(function (x) {
        var on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
        var p = document.getElementById(x.getAttribute('aria-controls')); p.hidden = !on; if (on) { p.classList.remove('show'); void p.offsetWidth; p.classList.add('show'); }
      });
      place(t); if (focus) t.focus();
      if (t.id === 'tab-colour') paintHex();
      t.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: RM ? 'auto' : 'smooth' });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var k = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (!k) return;
        e.preventDefault(); select(tabs[(i + k + tabs.length) % tabs.length], true);
      });
    });
    var sel = function () { place(list.querySelector('[aria-selected=true]')); };
    addEventListener('resize', sel); document.fonts && document.fonts.ready.then(sel); sel();
  });

  /* Swatch hex values follow the theme ------------------------------------------------------------------------------- */
  function toHex(c) {
    var m = c.match(/\d+(\.\d+)?/g); if (!m || m.length < 3) return c.trim();
    return '#' + m.slice(0, 3).map(function (v) { return ('0' + Math.round(+v).toString(16)).slice(-2); }).join('');
  }
  var probe = document.createElement('span'); probe.style.display = 'none'; document.body.appendChild(probe);
  function paintHex() {
    document.querySelectorAll('.hex[data-var]').forEach(function (el) { probe.style.color = 'var(' + el.dataset.var + ')'; el.textContent = toHex(getComputedStyle(probe).color); });
  }
  paintHex();
  new MutationObserver(paintHex).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', paintHex);

  /* Toast + copy ------------------------------------------------------------------------------------------------------ */
  var toast = document.querySelector('.toast'), toastT;
  function say(msg) { toast.textContent = msg; toast.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(function () { toast.classList.remove('on'); }, 1800); }
  function copy(text, msg) {
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(function () { say(msg); }, function () { say('Copy failed'); });
    else say('Copy not supported');
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-copy]'); if (t) { copy(t.dataset.copy, 'Copied ' + t.dataset.copy); return; }
    var c = e.target.closest('[data-copy-code]'); if (c) { var src = document.getElementById(c.dataset.copyCode); copy(src.textContent, 'Code copied'); return; }
    var th = e.target.closest('[data-theme-toggle]');
    if (th) {
      var stage = th.closest('.cc-stage'), isDark = stage.dataset.theme ? stage.dataset.theme === 'dark' : isRootDark();
      stage.dataset.theme = isDark ? 'light' : 'dark'; th.setAttribute('aria-pressed', 'true');
    }
  });
  function isRootDark() { return root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches; }

  /* Component stages: centre each demo and scale it down when it does not fit, so every card in a grid is the same size. */
  var stages = [].slice.call(document.querySelectorAll('.cc-stage'));
  function fit(stage) {
    var el = stage.querySelector('.fit'); if (!el) return;
    var cs = getComputedStyle(stage), aw = stage.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight), ah = stage.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
    var w = Math.max(el.offsetWidth, el.scrollWidth), hh = Math.max(el.offsetHeight, el.scrollHeight);
    if (!w || !hh) return;
    var s = Math.min(1, aw / w, ah / hh);
    el.style.setProperty('--s', s < .995 ? s.toFixed(3) : 1);
  }
  if ('ResizeObserver' in window) {
    var ro = new ResizeObserver(function (entries) { entries.forEach(function (en) { var st = en.target.closest('.cc-stage'); if (st) fit(st); }); });
    stages.forEach(function (st) { ro.observe(st); var f = st.querySelector('.fit'); if (f) ro.observe(f); });
  }
  setTimeout(function () { stages.forEach(fit); }, 60);
  document.fonts && document.fonts.ready.then(function () { stages.forEach(fit); });

  /* Filters and search over a component grid, animated with a view transition where the browser has one. ------------ */
  document.querySelectorAll('[data-grid]').forEach(function (grid) {
    var sec = grid.closest('section'), chips = sec.querySelectorAll('.fchip'), search = sec.querySelector('[data-search]'), empty = sec.querySelector('.empty');
    var cards = [].slice.call(grid.querySelectorAll('.cc')), group = 'all';
    function apply() {
      var q = search ? search.value.trim().toLowerCase() : '', shown = 0;
      cards.forEach(function (c) {
        var ok = (group === 'all' || c.dataset.group === group) && (!q || c.dataset.name.indexOf(q) > -1);
        c.hidden = !ok; if (ok) { shown++; c.classList.add('in'); }
      });
      if (empty) empty.hidden = shown > 0;
    }
    function run() {
      if (!document.startViewTransition || RM) { apply(); requestAnimationFrame(function () { stages.forEach(fit); }); return; }
      cards.forEach(function (c, i) { if (!c.hidden) c.style.viewTransitionName = 'cc' + i; });
      var vt = document.startViewTransition(function () { apply(); cards.forEach(function (c, i) { c.style.viewTransitionName = c.hidden ? '' : 'cc' + i; }); });
      vt.finished.then(function () { cards.forEach(function (c) { c.style.viewTransitionName = ''; }); stages.forEach(fit); });
    }
    chips.forEach(function (ch) { ch.addEventListener('click', function () {
      group = ch.dataset.f; chips.forEach(function (x) { x.setAttribute('aria-pressed', x === ch); }); run();
    }); });
    if (search) { var st; search.addEventListener('input', function () { clearTimeout(st); st = setTimeout(run, 120); }); }
  });

  /* Footer wordmark: letters near the pointer go thin, narrow, lift and warm up; a tap sends a wave across. ---------- */
  var wm = document.querySelector('.wordmark');
  if (wm && !RM) {
    var ls = [].slice.call(wm.querySelectorAll('.wm-l'));
    if (fine) {
      wm.addEventListener('pointermove', function (e) {
        ls.forEach(function (l) { var r = l.getBoundingClientRect(), d = Math.abs(e.clientX - (r.left + r.width / 2)) / (r.width * 2.2); l.style.setProperty('--p', Math.max(0, 1 - d).toFixed(3)); });
      });
      wm.addEventListener('pointerleave', function () { ls.forEach(function (l) { l.style.setProperty('--p', 0); }); });
    }
    wm.addEventListener('click', function () { wm.classList.remove('wave'); void wm.offsetWidth; wm.classList.add('wave'); });
  }

  /* Docs table of contents: highlight the section in view. --------------------------------------------------------- */
  var tocLinks = [].slice.call(document.querySelectorAll('.toc a'));
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var byId = {}; tocLinks.forEach(function (a) { byId[decodeURIComponent(a.hash.slice(1))] = a; });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { tocLinks.forEach(function (a) { a.classList.remove('on'); }); var a = byId[en.target.id]; if (a) a.classList.add('on'); } });
    }, { rootMargin: '-20% 0px -70% 0px' });
    Object.keys(byId).forEach(function (id) { var el = document.getElementById(id); if (el) spy.observe(el); });
  }

  /* FAQ: smooth open and close where ::details-content is not animatable yet. ---------------------------------------- */
  if (!RM && !CSS.supports('interpolate-size', 'allow-keywords')) {
    document.querySelectorAll('details.qa').forEach(function (d) {
      var s = d.querySelector('summary'), a = d.querySelector('.qa-a');
      s.addEventListener('click', function (e) {
        e.preventDefault();
        if (d.open) { a.animate([{ height: a.offsetHeight + 'px', opacity: 1 }, { height: '0px', opacity: 0 }], { duration: 260, easing: 'cubic-bezier(.2,0,0,1)' }).onfinish = function () { d.open = false; }; }
        else { d.open = true; var hgt = a.offsetHeight; a.animate([{ height: '0px', opacity: 0 }, { height: hgt + 'px', opacity: 1 }], { duration: 420, easing: 'cubic-bezier(.34,1.3,.64,1)' }); }
      });
    });
  }
})();
