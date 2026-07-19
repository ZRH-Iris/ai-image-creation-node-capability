#!/usr/bin/env node
const path = require('path');
const fs = require('fs');
function loadSharp() {
  const candidates = [
    'sharp',
    process.env.SHARP_MODULE_PATH,
    `${process.env.HERMES_IMAGE_RUNTIME || `${process.env.HOME}/.hermes-image-runtime`}/image-layout/node_modules/sharp`,
  ].filter(Boolean);
  for (const name of candidates) {
    try { return require(name); } catch (_) {}
  }
  throw new Error('Cannot load sharp. Install with: npm install sharp, or set SHARP_MODULE_PATH=/path/to/node_modules/sharp');
}
const sharp = loadSharp();
const runtimeRoot = process.env.HERMES_IMAGE_RUNTIME || `${process.env.HOME}/.hermes-image-runtime`;

const args = Object.fromEntries(process.argv.slice(2).map(s => {
  const i = s.indexOf('=');
  return i > 0 ? [s.slice(0, i), s.slice(i + 1)] : [s, true];
}));

const bg = args.bg || path.join(runtimeRoot, 'commercial-image-runtime-tests/product-poster/pillow_product_pedestal_bg_00001_.png');
const product = args.product || path.join(runtimeRoot, 'commercial-image-runtime-tests/sam/pillow_sam_cutout.png');
const out = args.out || path.join(runtimeRoot, 'commercial-image-runtime-tests/product-poster/final_product_poster.png');
const title = args.title || '山水抱枕';
const subtitle = args.subtitle || '把东方山水的松弛感，放进客厅';
const kicker = args.kicker || '东方织纹 · 家居软装';
const caption = args.caption || '暖金山形轮廓 / 细腻山水肌理 / 空间点睛单品';

function captionItems(s) {
  return String(s).split(/[\/｜|]/).map(x => x.trim()).filter(Boolean).slice(0, 3);
}

async function makeSvg() {
  const items = captionItems(caption);
  const pills = items.map((item, i) => {
    const x = 42 + i * 296;
    return `<g transform="translate(${x} 50)">
      <rect x="0" y="0" width="260" height="62" rx="31" fill="#f8e6cf" fill-opacity="0.92"/>
      <text x="130" y="40" text-anchor="middle" font-family="Noto Sans CJK SC, Noto Sans CJK, sans-serif" font-size="25" font-weight="800" fill="#613512" letter-spacing="0.4">${escapeXml(item)}</text>
    </g>`;
  }).join('\n');

  return Buffer.from(`
  <svg width="1080" height="1350" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="fadeTop" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#211207" stop-opacity="0.56"/>
        <stop offset="0.54" stop-color="#211207" stop-opacity="0.14"/>
        <stop offset="1" stop-color="#211207" stop-opacity="0"/>
      </linearGradient>
      <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
        <feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#3b210c" flood-opacity="0.22"/>
      </filter>
    </defs>
    <rect width="1080" height="1350" fill="url(#fadeTop)"/>
    <g filter="url(#softShadow)">
      <rect x="64" y="70" rx="27" width="314" height="56" fill="#f6dfc2" fill-opacity="0.94"/>
    </g>
    <text x="91" y="107" font-family="Noto Sans CJK SC, Noto Sans CJK, sans-serif" font-size="25" font-weight="800" fill="#6a3d14" letter-spacing="1.5">${escapeXml(kicker)}</text>
    <text x="64" y="225" font-family="Noto Serif CJK SC, Noto Serif CJK, serif" font-size="96" font-weight="900" fill="#fff4e5" letter-spacing="2.2">${escapeXml(title)}</text>
    <text x="70" y="292" font-family="Noto Sans CJK SC, Noto Sans CJK, sans-serif" font-size="31" font-weight="600" fill="#fff1dd" letter-spacing="0.8">${escapeXml(subtitle)}</text>
    <line x1="72" y1="334" x2="388" y2="334" stroke="#f3c37a" stroke-width="5" stroke-linecap="round"/>

    <g transform="translate(64 1130)">
      <rect x="0" y="0" width="952" height="144" rx="34" fill="#fff8ee" fill-opacity="0.86"/>
      <text x="42" y="34" font-family="Noto Sans CJK SC, Noto Sans CJK, sans-serif" font-size="22" font-weight="800" fill="#8b6239" letter-spacing="3">产品亮点</text>
      ${pills}
    </g>
    <text x="836" y="108" font-family="Noto Sans CJK SC, Noto Sans CJK, sans-serif" font-size="23" font-weight="800" fill="#fff3de" opacity="0.92" letter-spacing="2">2026 NEW</text>
  </svg>`);
}
function escapeXml(s){return String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}

async function main(){
  fs.mkdirSync(path.dirname(out), {recursive:true});
  const W=1080, H=1350;
  const bgBuf = await sharp(bg).resize(W,H,{fit:'cover',position:'center'}).modulate({brightness:0.98,saturation:0.92}).png().toBuffer();

  const prodMeta = await sharp(product).metadata();
  const productWidth = Math.round(W * 0.82);
  const prodBuf = await sharp(product)
    .trim({background:{r:0,g:0,b:0,alpha:0}, threshold:4})
    .resize({width: productWidth, withoutEnlargement: true})
    .modulate({brightness:1.04, saturation:1.03})
    .png().toBuffer();
  const resizedMeta = await sharp(prodBuf).metadata();
  const px = Math.round((W - resizedMeta.width)/2);
  const py = 555;

  // Contact shadow under the real product: deterministic layer, not AI redraw.
  const shadowSvg = Buffer.from(`<svg width="1080" height="1350" xmlns="http://www.w3.org/2000/svg">
    <ellipse cx="540" cy="990" rx="365" ry="58" fill="#5a3217" opacity="0.24" filter="blur(20px)"/>
  </svg>`);

  const overlay = await makeSvg();
  await sharp(bgBuf)
    .composite([
      {input: shadowSvg, left:0, top:0},
      {input: prodBuf, left:px, top:py},
      {input: overlay, left:0, top:0}
    ])
    .png({quality:96, compressionLevel:8})
    .toFile(out);
  const meta = await sharp(out).metadata();
  console.log(JSON.stringify({out, width:meta.width, height:meta.height, bg, product}, null, 2));
}

main().catch(e => { console.error(e); process.exit(1); });
