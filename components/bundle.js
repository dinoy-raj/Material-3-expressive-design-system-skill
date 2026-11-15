/* @ds-bundle: {"format":4,"namespace":"Expressive","components":[{"name":"Button"},{"name":"IconButton"},{"name":"Fab"},{"name":"ButtonGroup"},{"name":"Chip"},{"name":"Badge"},{"name":"ValuePill"},{"name":"NavigationBar"},{"name":"TopBar"},{"name":"SearchBar"},{"name":"TextField"},{"name":"Switch"},{"name":"Slider"},{"name":"WavyProgress"},{"name":"Card"},{"name":"ListItem"},{"name":"GroupedList"},{"name":"StatTile"},{"name":"ShapeAvatar"},{"name":"BottomSheet"},{"name":"SummaryList"},{"name":"Snackbar"},{"name":"LoadingIndicator"},{"name":"SplitButton"},{"name":"FloatingToolbar"},{"name":"DigitRoll"},{"name":"TimePickerDial"},{"name":"RotaryDial"},{"name":"NavigationRail"}]} */
(function () {
  var React = window.React;
  var h = React.createElement;
  var useState = React.useState;
  function cx() { return Array.prototype.filter.call(arguments, Boolean).join(' '); }
  function Icon(name, filled, extra) { return name ? h('span', { className: cx('ex-icon', filled && 'is-filled', extra), 'aria-hidden': 'true' }, name) : null; }

  /* The M3 Expressive shape library, as polar functions r(t) on a unit circle (t = 0 points up, clockwise).
     Every shape is star-shaped around its centre, so any two can morph by blending their radii. */
  function superformula(m, n, rot) { /* rounded regular polygon with m sides; larger n = sharper corners */
    return function (t) { var a = m * (t + (rot || 0)) / 4; return Math.pow(Math.pow(Math.abs(Math.cos(a)), n) + Math.pow(Math.abs(Math.sin(a)), n), -1 / n); };
  }
  function lp(a, b, pw, rot) { /* p-norm ellipse/rhombus with half-axes a (horizontal) and b (vertical) */
    return function (t) { var u = t + (rot || 0); return Math.pow(Math.pow(Math.abs(Math.sin(u) / a), pw) + Math.pow(Math.abs(Math.cos(u) / b), pw), -1 / pw); };
  }
  function parametric(fx, fy, cyShift) { /* polar lookup table from a closed parametric curve */
    var M = 720, xs = [], ys = [], i, s, table = new Array(360);
    for (i = 0; i < M; i++) { s = i / M * 2 * Math.PI; xs.push(fx(s)); ys.push(fy(s) - (cyShift || 0)); }
    for (i = 0; i < 360; i++) table[i] = 0;
    for (i = 0; i < M; i++) {
      var ang = Math.atan2(xs[i], ys[i]); if (ang < 0) ang += 2 * Math.PI;
      var k = Math.round(ang / (2 * Math.PI) * 360) % 360, r = Math.sqrt(xs[i] * xs[i] + ys[i] * ys[i]);
      table[k] = Math.max(table[k], r);
    }
    for (i = 0; i < 360; i++) if (!table[i]) { var a2 = i, b2 = i; while (!table[a2 = (a2 + 359) % 360]); while (!table[b2 = (b2 + 1) % 360]); table[i] = (table[a2] + table[b2]) / 2; }
    return function (t) { var x = ((t / (2 * Math.PI)) * 360 % 360 + 360) % 360, i0 = Math.floor(x), f = x - i0; return table[i0] * (1 - f) + table[(i0 + 1) % 360] * f; };
  }
  var SHAPES = {
    circle: function () { return 1; },
    cookie4: function (t) { return 1 + 0.08 * Math.cos(4 * t); },
    cookie6: function (t) { return 1 + 0.12 * Math.cos(6 * t); },
    cookie7: function (t) { return 1 + 0.09 * Math.cos(7 * t); },
    cookie9: function (t) { return 1 + 0.075 * Math.cos(9 * t); },
    cookie12: function (t) { return 1 + 0.05 * Math.cos(12 * t); },
    clover4: function (t) { return 0.9 + 0.22 * Math.pow(Math.abs(Math.cos(2 * t)), 1.6); },
    clover8: function (t) { return 0.86 + 0.16 * Math.pow(Math.abs(Math.cos(4 * t)), 1.4); },
    flower5: function (t) { return 1 + 0.16 * Math.cos(5 * t); },
    flower8: function (t) { return 1 + 0.17 * Math.cos(8 * t); },
    sunny: function (t) { return 1 + 0.04 * Math.cos(8 * t + 0.4); },
    softBurst: function (t) { return 1 + 0.07 * Math.cos(10 * t); },
    burst: function (t) { return 1 + 0.13 * Math.cos(10 * t); },
    boom: function (t) { return 0.76 + 0.24 * Math.pow(0.5 + 0.5 * Math.cos(15 * t), 2.2); },
    pebble: function (t) { return 0.94 + 0.12 * Math.cos(3 * t); },
    puffy: function (t) { return lp(1, 0.84, 2.6)(t) * (1 + 0.035 * Math.cos(12 * t)); },
    square: superformula(4, 5),
    pill: lp(1, 0.6, 4.5),
    oval: lp(1, 0.74, 2, Math.PI / 4),
    diamond: lp(0.82, 1, 1.25),
    triangle: superformula(3, 3.4, Math.PI),
    pentagon: superformula(5, 4.2, Math.PI / 5),
    gem: superformula(6, 3.6, Math.PI / 6),
    heart: parametric(function (s) { return 16 * Math.pow(Math.sin(s), 3); },
      function (s) { return 13 * Math.cos(s) - 5 * Math.cos(2 * s) - 2 * Math.cos(3 * s) - Math.cos(4 * s); }, 1.5),
    arch: function (t) { var u = ((t % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI); return (u <= Math.PI / 2 || u >= 1.5 * Math.PI) ? 1 : Math.pow(Math.pow(Math.abs(Math.sin(u)), 6) + Math.pow(Math.abs(Math.cos(u)), 6), -1 / 6); }
  };
  var N_PTS = 180, radiiCache = {}, pathCache = {};
  function radii(name) {
    if (radiiCache[name]) return radiiCache[name];
    var fn = SHAPES[name] || SHAPES.circle, out = [], max = 0, i;
    for (i = 0; i < N_PTS; i++) { var r = fn(i / N_PTS * 2 * Math.PI); out.push(r); max = Math.max(max, r); }
    for (i = 0; i < N_PTS; i++) out[i] /= max;
    return (radiiCache[name] = out);
  }
  function radiiPath(rs) {
    var d = '';
    for (var j = 0; j < rs.length; j++) { var t = j / rs.length * 2 * Math.PI; d += (j ? 'L' : 'M') + (rs[j] * Math.sin(t)).toFixed(4) + ' ' + (-rs[j] * Math.cos(t)).toFixed(4); }
    return d + 'Z';
  }
  function shapePath(name) { return pathCache[name] || (pathCache[name] = radiiPath(radii(name))); }
  /* Blend two library shapes; k may overshoot past 0..1 when driven by a spatial spring. */
  function shapeMorph(a, b, k) {
    var ra = radii(a), rb = radii(b), out = [];
    for (var i = 0; i < N_PTS; i++) out.push(Math.max(0.02, ra[i] + (rb[i] - ra[i]) * k));
    return radiiPath(out);
  }

  /* Springs: the motion tokens as real damped springs, for JS-driven animation. */
  var SPRINGS = {
    expressive: { 'spatial-fast': [0.6, 800], 'spatial-default': [0.8, 380], 'spatial-slow': [0.8, 200], 'effects-fast': [1, 3800], 'effects-default': [1, 1600], 'effects-slow': [1, 800] },
    standard: { 'spatial-fast': [0.9, 1400], 'spatial-default': [0.9, 700], 'spatial-slow': [0.9, 300], 'effects-fast': [1, 3800], 'effects-default': [1, 1600], 'effects-slow': [1, 800] }
  };
  function reducedMotion() { return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches); }
  function motionScheme() { var el = document.documentElement; return (el && el.getAttribute('data-motion') === 'standard') ? 'standard' : 'expressive'; }
  /* spring(token) or spring(damping, stiffness) -> { at(seconds) -> progress, duration (seconds), v0 support } */
  function spring(a, b, v0) {
    var z, k;
    if (typeof a === 'string') { var sp = SPRINGS[motionScheme()][a] || SPRINGS.expressive['spatial-default']; z = sp[0]; k = sp[1]; } else { z = a; k = b; }
    var w = Math.sqrt(k), v = -(v0 || 0); /* v0: initial velocity in progress units per second */
    function at(t) {
      if (z < 1) { var wd = w * Math.sqrt(1 - z * z); return 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + (z * w + v) / wd * Math.sin(wd * t)); }
      return 1 - Math.exp(-w * t) * (1 + (w + v) * t);
    }
    var dur = 0; for (var t = 0; t < 3; t += 0.004) if (Math.abs(1 - at(t)) > 0.001) dur = t;
    return { at: at, duration: Math.max(0.05, dur) };
  }
  /* Run a spring from `from` to `to`, calling onFrame(value). Returns a cancel function. */
  function animateSpring(from, to, token, onFrame, onDone, velocity) {
    if (reducedMotion() && String(token).indexOf('spatial') === 0) { onFrame(to); if (onDone) onDone(); return function () {}; }
    var range = to - from, sp = spring(token, undefined, range ? (velocity || 0) / range : 0), start = null, raf;
    function frame(ts) {
      if (start === null) start = ts;
      var t = (ts - start) / 1000;
      if (t >= sp.duration) { onFrame(to); if (onDone) onDone(); return; }
      onFrame(from + range * sp.at(t)); raf = requestAnimationFrame(frame);
    }
    raf = requestAnimationFrame(frame);
    return function () { cancelAnimationFrame(raf); };
  }
  /* Haptics where the browser supports them (Android Chrome). Kinds follow docs/motion.md. */
  var HAPTICS = { tick: 4, tap: 8, confirm: [10, 40, 18], reject: [24, 50, 24], longPress: 18, start: 12, stop: [8, 30, 8] };
  function haptic(kind) { try { if (navigator.vibrate && !reducedMotion()) navigator.vibrate(HAPTICS[kind] || 8); } catch (e) { /* unsupported */ } }

  function Button(p) {
    var variant = p.variant || 'filled', size = p.size || 'sm';
    var rest = Object.assign({}, p); ['variant', 'size', 'icon', 'tone', 'fullWidth', 'className', 'children'].forEach(function (k) { delete rest[k]; });
    return h('button', Object.assign({ type: 'button' }, rest, { className: cx('ex-press ex-btn', 'v-' + variant, 'size-' + size, p.tone && 't-' + p.tone, p.fullWidth && 'full', p.className) }), Icon(p.icon), p.children);
  }

  function IconButton(p) {
    var variant = p.variant || 'standard';
    return h('button', { type: 'button', className: cx('ex-press ex-iconbtn', 'v-' + variant, p.size === 'sm' && 'size-sm', p.selected && 'is-selected', p.className), 'aria-label': p.label, 'aria-pressed': p.selected == null ? undefined : !!p.selected, onClick: p.onClick, disabled: p.disabled }, Icon(p.icon, p.selected));
  }

  function Fab(p) {
    return h('button', { type: 'button', className: cx('ex-press ex-fab', 't-' + (p.tone || 'primary'), p.size === 'lg' && 'size-lg', p.label && 'has-label', p.className), 'aria-label': p.label ? undefined : p.ariaLabel, onClick: p.onClick }, Icon(p.icon, true), p.label);
  }

  function ButtonGroup(p) {
    var controlled = p.value !== undefined;
    var st = useState(p.defaultValue !== undefined ? p.defaultValue : (p.options[0] && p.options[0].value));
    var value = controlled ? p.value : st[0];
    var hasSub = p.options.some(function (o) { return o.sub; });
    return h('div', { role: 'radiogroup', 'aria-label': p.label, className: cx('ex-bgroup', p.fit && 'is-fit', p.tone && 't-' + p.tone, hasSub && 'has-sub', p.className) },
      p.options.map(function (o) {
        var sel = o.value === value;
        return h('button', { key: o.value, type: 'button', role: 'radio', 'aria-checked': sel, className: cx('ex-press ex-seg', sel && 'is-selected'), onClick: function () { if (!controlled) st[1](o.value); if (p.onChange) p.onChange(o.value); } },
          Icon(o.icon, sel), hasSub ? h('span', null, o.label, h('span', { className: 'ex-seg-sub' }, o.sub)) : o.label);
      }));
  }

  function Chip(p) {
    var st = useState(!!p.defaultSelected);
    var sel = p.selected !== undefined ? p.selected : st[0];
    var icon = p.icon || (sel && p.variant !== 'tonal' ? 'check' : null);
    return h('button', { type: 'button', 'aria-pressed': sel, className: cx('ex-press ex-chip', p.variant === 'tonal' && 'v-tonal', sel && 'is-selected', p.className), onClick: function () { if (p.selected === undefined) st[1](!sel); if (p.onClick) p.onClick(!sel); } },
      Icon(icon, sel), p.label, p.count != null ? h('span', { className: 'ex-chip-count' }, p.count) : null);
  }

  function Badge(p) {
    return h('span', { className: cx('ex-badge', p.tone && 't-' + p.tone, p.mono && 'is-mono', p.count != null && 'is-count', p.className) }, p.dot ? h('span', { className: 'dot' }) : null, p.count != null ? p.count : p.children);
  }

  function ValuePill(p) {
    var dir = p.direction || 'up';
    if (p.inline) return h('span', { className: cx('ex-delta', dir) }, Icon(dir === 'up' ? 'arrow_drop_up' : 'arrow_drop_down', true), p.children);
    return h('span', { className: cx('ex-vpill', dir, p.solid && 'is-solid') }, Icon(dir === 'up' ? 'arrow_drop_up' : 'arrow_drop_down', true), p.children);
  }

  function NavigationBar(p) {
    var st = useState(p.defaultValue !== undefined ? p.defaultValue : 0);
    var active = p.value !== undefined ? p.value : st[0];
    return h('nav', { className: cx('ex-navbar', p.className), 'aria-label': p.label || 'Main' },
      p.items.map(function (it, i) {
        var on = i === active;
        return h('button', { key: it.label, type: 'button', className: cx('ex-press ex-navitem', on && 'is-active'), 'aria-current': on ? 'page' : undefined, onClick: function () { if (p.value === undefined) st[1](i); if (p.onChange) p.onChange(i); } },
          h('span', { className: 'ex-navpill' }, Icon(it.icon, on), it.badge ? h(Badge, { count: it.badge }) : null), it.label);
      }));
  }

  function TopBar(p) {
    var lead = p.leading === 'back' ? h(IconButton, { icon: 'arrow_back', label: 'Back', onClick: p.onLeading }) : p.leading === 'close' ? h(IconButton, { icon: 'close', label: 'Close', onClick: p.onLeading }) : null;
    var actions = (p.actions || []).map(function (a) { return h(IconButton, { key: a.icon, icon: a.icon, label: a.label, onClick: a.onClick, selected: a.selected }); });
    if (p.size === 'small') {
      return h('header', { className: 'ex-topbar' }, h('div', { className: 'ex-topbar-row' }, lead, h('h1', { className: 'ex-topbar-title' }, p.title), h('div', { className: 'ex-topbar-actions' }, actions)));
    }
    var titleClass = p.display ? 'display-small' : 'headline-large';
    return h('header', { className: 'ex-topbar' },
      (lead || actions.length) ? h('div', { className: 'ex-topbar-row' }, lead, h('div', { className: 'ex-topbar-actions' }, actions)) : null,
      h('div', { className: 'ex-topbar-large' },
        p.eyebrow ? h('div', { className: 'eyebrow', style: { color: 'var(--on-surface-variant)' } }, p.eyebrow) : null,
        h('h1', { className: titleClass, style: p.display ? { fontFamily: 'var(--font-display)' } : null }, p.title),
        p.subtitle ? h('p', { className: 'ex-topbar-sub body-large' }, p.subtitle) : null));
  }

  function SearchBar(p) {
    var st = useState(p.defaultValue || '');
    return h('label', { className: cx('ex-search', p.className) },
      h('span', { className: 'ex-search-lead' }, Icon(p.icon || 'search')),
      h('input', { type: 'search', id: p.id, placeholder: p.placeholder || 'Search', value: st[0], onChange: function (e) { st[1](e.target.value); if (p.onChange) p.onChange(e.target.value); }, 'aria-label': p.placeholder || 'Search' }),
      st[0] ? h(IconButton, { icon: 'close', label: 'Clear', size: 'sm', onClick: function () { st[1](''); } }) : (p.trailing || null));
  }

  function TextField(p) {
    var st = useState(p.defaultValue || '');
    var Tag = p.multiline ? 'textarea' : 'input';
    return h('div', { className: cx('ex-field', p.variant === 'filled' && 'is-filled', p.error && 'is-error', p.className) },
      h('label', { className: 'ex-field-box' },
        p.label ? h('span', { className: 'ex-field-label' }, p.label) : null,
        h(Tag, { id: p.id, value: st[0], placeholder: p.placeholder, inputMode: p.inputMode, 'aria-invalid': p.error ? true : undefined, onChange: function (e) { st[1](e.target.value); if (p.onChange) p.onChange(e.target.value); } }),
        p.trailingIcon ? h('span', { className: 'ex-field-trail' }, Icon(p.trailingIcon)) : null),
      (p.error || p.supportingText) ? h('div', { className: 'ex-field-support' }, p.error || p.supportingText) : null);
  }

  function Switch(p) {
    var st = useState(!!p.defaultChecked);
    var on = p.checked !== undefined ? p.checked : st[0];
    var sw = h('button', { type: 'button', role: 'switch', 'aria-checked': on, 'aria-label': p.label, className: cx('ex-press ex-switch', on && 'is-on'), onClick: function () { if (p.checked === undefined) st[1](!on); if (p.onChange) p.onChange(!on); } },
      h('span', { className: 'thumb' }, Icon('check')));
    if (!p.label) return sw;
    return h('div', { className: 'ex-switch-row' }, h('div', { className: 'ex-switch-text' }, h('div', { className: 't' }, p.label), p.supportingText ? h('div', { className: 's' }, p.supportingText) : null), sw);
  }

  function Slider(p) {
    var min = p.min || 0, max = p.max == null ? 100 : p.max;
    var st = useState(p.defaultValue != null ? p.defaultValue : 50);
    var v = p.value != null ? p.value : st[0];
    var pct = (v - min) / (max - min) * 100;
    var fmt = p.format || function (x) { return x; };
    return h('div', { className: 'ex-slider' },
      p.label ? h('div', { className: 'ex-slider-head' }, h('span', { className: 'l' }, p.label), h('span', { className: 'v' }, fmt(v))) : null,
      p.supportingText ? h('div', { className: 'body-medium', style: { color: 'var(--on-surface-variant)', marginTop: '-4px' } }, p.supportingText) : null,
      h('div', { className: 'ex-slider-track' },
        h('div', { className: 'act', style: { width: 'calc(' + pct + '% - 6px)' } }),
        h('div', { className: 'rest', style: { width: 'calc(' + (100 - pct) + '% - 6px)' } }),
        h('input', { type: 'range', id: p.id, min: min, max: max, step: p.step || 1, value: v, 'aria-label': p.label, onChange: function (e) { var n = +e.target.value; if (p.value == null) st[1](n); if (p.onChange) p.onChange(n); } }),
        h('div', { className: 'handle', style: { left: pct + '%' } })));
  }

  function WavyProgress(p) {
    var value = Math.max(0, Math.min(1, p.value == null ? 0.5 : p.value));
    var W = 400, amp = p.flat ? 0 : 3, wl = 24, split = W * value, d = 'M2 8';
    for (var x = 2; x <= Math.max(2, split - 6); x += 2) d += 'L' + x + ' ' + (8 + amp * Math.sin(x / wl * 2 * Math.PI)).toFixed(2);
    return h('div', { className: cx('ex-progress', p.animated && 'is-animated'), role: 'progressbar', 'aria-valuemin': 0, 'aria-valuemax': 100, 'aria-valuenow': Math.round(value * 100), 'aria-label': p.label },
      p.label ? h('div', { className: 'ex-progress-label' }, p.label) : null,
      h('svg', { viewBox: '0 0 ' + W + ' 16', preserveAspectRatio: 'none', 'aria-hidden': 'true' },
        value > 0.01 ? h('path', { className: 'wave', d: d, vectorEffect: 'non-scaling-stroke' }) : null,
        value < 0.99 ? h('line', { className: 'rest', x1: Math.min(W - 2, split + 6), y1: 8, x2: W - 2, y2: 8, vectorEffect: 'non-scaling-stroke' }) : null,
        value < 0.99 ? h('circle', { className: 'stop', cx: W - 4, cy: 8, r: 2 }) : null));
  }

  function Card(p) {
    var Tag = p.onClick ? 'button' : 'div';
    return h(Tag, { className: cx('ex-card', 'v-' + (p.variant || 'low'), p.padding === 'sm' && 'pad-sm', p.onClick && 'is-pressable', p.className), onClick: p.onClick, style: Object.assign(p.onClick ? { border: 0, textAlign: 'left', font: 'inherit', color: 'inherit' } : {}, p.style || {}) },
      p.eyebrow ? h('div', { className: 'eyebrow' }, p.eyebrow) : null,
      p.title ? h('h3', { className: cx('ex-card-title', p.display ? 'headline-small' : 'title-large'), style: p.display ? { fontFamily: 'var(--font-display)', fontWeight: 600 } : null }, p.title) : null,
      p.body ? h('p', { className: 'ex-card-body body-medium' }, p.body) : null,
      p.children);
  }

  function ListItem(p) {
    return h(p.onClick ? 'button' : 'div', { className: cx(p.onClick && 'ex-press', 'ex-li', p.className), onClick: p.onClick, style: p.onClick ? { border: 0, font: 'inherit' } : null },
      p.leading || null,
      h('div', { className: 'ex-li-text' }, h('span', { className: 'h' }, p.headline), p.supporting ? h('span', { className: 's' }, p.supporting) : null, p.meta ? h('span', { className: 'm' }, p.meta) : null),
      p.trailing != null ? h('div', { className: 'ex-li-trail' }, p.trailing) : null);
  }

  function GroupedList(p) {
    return h('section', { className: 'ex-group' },
      p.title ? h('div', { className: 'ex-group-title' }, p.title) : null,
      React.Children.map(p.children, function (c) { return c ? h('div', { className: 'ex-group-item' }, c) : null; }));
  }

  function StatTile(p) {
    return h('div', { className: cx('ex-stat', p.tone && 't-' + p.tone) }, h('span', { className: cx('v', p.display && 'is-display') }, p.value), h('span', { className: 'l' }, p.label));
  }

  function ShapeAvatar(p) {
    var size = p.size || 40, shape = p.shape || 'cookie9';
    var ref = React.useRef(null), last = React.useRef(shape);
    React.useEffect(function () {
      var from = last.current; last.current = shape;
      if (from === shape || !ref.current || p.morph === false) return undefined;
      var el = ref.current;
      return animateSpring(0, 1, 'spatial-default', function (k) { el.setAttribute('d', shapeMorph(from, shape, k)); }, function () { el.setAttribute('d', shapePath(shape)); });
    }, [shape]);
    return h('span', { className: cx('ex-shape', 't-' + (p.tone || 'primary-container'), p.spin && 'is-spin', p.className), style: { width: size, height: size }, role: p.label ? 'img' : undefined, 'aria-label': p.label },
      h('svg', { viewBox: '-1 -1 2 2', 'aria-hidden': 'true' }, h('path', { ref: ref, d: shapePath(shape) })),
      p.icon ? h('span', { className: 'ex-shape-c' }, h('span', { className: 'ex-icon is-filled', style: { fontSize: Math.round(size * 0.5) }, 'aria-hidden': 'true' }, p.icon))
        : p.text ? h('span', { className: 'ex-shape-c', style: { fontSize: Math.round(size * 0.42) } }, p.text) : null);
  }
  ShapeAvatar.shapes = Object.keys(SHAPES);
  ShapeAvatar.path = shapePath;
  ShapeAvatar.morph = shapeMorph;

  function BottomSheet(p) {
    return h('div', { className: 'ex-sheet-wrap' },
      h('div', { className: 'ex-sheet', role: 'dialog', 'aria-label': p.title },
        h('div', { className: 'ex-sheet-handle', 'aria-hidden': 'true' }),
        (p.title || p.eyebrow) ? h('div', { className: 'ex-sheet-head' },
          p.eyebrow ? h(Badge, { tone: p.eyebrowTone, mono: true, dot: true }, p.eyebrow) : null,
          p.title ? h('h2', { className: 'headline-medium', style: { fontFamily: 'var(--font-display)', fontWeight: 500 } }, p.title) : null,
          p.subtitle ? h('p', { className: 'body-medium', style: { margin: 0, color: 'var(--on-surface-variant)' } }, p.subtitle) : null) : null,
        p.children));
  }

  function SummaryList(p) {
    return h('div', { className: 'ex-summary' },
      p.rows.map(function (r, i) {
        return h('div', { key: i, className: cx('ex-summary-row', r.total && 'is-total') }, h('span', { className: 'k' }, r.label), h('span', { className: cx('val', r.tone && 't-' + r.tone) }, r.value));
      }),
      p.footnote ? h('div', { className: 'ex-summary-foot' }, p.footnote) : null);
  }

  function Snackbar(p) {
    return h('div', { className: 'ex-snack', role: 'status' }, h('span', { className: 'msg' }, p.message), p.action ? h('button', { type: 'button', className: 'ex-press', onClick: p.onAction }, p.action) : null);
  }

  /* Loading indicator: a shape that morphs through the shape library while it rotates. */
  var LOADING_SEQ = ['cookie9', 'pebble', 'sunny', 'burst', 'flower5', 'cookie4', 'clover4'];
  function morphPath(a, b, k) { return shapeMorph(a, b, k); }
  function LoadingIndicator(p) {
    var size = p.size || 48;
    var ref = React.useRef(null);
    React.useEffect(function () {
      var el = ref.current, raf, start = null;
      var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (!el) return undefined;
      if (reduce) { el.setAttribute('d', shapePath('cookie9')); return undefined; }
      function frame(ts) {
        if (start === null) start = ts;
        var t = (ts - start) / 650, i = Math.floor(t) % LOADING_SEQ.length, f = t - Math.floor(t);
        var k = f < 0.5 ? 4 * f * f * f : 1 - Math.pow(-2 * f + 2, 3) / 2;
        el.setAttribute('d', morphPath(LOADING_SEQ[i], LOADING_SEQ[(i + 1) % LOADING_SEQ.length], k));
        el.setAttribute('transform', 'rotate(' + ((ts - start) / 4.2 % 360).toFixed(1) + ') scale(' + (0.92 + 0.08 * Math.sin(f * Math.PI)).toFixed(3) + ')');
        raf = requestAnimationFrame(frame);
      }
      raf = requestAnimationFrame(frame);
      return function () { cancelAnimationFrame(raf); };
    }, []);
    return h('span', { className: cx('ex-loading', p.contained && 'is-contained'), style: { width: size, height: size }, role: 'progressbar', 'aria-label': p.label || 'Loading' },
      h('svg', { viewBox: '-1.35 -1.35 2.7 2.7', 'aria-hidden': 'true' }, h('path', { ref: ref, d: shapePath('cookie9') })));
  }

  /* Split button: a main action and a menu trigger that rounds fully and spins its chevron when open. */
  function SplitButton(p) {
    var st = useState(!!p.defaultOpen), open = st[0];
    var variant = p.variant || 'filled';
    return h('div', { className: cx('ex-split', 'v-' + variant, open && 'is-open', p.size === 'md' && 'size-md') },
      h('button', { type: 'button', className: 'ex-press ex-split-main', onClick: p.onClick }, Icon(p.icon), p.children),
      h('button', { type: 'button', className: 'ex-press ex-split-trail', 'aria-label': p.menuLabel || 'More options', 'aria-expanded': open, 'aria-haspopup': 'menu', onClick: function () { st[1](!open); } }, Icon('keyboard_arrow_down')),
      open && p.items ? h('div', { className: 'ex-menu', role: 'menu' }, p.items.map(function (it) {
        return h('button', { key: it.label, type: 'button', role: 'menuitem', className: 'ex-press ex-menu-item', onClick: function () { st[1](false); if (it.onClick) it.onClick(); } }, Icon(it.icon), it.label);
      })) : null);
  }

  /* Floating toolbar: a pill of contextual actions that floats over content, optionally beside a FAB. */
  function FloatingToolbar(p) {
    var st = useState(p.defaultValue != null ? p.defaultValue : -1);
    var sel = p.value != null ? p.value : st[0];
    return h('div', { className: 'ex-ftb-wrap' },
      h('div', { className: cx('ex-ftb', p.vibrant && 'is-vibrant'), role: 'toolbar', 'aria-label': p.label || 'Actions' },
        p.items.map(function (it, i) {
          var on = i === sel;
          return h('button', { key: it.icon, type: 'button', className: cx('ex-press ex-ftb-btn', on && 'is-selected'), 'aria-label': it.label, 'aria-pressed': it.toggle ? on : undefined, onClick: function () { if (it.toggle) { if (p.value == null) st[1](on ? -1 : i); } if (it.onClick) it.onClick(); } }, Icon(it.icon, on));
        })),
      p.fab ? h(Fab, Object.assign({ tone: p.vibrant ? 'primary' : 'secondary' }, p.fab)) : null);
  }

  /* Digit roll: each character sits in its own cell and rolls when it changes. Increasing values roll up,
     decreasing values roll down; simultaneous changes start right to left, a stagger apart. */
  function RollCell(p) {
    var s = useState({ cur: p.ch, prev: null, n: 0, dir: p.dir }), st = s[0];
    if (st.cur !== p.ch) { st = { cur: p.ch, prev: st.cur, n: st.n + 1, dir: p.dir }; s[1](st); }
    var style = { animationDelay: (p.delay || 0) + 'ms' };
    var digit = /[0-9]/.test(st.cur);
    return h('span', { className: cx('ex-roll-cell', !digit && 'is-sep', st.prev != null && 'is-rolling', st.dir === 'down' ? 'dir-down' : 'dir-up') },
      st.prev != null ? h('span', { key: 'o' + st.n, className: 'ex-roll-out', style: style, 'aria-hidden': 'true', onAnimationEnd: function () { s[1](function (x) { return x.n === st.n ? Object.assign({}, x, { prev: null }) : x; }); } }, st.prev) : null,
      h('span', { key: 'i' + st.n, className: st.n ? 'ex-roll-in' : null, style: style }, st.cur));
  }
  function DigitRoll(p) {
    var lines = Array.isArray(p.value) ? p.value.map(String) : [String(p.value)];
    var prevRef = React.useRef(lines), dirRef = React.useRef('up');
    var joined = lines.join(''), prevJoined = prevRef.current.join('');
    if (joined !== prevJoined) {
      var a = parseFloat(prevJoined.replace(/[^0-9.]/g, '')), b = parseFloat(joined.replace(/[^0-9.]/g, ''));
      dirRef.current = p.direction && p.direction !== 'auto' ? p.direction : (isNaN(a) || isNaN(b) || b >= a ? 'up' : 'down');
      prevRef.current = lines;
    }
    var stagger = p.stagger == null ? 30 : p.stagger;
    var label = p.label || lines.join(p.stacked ? ' ' : '');
    return h('span', { className: cx('ex-roll', p.stacked && 'is-stacked', p.blur === false && 'no-blur', p.className || 'numeral-large'), role: 'text', 'aria-label': label, style: p.style },
      lines.map(function (line, li) {
        var chars = line.split('');
        return h('span', { key: li, className: 'ex-roll-line', 'aria-hidden': 'true' }, chars.map(function (ch, i) {
          var fromRight = chars.length - 1 - i;
          return h(RollCell, { key: fromRight, ch: ch, dir: dirRef.current, delay: fromRight * stagger });
        }));
      }));
  }

  /* Time picker dial: a circular dial with a spring-moving handle, plus the HH:MM fields and an AM/PM toggle. */
  function pad2(n) { return (n < 10 ? '0' : '') + n; }
  function TimePickerDial(p) {
    var is24 = !!p.is24h;
    var st = useState({ hour: p.defaultHour != null ? p.defaultHour : 7, minute: p.defaultMinute != null ? p.defaultMinute : 30 });
    var hour = p.hour != null ? p.hour : st[0].hour, minute = p.minute != null ? p.minute : st[0].minute;
    var ms = useState(p.defaultMode || 'hour'), mode = ms[0];
    var dragging = useState(false), drag = dragging[0];
    var angleRef = React.useRef(null), dialRef = React.useRef(null);
    function set(hh, mm) {
      if (hh === hour && mm === minute) return;
      if (p.hour == null) st[1]({ hour: hh, minute: mm });
      if (p.haptics !== false) haptic('tick');
      if (p.onChange) p.onChange({ hour: hh, minute: mm });
    }
    var pm = hour >= 12, h12 = hour % 12 === 0 ? 12 : hour % 12;
    var inner = is24 && mode === 'hour' && (hour === 0 || hour > 12);
    var unit = mode === 'hour' ? (hour % 12) : minute / 5;
    var target = unit * 30;
    /* shortest rotation path so 11 -> 12 turns forward, not all the way back */
    if (angleRef.current == null) angleRef.current = target;
    var delta = ((target - angleRef.current) % 360 + 540) % 360 - 180;
    angleRef.current += delta;
    var R = 128, rOuter = 100, rInner = 64, rHand = inner ? rInner : rOuter;
    function pick(e, done) {
      var box = dialRef.current.getBoundingClientRect();
      var x = e.clientX - box.left - box.width / 2, y = e.clientY - box.top - box.height / 2;
      var ang = (Math.atan2(x, -y) * 180 / Math.PI + 360) % 360, dist = Math.sqrt(x * x + y * y) / (box.width / 2) * R;
      if (mode === 'hour') {
        var k = Math.round(ang / 30) % 12, hh;
        if (is24) hh = dist < (rOuter + rInner) / 2 ? (k === 0 ? 0 : k + 12) : (k === 0 ? 12 : k);
        else hh = (k === 0 ? 12 : k) % 12 + (pm ? 12 : 0);
        set(hh, minute);
        if (done) ms[1]('minute');
      } else {
        set(hour, Math.round(ang / 6) % 60);
      }
    }
    function onDown(e) { e.currentTarget.setPointerCapture(e.pointerId); dragging[1](true); pick(e, false); }
    function onMove(e) { if (drag) pick(e, false); }
    function onUp(e) { if (!drag) return; dragging[1](false); pick(e, true); }
    function onKey(e) {
      var step = { ArrowUp: 1, ArrowRight: 1, ArrowDown: -1, ArrowLeft: -1 }[e.key];
      if (!step) return;
      e.preventDefault();
      if (mode === 'hour') set((hour + step + 24) % 24, minute); else set(hour, (minute + step + 60) % 60);
    }
    var labels = [];
    for (var i = 0; i < 12; i++) {
      var a = i * 30 * Math.PI / 180;
      var outerText = mode === 'hour' ? String(i === 0 ? 12 : i) : pad2(i * 5);
      var selOuter = mode === 'hour' ? (!inner && hour % 12 === i) : minute === i * 5;
      labels.push(h('text', { key: 'o' + i, x: Math.sin(a) * rOuter, y: -Math.cos(a) * rOuter, className: cx('lbl', selOuter && 'is-sel') }, outerText));
      if (is24 && mode === 'hour') {
        var v = i === 0 ? 0 : i + 12;
        labels.push(h('text', { key: 'i' + i, x: Math.sin(a) * rInner, y: -Math.cos(a) * rInner, className: cx('lbl is-inner', inner && hour === v && 'is-sel') }, pad2(v)));
      }
    }
    var offFive = mode === 'minute' && minute % 5 !== 0;
    return h('div', { className: 'ex-tpd', role: 'group', 'aria-label': p.label || 'Select time' },
      h('div', { className: 'ex-tpd-head' },
        h('div', { className: 'ex-tpd-fields' },
          h('button', { type: 'button', className: cx('ex-press ex-tpd-field', mode === 'hour' && 'is-active'), 'aria-label': 'Hour', 'aria-pressed': mode === 'hour', onClick: function () { ms[1]('hour'); } }, is24 ? pad2(hour) : h12),
          h('span', { className: 'ex-tpd-colon', 'aria-hidden': 'true' }, ':'),
          h('button', { type: 'button', className: cx('ex-press ex-tpd-field', mode === 'minute' && 'is-active'), 'aria-label': 'Minute', 'aria-pressed': mode === 'minute', onClick: function () { ms[1]('minute'); } }, pad2(minute))),
        is24 ? null : h('div', { className: 'ex-tpd-ampm', role: 'radiogroup', 'aria-label': 'AM or PM' },
          ['AM', 'PM'].map(function (x) {
            var on = (x === 'PM') === pm;
            return h('button', { key: x, type: 'button', role: 'radio', 'aria-checked': on, className: cx('ex-press', on && 'is-selected'), onClick: function () { if (!on) set((hour + 12) % 24, minute); } }, x);
          }))),
      h('div', { ref: dialRef, className: cx('ex-tpd-dial', drag && 'is-dragging'), role: 'slider', tabIndex: 0,
        'aria-label': mode === 'hour' ? 'Hour' : 'Minute', 'aria-valuemin': 0, 'aria-valuemax': mode === 'hour' ? 23 : 59, 'aria-valuenow': mode === 'hour' ? hour : minute,
        'aria-valuetext': mode === 'hour' ? (is24 ? pad2(hour) : h12 + (pm ? ' PM' : ' AM')) : minute + ' minutes',
        onPointerDown: onDown, onPointerMove: onMove, onPointerUp: onUp, onPointerCancel: function () { dragging[1](false); }, onKeyDown: onKey },
        h('svg', { viewBox: '-128 -128 256 256', 'aria-hidden': 'true' },
          h('circle', { className: 'face', r: R }),
          h('g', { className: 'hand', style: { transform: 'rotate(' + angleRef.current + 'deg)' } },
            h('line', { className: 'arm', x1: 0, y1: 0, x2: 0, y2: -rHand + 24 }),
            h('circle', { className: 'knob', cy: -rHand, r: 24 }),
            offFive ? h('circle', { className: 'dot', cy: -rHand, r: 3 }) : null),
          h('circle', { className: 'hub', r: 4 }),
          labels)));
  }

  /* Rotary dial: a drum seen edge-on, wearing the slider's anatomy. Graduations are projected around a cylinder,
     so they bunch toward the rim; the one under the centre is the marker. Drag or fling to turn; it snaps with a spring. */
  function RotaryDial(p) {
    var min = p.min || 0, max = p.max == null ? 60 : p.max, step = p.step || 1, major = p.majorEvery || 5;
    var st = useState(p.defaultValue != null ? p.defaultValue : min);
    var value = p.value != null ? p.value : st[0];
    var posS = useState(value), pos = posS[0];
    var drag = React.useRef(null), cancel = React.useRef(function () {}), lastEmit = React.useRef(value);
    var wrapRef = React.useRef(null), widthS = useState(320), width = widthS[0];
    React.useEffect(function () {
      var el = wrapRef.current; if (!el || !window.ResizeObserver) return undefined;
      var ro = new ResizeObserver(function (en) { widthS[1](en[0].contentRect.width); }); ro.observe(el);
      return function () { ro.disconnect(); };
    }, []);
    /* re-seat only on a genuinely external change, never on our own echo */
    React.useEffect(function () { if (value !== lastEmit.current && !drag.current) { lastEmit.current = value; cancel.current(); cancel.current = animateSpring(pos, value, 'spatial-default', posS[1]); } }, [value]);
    var stepRad = p.stepRadians || 0.08, R = width / 2 - 8, pxPerStep = R * stepRad;
    function clamp(v) { return Math.max(min, Math.min(max, v)); }
    function emit(v) {
      var snapped = clamp(Math.round(v / step) * step);
      if (snapped !== lastEmit.current) { lastEmit.current = snapped; if (p.haptics !== false) haptic('tick'); if (p.value == null) st[1](snapped); if (p.onChange) p.onChange(snapped); }
    }
    function settle(v, velocity) {
      var to = clamp(Math.round(v / step) * step);
      cancel.current();
      cancel.current = animateSpring(v, to, 'spatial-fast', function (x) { posS[1](x); }, function () { emit(to); }, velocity);
    }
    function onDown(e) { e.currentTarget.setPointerCapture(e.pointerId); cancel.current(); drag.current = { x: e.clientX, pos: pos, t: e.timeStamp, v: 0 }; }
    function onMove(e) {
      var d = drag.current; if (!d) return;
      var next = clamp(d.pos - (e.clientX - d.x) / pxPerStep * step);
      var dt = Math.max(1, e.timeStamp - d.t); d.v = (next - pos) / dt * 1000; d.t = e.timeStamp;
      posS[1](next); emit(next);
    }
    function onUp() {
      var d = drag.current; if (!d) return; drag.current = null;
      settle(clamp(pos + d.v * 0.12), d.v);
    }
    function onKey(e) {
      var dlt = { ArrowRight: step, ArrowUp: step, ArrowLeft: -step, ArrowDown: -step, PageUp: step * major, PageDown: -step * major }[e.key];
      if (e.key === 'Home') dlt = min - value; if (e.key === 'End') dlt = max - value;
      if (dlt == null) return; e.preventDefault();
      var to = clamp(value + dlt); emit(to); cancel.current(); cancel.current = animateSpring(pos, to, 'spatial-fast', posS[1]);
    }
    var ticks = [], cx0 = width / 2, H = p.height || 76, vis = Math.ceil(Math.PI / 2 / stepRad);
    var centreIdx = Math.round(pos / step);
    for (var i = centreIdx - vis; i <= centreIdx + vis; i++) {
      var v = i * step; if (v < min || v > max) continue;
      var th = (v - pos) / step * stepRad; if (Math.abs(th) >= Math.PI / 2) continue;
      var depth = Math.cos(th), isMajor = Math.round(v / step) % major === 0, near = Math.abs(v - pos) < step / 2;
      var tw = 1 + depth * (isMajor ? 2.2 : 1.4), th2 = isMajor ? H * 0.46 : H * 0.3;
      ticks.push(h('rect', { key: v, className: cx('tick', near && 'is-centre', isMajor && 'is-major'), x: cx0 + R * Math.sin(th) - tw / 2, y: (H - th2) / 2, width: tw, height: th2, rx: tw / 2, opacity: near ? 1 : 0.18 + 0.7 * depth * depth }));
    }
    var fmt = p.format || function (x) { return x; };
    return h('div', { className: 'ex-rotary' },
      p.label ? h('div', { className: 'ex-slider-head' }, h('span', { className: 'l' }, p.label), h('span', { className: 'v' }, fmt(value))) : null,
      h('div', { ref: wrapRef, className: 'ex-rotary-drum', role: 'slider', tabIndex: 0, 'aria-label': p.label, 'aria-valuemin': min, 'aria-valuemax': max, 'aria-valuenow': value, 'aria-valuetext': String(fmt(value)),
        style: { height: H }, onPointerDown: onDown, onPointerMove: onMove, onPointerUp: onUp, onPointerCancel: onUp, onKeyDown: onKey },
        h('svg', { width: '100%', height: H, viewBox: '0 0 ' + width + ' ' + H, 'aria-hidden': 'true' }, ticks),
        h('span', { className: 'ex-rotary-notch', 'aria-hidden': 'true' })));
  }

  /* Navigation rail: medium and larger windows. Collapsed shows icon + label stacks; expanded shows full rows. */
  function NavigationRail(p) {
    var st = useState(p.defaultValue != null ? p.defaultValue : 0), active = p.value != null ? p.value : st[0];
    var ex = useState(!!p.defaultExpanded), expanded = p.expanded != null ? p.expanded : ex[0];
    function toggle() { if (p.expanded == null) ex[1](!expanded); if (p.onExpandedChange) p.onExpandedChange(!expanded); }
    return h('nav', { className: cx('ex-rail', expanded && 'is-expanded', p.className), 'aria-label': p.label || 'Main' },
      h('div', { className: 'ex-rail-top' },
        p.menu === false ? null : h(IconButton, { icon: expanded ? 'menu_open' : 'menu', label: expanded ? 'Collapse navigation' : 'Expand navigation', onClick: toggle }),
        p.fab ? h('button', { type: 'button', className: cx('ex-press ex-fab ex-rail-fab', 't-' + (p.fab.tone || 'primary'), expanded && 'has-label'), 'aria-label': expanded ? undefined : p.fab.label, onClick: p.fab.onClick }, Icon(p.fab.icon, true), h('span', { className: 'ex-rail-fab-label' }, p.fab.label)) : null),
      h('div', { className: 'ex-rail-items' }, p.items.map(function (it, i) {
        var on = i === active;
        return h('button', { key: it.label, type: 'button', className: cx('ex-press ex-railitem', on && 'is-active'), 'aria-current': on ? 'page' : undefined, onClick: function () { if (p.value == null) st[1](i); if (p.onChange) p.onChange(i); } },
          h('span', { className: 'ex-railpill' }, Icon(it.icon, on), h('span', { className: 'ex-raillabel-in' }, it.label), it.badge ? h(Badge, { count: it.badge, tone: 'error' }) : null),
          h('span', { className: 'ex-raillabel' }, it.label));
      })));
  }

  var api = { DigitRoll: DigitRoll, TimePickerDial: TimePickerDial, RotaryDial: RotaryDial, NavigationRail: NavigationRail, LoadingIndicator: LoadingIndicator, SplitButton: SplitButton, FloatingToolbar: FloatingToolbar, Button: Button, IconButton: IconButton, Fab: Fab, ButtonGroup: ButtonGroup, Chip: Chip, Badge: Badge, ValuePill: ValuePill, NavigationBar: NavigationBar, TopBar: TopBar, SearchBar: SearchBar, TextField: TextField, Switch: Switch, Slider: Slider, WavyProgress: WavyProgress, Card: Card, ListItem: ListItem, GroupedList: GroupedList, StatTile: StatTile, ShapeAvatar: ShapeAvatar, BottomSheet: BottomSheet, SummaryList: SummaryList, Snackbar: Snackbar };
  api.motion = { spring: spring, animate: animateSpring, haptic: haptic, reducedMotion: reducedMotion, springs: SPRINGS };
  window.Expressive = Object.assign(window.Expressive || {}, api);
})();
