const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
async function r(svgFile,out,w,h){const svg=fs.readFileSync(svgFile,'utf8');const m=svg.match(/viewBox="([^"]+)"/)[1].split(' ').map(Number);
 if(!h)h=Math.round(w*m[3]/m[2]);await p.setViewportSize({width:w,height:h});
 await p.setContent(`<html><body style="margin:0;background:transparent">${svg.replace(/width="[^"]*" height="[^"]*"/,`width="${w}" height="${h}"`)}</body></html>`);
 await p.screenshot({path:out,omitBackground:true,clip:{x:0,y:0,width:w,height:h}});}
const S='cups1/svg/',P='cups1/png/',F='cups1/favicon/';
for(const f of fs.readdirSync(S)){const n=f.replace('.svg','');await r(S+f,P+n+(f.includes('icon')?'-1024.png':'-2048.png'),f.includes('icon')?1024:2048);}
for(const z of [16,32,48])await r('cups1/fav_small.svg',`cups1/fav-${z}.png`,z,z);
await r('cups1/apple_square.svg',F+'apple-touch-icon.png',180,180);
await r('cups1/svg/cups1-icon-tile.svg',F+'icon-192.png',192,192);
await r('cups1/svg/cups1-icon-tile.svg',F+'icon-512.png',512,512);
await r('cups1/maskable.svg',F+'icon-maskable-512.png',512,512);
await b.close();})();
