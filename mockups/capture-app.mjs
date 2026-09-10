import { chromium } from '@playwright/test';
import { mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const base = process.env.BASE_URL || 'http://localhost:4326';
const out = join(dirname(fileURLToPath(import.meta.url)), 'stills', 'app');
mkdirSync(out, { recursive: true });

const LIST = 'Maria 34612345678\nLuis 34698765432\nAna B 34656781234\n\nFriends:\nCarlos 34634567890\nElena 34678901234\nPablo 655 123 456';

async function paste(page, text) {
	await page.locator('input[type="tel"]').evaluate((el, value) => {
		const data = new DataTransfer();
		data.setData('text', value);
		el.dispatchEvent(new ClipboardEvent('paste', { clipboardData: data, bubbles: true, cancelable: true }));
	}, text);
}

const STATES = {
	empty: async (page) => page.goto(`${base}/`),
	typing: async (page) => {
		await page.goto(`${base}/`);
		await page.locator('input[type="tel"]').pressSequentially('61234', { delay: 20 });
	},
	invalid: async (page) => {
		await page.goto(`${base}/`);
		await page.locator('input[type="tel"]').pressSequentially('123456789', { delay: 20 });
		await page.keyboard.press('Tab');
	},
	valid: async (page) => page.goto(`${base}/34612345678`),
	name: async (page) => {
		await page.goto(`${base}/34612345678`);
		await page.getByRole('button', { name: 'Save contact' }).click();
	},
	qr: async (page) => {
		await page.goto(`${base}/34612345678`);
		await page.getByRole('button', { name: 'QR', exact: true }).click();
		await page.getByRole('button', { name: 'WhatsApp QR code' }).click();
	},
	share: async (page) => {
		await page.goto(`${base}/34612345678`);
		await page.getByRole('button', { name: 'Share link' }).click();
	},
	country: async (page) => {
		await page.goto(`${base}/34612345678`);
		await page.getByRole('button', { name: 'Change country' }).click();
	},
	list: async (page) => {
		await page.goto(`${base}/`);
		await paste(page, LIST);
	},
	landing: async (page) => page.goto(`${base}/34612345678/Maria`),
};

const LANES = [
	{ id: 'phone', viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true },
	{ id: 'desk', viewport: { width: 1280, height: 800 } },
];

const browser = await chromium.launch({ channel: 'chrome' });
for (const scheme of ['light', 'dark']) {
	for (const lane of LANES) {
		const context = await browser.newContext({
			...lane,
			colorScheme: scheme,
			extraHTTPHeaders: { 'cf-ipcountry': 'ES' },
		});
		await context.addInitScript(() => {
			localStorage.setItem(
				'textme:recent',
				JSON.stringify([
					{ e164: '+12024561111', name: '', at: 1 },
					{ e164: '+34698765432', name: 'Luis', at: 2 },
				]),
			);
		});
		const page = await context.newPage();
		for (const [id, run] of Object.entries(STATES)) {
			await run(page);
			await page.waitForTimeout(700);
			await page.screenshot({ path: join(out, `${scheme}-${lane.id}-${id}.png`) });
			console.log(`${scheme}-${lane.id}-${id}.png`);
		}
		await context.close();
	}
}
await browser.close();
