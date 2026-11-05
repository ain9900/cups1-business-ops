# Cups1 logo v2.0 (owner's pick, 2026-11-06)

Vector rebuild of owner-shortlisted **Sample 1** (`brand/logo/references/sample-1-navy-cup-steam-leaf.png`), spelled **Cups1**.
All text is outlined to paths (no font needed). v1.2 ("Cup" + teal cup-1) files in `brand/logo/svg|png|favicon` are kept for reference.

| File | Use |
|---|---|
| `svg/cups1-logo-full-color.svg` (+ `-reversed`, `-black`) | Full logo with steam, swoosh and tagline: packaging, decks, banners, print (min. width 240px / 60mm) |
| `svg/cups1-logo-color.svg` (+ `-reversed`) | No tagline: social headers, email signature, large website hero |
| `svg/cups1-logo-nav-color.svg` (+ `-reversed`) | Simplified (no steam, no swoosh): website navbar at 24–40px tall, invoices, small print |
| `svg/cups1-icon-color.svg`, `svg/cups1-icon-tile.svg` | Cup icon alone: social avatar, app icon |
| `favicon/` | favicon.ico (16/32/48), favicon.svg, apple-touch-icon, 192/512, maskable, site.webmanifest, HTML snippet |

**Colours:** Navy #102A4C (text, cup), Orange #F28A1B (the 1, steam, swoosh, buttons), Leaf green #5FA136 (leaf only).
Orange on white is about 2.6:1 contrast: fine for the logo and large shapes, but don't use it for small body text.
**Font of the wordmark:** Inter Display Black (outlined) + custom slab "1"; tagline Inter Medium.
**Watch:** the leaf suggests an environmental benefit. Under our claims rule, back it with documents (FSC, BPI, PFAS-free) on the site and packaging, or use a version without the leaf.
Rebuild: `python3 build_cups1.py && node render_cups.js` (needs the scripts in `scripts/logo/`).
