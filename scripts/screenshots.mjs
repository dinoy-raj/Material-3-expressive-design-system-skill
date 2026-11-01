// Renders the README and site images with Playwright:
//   assets/banner-light.png, assets/banner-dark.png      feature graphic (1280x640 at 2x)
//   assets/hero-light.png, assets/hero-dark.png          phone-only crop for the website hero
//   assets/components/<Name>-light.png / -dark.png       one image per component preview
// Usage, from the repository root:  npx playwright install chromium && node scripts/screenshots.mjs
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import { readFileSync, readdirSync, writeFileSync, mkdirSync, existsSync, rmSync } from 'node:fs';
import { join, resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const out = join(root, 'assets');
mkdirSync(join(out, 'components'), { recursive: true });

const head = `<link rel="stylesheet" href="${root}/tokens/tokens.css"><link rel="stylesheet" href="${root}/components/bundle.css">
<script src="https://cdn.jsdelivr.net/npm/react@18.3.1/umd/react.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/react-dom@18.3.1/umd/react-dom.production.min.js"></script>
<script src="${root}/components/bundle.js"></script>
<style>body{width:560px;padding:8px 4px;box-sizing:border-box}#root{display:inline-block;min-width:520px}</style>`;

const browser = await chromium.launch();
const errors = [];
for (const theme of ['light', 'dark']) {
  const page = await browser.newPage({ deviceScaleFactor: 2, viewport: { width: 1280, height: 640 }, colorScheme: theme });
  page.on('pageerror', (e) => errors.push(e.message));

  await page.goto('file://' + join(root, 'scripts/banner.html'));
  await page.evaluate((t) => { document.documentElement.dataset.theme = t; }, theme);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1200);
  await page.screenshot({ path: join(out, `banner-${theme}.png`) });
  await page.screenshot({ path: join(out, `hero-${theme}.png`), clip: { x: 600, y: 0, width: 680, height: 640 } });

  await page.setViewportSize({ width: 560, height: 800 });
  for (const name of readdirSync(join(root, 'components')).sort()) {
    const file = join(root, 'components', name, 'preview.html');
    if (name === 'Cover' || !existsSync(file)) continue;
    const html = readFileSync(file, 'utf8').replace('<head>', '<head>' + head).replace('<html', `<html data-theme="${theme}"`);
    const tmp = join(root, 'scripts', `.shot-${name}.html`);
    writeFileSync(tmp, html);
    await page.goto('file://' + tmp);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(name === 'LoadingIndicator' ? 900 : 500);
    await page.locator('#root').screenshot({ path: join(out, 'components', `${name}-${theme}.png`), omitBackground: false });
    rmSync(tmp);
  }
  await page.close();
}
await browser.close();
if (errors.length) { console.error(errors); process.exit(1); }
console.log('Wrote assets/banner-*.png and assets/components/*.png');
