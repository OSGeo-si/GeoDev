#!/usr/bin/env node
/**
 * banner-to-png.js
 *
 * Render fixed-pixel HTML banners (with a `.banner` element of explicit
 * width/height) to PNG images. Built for the meetup story/landscape banners
 * under YYYY-NN-meetup/.
 *
 * Usage:
 *   node banner-to-png.js <html...> [--out=DIR] [--scale=2] [--selector=.banner]
 *
 * Examples:
 *   node banner-to-png.js ../2026-15-meetup/banner-story.html
 *   node banner-to-png.js ../2026-15-meetup/banner-*.html --scale=2
 *   node banner-to-png.js ../2026-15-meetup/banner-story.html --out=/tmp
 *
 * Flags:
 *   --out=DIR        output directory (default: alongside each source HTML)
 *   --scale=N        device pixel ratio (default: 2 → e.g. 1080×1920 banner
 *                    renders as a 2160×3840 PNG). Pass 1 for native size.
 *   --selector=SEL   element to screenshot (default: .banner). The element
 *                    must have a fixed pixel width and height in CSS.
 *
 * Setup (one-time):
 *   cd scripts && npm install && npx playwright install chromium
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const url = require('url');

function parseArgs() {
  const argv = process.argv.slice(2);
  const files = [];
  const opts = { out: null, scale: 2, selector: '.banner' };

  for (const a of argv) {
    if (a.startsWith('--out=')) opts.out = path.resolve(a.slice(6));
    else if (a.startsWith('--scale=')) opts.scale = Number(a.slice(8)) || 2;
    else if (a.startsWith('--selector=')) opts.selector = a.slice(11);
    else if (a.startsWith('--')) {
      console.error(`Unknown flag: ${a}`);
      process.exit(1);
    } else {
      files.push(path.resolve(a));
    }
  }

  if (files.length === 0) {
    console.error(
      'Usage: node banner-to-png.js <html...> [--out=DIR] [--scale=2] [--selector=.banner]'
    );
    process.exit(1);
  }
  return { files, opts };
}

async function renderOne(page, htmlPath, opts) {
  if (!fs.existsSync(htmlPath)) {
    console.warn(`  ✗ ${htmlPath} — not found, skipping`);
    return;
  }

  const fileUrl = url.pathToFileURL(htmlPath).href;
  await page.goto(fileUrl, { waitUntil: 'networkidle' });

  // Wait for web fonts so the screenshot doesn't catch FOUT.
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await page.waitForTimeout(150);

  const el = await page.$(opts.selector);
  if (!el) {
    console.warn(`  ✗ ${path.basename(htmlPath)} — '${opts.selector}' not found, skipping`);
    return;
  }

  const outDir = opts.out || path.dirname(htmlPath);
  fs.mkdirSync(outDir, { recursive: true });
  const baseName = path.basename(htmlPath, path.extname(htmlPath));
  const outPath = path.join(outDir, `${baseName}.png`);

  await el.screenshot({ path: outPath, type: 'png', omitBackground: false });

  const box = await el.boundingBox();
  const wOut = Math.round((box?.width ?? 0) * opts.scale);
  const hOut = Math.round((box?.height ?? 0) * opts.scale);
  console.log(`  ✔ ${path.basename(htmlPath)}  →  ${path.basename(outPath)}  (${wOut}×${hOut})`);
}

async function main() {
  const { files, opts } = parseArgs();

  console.log(`→ Rendering ${files.length} banner(s) at ${opts.scale}× device pixel ratio`);

  const browser = await chromium.launch();
  const context = await browser.newContext({
    deviceScaleFactor: opts.scale,
    // Generous viewport — the .banner element has its own fixed size; this
    // just needs to be at least as large so layout doesn't reflow.
    viewport: { width: 2000, height: 2400 },
  });
  const page = await context.newPage();
  page.on('pageerror', (err) => console.warn('  [page error]', err.message));

  for (const f of files) {
    await renderOne(page, f, opts);
  }

  await browser.close();
  console.log(`✔ Done.`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
