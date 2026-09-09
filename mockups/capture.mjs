import { chromium } from '@playwright/test';
import { mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const deckName = process.argv[2] || 'card';
const here = dirname(fileURLToPath(import.meta.url));
const deck = 'file://' + join(here, `${deckName}.html`);
const out = join(here, 'stills', deckName);
mkdirSync(out, { recursive: true });

const browser = await chromium.launch({ channel: 'chrome' });
const page = await browser.newPage({ viewport: { width: 1540, height: 1000 } });
await page.goto(deck);
await page.evaluate(() => document.fonts.ready);
const { variants, states } = await page.evaluate(() => window.DECK);

let overflow = 0;
for (const v of variants) {
	for (const s of states) {
		await page.click(`[data-variant="${v}"]`);
		await page.click(`[data-set="${s}"]`);
		await page.waitForTimeout(700);
		const wide = await page.$eval('#screen-phone', (el) => el.scrollWidth > el.clientWidth);
		if (wide) {
			overflow++;
			console.error(`overflow: ${v}/${s}`);
		}
		await page.locator('#stage').screenshot({ path: join(out, `${v}-${s}.png`) });
		console.log(`${v}-${s}.png`);
	}
}
await browser.close();
process.exit(overflow ? 1 : 0);
