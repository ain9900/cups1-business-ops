const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const D = __dirname, OUT = path.join(D, 'out');
async function shot(page, svgFile, w, h, out, bg) {
  const svg = fs.readFileSync(svgFile, 'utf8').replace(/width="[^"]*" height="[^"]*"/, `width="${w}" height="${h}"`);
  await page.setViewportSize({ width: w, height: h });
  await page.setContent(`<html><body style="margin:0;background:${bg || 'transparent'}">${svg}</body></html>`);
  await page.screenshot({ path: out, omitBackground: !bg, clip: { x: 0, y: 0, width: w, height: h } });
}
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const svgDir = path.join(OUT, 'svg');
  for (const f of fs.readdirSync(svgDir)) {
    const src = fs.readFileSync(path.join(svgDir, f), 'utf8');
    const m = src.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/); const ar = (+m[1]) / (+m[2]);
    for (const W of (f.includes('icon') ? [512, 1024] : [1024, 2048])) {
      const H = Math.round(W / ar);
      await shot(p, path.join(svgDir, f), W, H, path.join(OUT, 'png', f.replace('.svg', `-${W}.png`)));
    }
  }
  const fav = path.join(OUT, 'favicon');
  for (const z of [16, 32, 48]) await shot(p, path.join(OUT, 'favicon_small_tile.svg'), z, z, path.join(D, `fav-${z}.png`));
  await shot(p, path.join(OUT, 'favicon_full_tile_square.svg'), 180, 180, path.join(fav, 'apple-touch-icon.png'), '#1F4E5A');
  await shot(p, path.join(OUT, 'svg', 'cup1-icon-tile.svg'), 192, 192, path.join(fav, 'icon-192.png'));
  await shot(p, path.join(OUT, 'svg', 'cup1-icon-tile.svg'), 512, 512, path.join(fav, 'icon-512.png'));
  await shot(p, path.join(OUT, 'maskable.svg'), 512, 512, path.join(fav, 'icon-maskable-512.png'), '#1F4E5A');
  await b.close();
})();
