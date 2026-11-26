// Renderiza um motor de estilo (HTML com window.seek(t)) quadro a quadro, via Playwright/Chromium.
// Uso: node render.cjs <estilo.html> <timeline.json> <pasta_frames> [test|full]
//   test  -> gera 1 quadro por cena (t<nome>_<i>.png na pasta atual) para conferência rápida
//   full  -> gera todos os quadros (f00000.png ...) na pasta de frames
// Requer que logo.png esteja na MESMA pasta do HTML (o HTML referencia "logo.png").
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');

(async () => {
  const [html, tlPath, framesDir, mode = 'full'] = process.argv.slice(2);
  if (!html || !tlPath) { console.error('uso: node render.cjs <estilo.html> <timeline.json> <frames> [test|full]'); process.exit(1); }
  const tl = JSON.parse(fs.readFileSync(tlPath, 'utf8'));
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const pg = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await pg.goto('file://' + path.resolve(html));
  await pg.waitForFunction('window.__ready===true');
  await pg.evaluate((d) => window.setTimeline(d), tl);
  await pg.evaluate(() => document.fonts.ready);
  await pg.waitForTimeout(500);
  if (mode === 'test') {
    for (const s of tl.scenes) { const tt = (s.start + s.end) / 2; await pg.evaluate((x) => window.seek(x), tt); await pg.screenshot({ path: `teste_${s.i}.png` }); }
    console.log('quadros de teste: teste_1.png ...');
  } else {
    fs.mkdirSync(framesDir, { recursive: true });
    const fps = tl.fps || 30, N = Math.ceil(tl.total * fps);
    for (let f = 0; f < N; f++) { await pg.evaluate((x) => window.seek(x), f / fps); await pg.screenshot({ path: path.join(framesDir, `f${String(f).padStart(5, '0')}.png`) }); }
    console.log('frames:', N);
  }
  await b.close();
})();
