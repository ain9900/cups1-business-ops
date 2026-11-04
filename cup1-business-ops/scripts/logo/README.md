# Logo build scripts (v1.1 Rim Monogram)

- `glyphs.py`: outlines text to SVG paths with fontTools (needs Inter Display ExtraBold/Black installed; free from rsms.me/inter).
- `build_logo.py`: builds all SVG versions, favicon.svg, site.webmanifest and the HTML snippet into `out/`.
- `render.js`: renders PNGs and favicon sizes with Playwright (`npm i playwright`).
- `concepts.py`: the round-1 concept board (A, B, C).

Build: `python build_logo.py && node render.js`, then make `favicon.ico` from `fav-16/32/48.png` with Pillow.
Note: font paths in the scripts point to `/usr/share/fonts/opentype/inter/`; change them for Windows/macOS.
