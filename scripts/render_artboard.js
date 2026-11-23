// Renderiza artboards .dc.html do canvas em JPEG 1080x1350.
// Uso: node scripts/render_artboard.js <pasta_com_assets_baixados> <arquivo.dc.html> <saida.jpg> [...]
// Os /_blob/<id> do HTML viram arquivos <id>.* da pasta de assets.
const { chromium } = require('playwright');
const fs = require('fs');
const [,, A, ...pairs] = process.argv;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  for (let i = 0; i < pairs.length; i += 2) {
    let html = fs.readFileSync(pairs[i], 'utf8').replace(/\/_blob\/([0-9a-f]{32})/g, (m, id) => {
      const f = fs.readdirSync(A).find(x => x.startsWith(id)); return 'file://' + A + '/' + f; });
    const tmp = pairs[i] + '.render.html'; fs.writeFileSync(tmp, html);
    await p.goto('file://' + tmp, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    const fam = await p.evaluate(() => document.fonts.check('800 72px Poppins'));
    await p.locator('body > x-dc > div').first().screenshot({ path: pairs[i+1], type: 'jpeg', quality: 92 });
    console.log(pairs[i+1], 'poppins:', fam); fs.unlinkSync(tmp);
  }
  await b.close();
})();
