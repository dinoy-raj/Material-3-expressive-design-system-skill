# Seed palettes

The default tokens use a rust primary on warm paper. To give a product its own voice, keep every token name and swap the values below. Each row was sampled from the reference screens (light / dark). Generate the full container ramps from the seed with Material Theme Builder, then check `on-*` pairs at 4.5:1.

| Product | Seed | `surface` | `primary` | Accent fills | Display face | Signature shape |
| --- | --- | --- | --- | --- | --- | --- |
| Sherwood (finance) | `#b3ee46` | `#f6f5ef` / `#0b0d0a` | `#3d5a00` / `#c8f542` | loss `#c2331a` / `#ff6a45` | Instrument Serif, Bricolage Grotesque, Geist Mono | cookie9 |
| Trill (music learning) | `#ffb79e` | `#fbf6ee` / `#15121f` | `#b83a14` / `#ffb59c` | `#ffdbcf`, `#f3daff`, `#a6f0ef` | Fraunces | clover4 |
| Greenwave (cycling) | `#81dfa2` | `#f6fbf4` / `#0f1511` | `#1b6b4a` / `#7fd9a3` | score burst in primary | Google Sans Flex only | cookie12 |
| Magpie (design chat) | `#b8a9ff` | `#f4f1ea` / `#121110` | `#1b1a17` / `#f1ede4` | hot pink `#e40078` | Instrument Serif, Bricolage Grotesque, Geist Mono | flower5 |
| Prime Meridian (jet lag) | `#ffd07b` | `#fbf7f0` / `#0d0f1f` | `#8a5000` / `#ffb94f` | indigo `#2c3a8f` / `#8490e4` | Doto, Google Sans Code | sunny |
| Shelfie (home library) | `#b4532f` | `#fff8f4` / `#1b1107` | `#9d4220` / `#ffb59c` | teal `#2c6765` / `#97d1ce` | Fraunces | cookie6 |
| Dollop (bakery delivery) | `#e0507f` | `#fff8f6` / `#1b0a03` | `#af295a` / `#ffb1c3` | brown `#845424`, apricot `#f0b478` | DynaPuff, Shrikhand | burst |
| Tern (travel points) | `#1f3fb8` | `#fff8f8` / `#190911` | `#954271` / `#ffc4df` | violet `#48249c`, mint `#6cf0d8` | Big Shoulders Display | pebble |
| Pinhole (photography) | `#e0891f` | `#fff5ec` / `#170c00` | `#844800` / `#ffb84d` | highlight `#fc9500` | Fraunces, Google Sans Code | cookie4 |
| Heliotrope (home solar) | `#7652c9` | `#fdf3ff` / `#170529` | `#6b34d8` / `#ba9eff` | amber `#e49000`, green `#189c60` | Google Sans Code | flower8 |

## How the references use them

- **Neutral-first** brands (Magpie) make `primary` near-black ink and let a single hot accent and user content (palettes, photos) bring colour. Use Button `tone="ink"`.
- **Two-voice** brands (Shelfie, Prime Meridian, Tern) pair a warm `primary` with a cool `secondary` and assign each a job: primary for actions, secondary for selection and settings.
- **Data** brands (Sherwood, Heliotrope) reserve their brightest colours for chart series and gain/loss, and keep chrome neutral.
- **Playful** brands (Trill, Dollop, Pinhole) give each hub card a different container colour and lean on a mascot illustration and a characterful display face.
- Dark surfaces follow the brand's hue: green-black for Sherwood, aubergine for Heliotrope, navy for Prime Meridian, cocoa for Dollop. Never use a neutral grey `#121212`.
