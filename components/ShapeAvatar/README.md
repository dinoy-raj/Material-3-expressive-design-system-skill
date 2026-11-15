# ShapeAvatar

Letter, icon or illustration seat cut from the M3 Expressive shape library.

**Provide:** `shape`, `text` (one letter) or `icon`, `tone`, `size` (px, default 40), `label` for a meaningful image, `spin` for a slow decorative rotation on hero moments, `morph={false}` to swap shapes without animating.

**Shapes (25):** `circle`, `cookie4`, `cookie6`, `cookie7`, `cookie9`, `cookie12`, `clover4`, `clover8`, `flower5`, `flower8`, `sunny`, `softBurst`, `burst`, `boom`, `pebble`, `puffy`, `square`, `pill`, `oval`, `diamond`, `triangle`, `pentagon`, `gem`, `heart`, `arch`. `ShapeAvatar.shapes` lists them.

- Give each entity type one shape and keep it (tickers are cookie9, collections are clover4, agents are flower5). Colour can vary per item; the shape stays.
- Use big shapes (96px+) behind hero icons, a book cover, a mascot, the app's icon.
- Changing `shape` morphs from the old shape to the new one on the `spatial-default` spring. Use it for selection (a circle becomes a cookie when picked) or a state change (pending pebble becomes a done flower). With reduced motion it swaps instantly.
- `ShapeAvatar.path(name)` returns the SVG path (viewBox -1 -1 2 2) for clipping images or drawing your own; `ShapeAvatar.morph(a, b, k)` returns the blended path at progress `k`.

**Compose:** `MaterialShapes.Cookie9Sided.toShape()` and friends; morph with `Morph(start, end)` from `androidx.graphics.shapes` (see `docs/motion.md`).
