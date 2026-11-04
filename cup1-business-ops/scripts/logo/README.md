# Logo build scripts (v1.2: "Cup" + cup-1)

- `round2.py`: text outlining helpers + the round-2 concept board (teal, navy+orange, navy+orange-1).
- `build_v12.py`: builds the final SVG set (horizontal color/reversed/black/white, icon, tile), favicon.svg, site.webmanifest and HTML snippet into `v12/`.
- `render12.js`: renders PNGs, favicon sizes, apple-touch and Android icons with Playwright (`npm i playwright`).
- `glyphs.py`: older helper used by round 1 (v1.1 Rim Monogram, superseded).

Build: `python build_v12.py && node render12.js`, then make `favicon.ico` from `v12/fav-16/32/48.png` with Pillow.
Fonts: Inter Display Black (rsms.me/inter, SIL OFL). Paths in the scripts point to `/usr/share/fonts/opentype/inter/`; change them on Windows/macOS.
