import { chromium } from '@playwright/test';
import { mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const deck = 'file://' + join(here, 'directions.html');
const out = join(here, 'stills');
mkdirSync(out, { recursive: true });

const DIRS = ['a', 'b', 'c'];
const STATES = ['empty', 'valid', 'list', 'landing'];

const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 1540, height: 1000 } });
await page.goto(deck);
await page.evaluate(() => document.fonts.ready);

let overflow = 0;
for (const d of DIRS) {
	for (const s of STATES) {
		await page.click(`[data-dir-btn="${d}"]`);
		await page.click(`[data-set="${s}"]`);
		await page.waitForTimeout(700);
		const wide = await page.$eval('#screen-phone', (el) => el.scrollWidth > el.clientWidth);
		if (wide) {
			overflow++;
			console.error(`overflow: ${d}/${s}`);
		}
		await page.locator('#stage').screenshot({ path: join(out, `${d}-${s}.png`) });
		console.log(`${d}-${s}.png`);
	}
}
await browser.close();
process.exit(overflow ? 1 : 0);
