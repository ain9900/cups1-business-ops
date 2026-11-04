const { chromium } = require('playwright'); const fs=require('fs'), path=require('path');
const D=__dirname, O=path.join(D,'v12');
async function shot(p,f,w,h,out,bg){const svg=fs.readFileSync(f,'utf8').replace(/width="[^"]*" height="[^"]*"/,`width="${w}" height="${h}"`);await p.setViewportSize({width:w,height:h});await p.setContent(`<html><body style="margin:0;background:${bg||'transparent'}">${svg}</body></html>`);await p.screenshot({path:out,omitBackground:!bg,clip:{x:0,y:0,width:w,height:h}});}
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for(const f of fs.readdirSync(path.join(O,'svg'))){const s=fs.readFileSync(path.join(O,'svg',f),'utf8');const m=s.match(/viewBox="[-\d.]+ [-\d.]+ ([\d.]+) ([\d.]+)"/);const ar=(+m[1])/(+m[2]);
 for(const W of (f.includes('icon')?[512,1024]:[1024,2048])) await shot(p,path.join(O,'svg',f),W,Math.round(W/ar),path.join(O,'png',f.replace('.svg',`-${W}.png`)));}
for(const z of [16,32,48]) await shot(p,path.join(O,'fav_tile_heavy.svg'),z,z,path.join(O,`fav-${z}.png`));
await shot(p,path.join(O,'apple_square.svg'),180,180,path.join(O,'favicon','apple-touch-icon.png'),'#1F4E5A');
await shot(p,path.join(O,'svg','cup1-icon-tile.svg'),192,192,path.join(O,'favicon','icon-192.png'));
await shot(p,path.join(O,'svg','cup1-icon-tile.svg'),512,512,path.join(O,'favicon','icon-512.png'));
await shot(p,path.join(O,'maskable.svg'),512,512,path.join(O,'favicon','icon-maskable-512.png'),'#1F4E5A');
await b.close();})();
