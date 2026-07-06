import { chromium } from '@playwright/test';
import { mkdirSync } from 'node:fs';

const BASE = 'http://localhost:4319';
const OUT = 'static/auth-preview';
mkdirSync(OUT, { recursive: true });

const PHONE = { width: 390, height: 844 };
const DESKTOP = { width: 1100, height: 720 };

function email(tag) {
	return `${tag}-${Date.now()}@example.com`;
}

async function otpFor(ctx, addr) {
	const res = await ctx.request.get(`${BASE}/api/dev/otp?email=${encodeURIComponent(addr)}`);
	const { code } = await res.json();
	return code;
}

async function shot(page, name) {
	await page.waitForTimeout(400);
	await page.screenshot({ path: `${OUT}/${name}.png` });
	console.log(`captured ${name}`);
}

const browser = await chromium.launch();

// Phone lane — the auth flow, state by state.
{
	const ctx = await browser.newContext({ viewport: PHONE });
	const page = await ctx.newPage();

	await page.goto(`${BASE}/`);
	await shot(page, 'phone-1-home-signed-out');

	await page.goto(`${BASE}/login`);
	await page.locator('input.anahtar-input').waitFor();
	await shot(page, 'phone-2-login-email');

	const addr = email('preview');
	await page.locator('input.anahtar-input').fill(addr);
	await page.locator('button.anahtar-submit-icon').click();
	await page.locator('input.anahtar-otp-digit').first().waitFor();
	await shot(page, 'phone-3-login-otp');

	const code = await otpFor(ctx, addr);
	await page.locator('input.anahtar-otp-digit').first().fill(code);
	await page.locator('.anahtar-passkey-add').waitFor();
	await shot(page, 'phone-4-passkey-prompt');

	await page.locator('.anahtar-passkey-later').click();
	await page.locator('.anahtar-pill-email').waitFor();
	await page.goto(`${BASE}/gated`);
	await page.getByTestId('gated-user').waitFor();
	await shot(page, 'phone-5-gated-signed-in');

	await ctx.close();
}

// Desktop lane — pill placement signed-out and signed-in.
{
	const ctx = await browser.newContext({ viewport: DESKTOP });
	const page = await ctx.newPage();

	await page.goto(`${BASE}/`);
	await shot(page, 'desktop-1-home-signed-out');

	const addr = email('preview-d');
	await page.request.post(`${BASE}/api/auth/start`, { data: { email: addr } });
	const code = await otpFor(ctx, addr);
	await page.request.post(`${BASE}/api/auth/verify`, { data: { email: addr, code } });
	await page.goto(`${BASE}/gated`);
	await page.getByTestId('gated-user').waitFor();
	await shot(page, 'desktop-2-gated-signed-in');

	await ctx.close();
}

await browser.close();
console.log('done');
