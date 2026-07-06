import { test, expect, type Page } from '@playwright/test';

function uniqueEmail(tag: string) {
	return `${tag}-${Date.now()}-${Math.floor(Math.random() * 1e6)}@example.com`;
}

async function otpFor(page: Page, email: string): Promise<string> {
	const res = await page.request.get(`/api/dev/otp?email=${encodeURIComponent(email)}`);
	expect(res.ok()).toBe(true);
	const { code } = await res.json();
	expect(code).toMatch(/^\d{5}$/);
	return code;
}

async function signInViaApi(page: Page, email: string) {
	const start = await page.request.post('/api/auth/start', { data: { email } });
	expect(start.ok()).toBe(true);
	const code = await otpFor(page, email);
	const verify = await page.request.post('/api/auth/verify', { data: { email, code } });
	expect(verify.ok()).toBe(true);
	return (await verify.json()) as { user: { id: string; email: string } };
}

test('email OTP round-trip creates a session', async ({ page }) => {
	const email = uniqueEmail('api');
	const body = await signInViaApi(page, email);
	expect(body.user.email).toBe(email);
});

test('gated route redirects to login when signed out', async ({ page }) => {
	await page.goto('/gated');
	await expect(page).toHaveURL('/login?next=%2Fgated');
});

test('gated route is accessible once signed in', async ({ page }) => {
	const email = uniqueEmail('guard');
	await signInViaApi(page, email);
	await page.goto('/gated');
	await expect(page.getByTestId('gated-user')).toHaveText(email);
});

test('signing in via the login page, then signing out', async ({ page }) => {
	const email = uniqueEmail('ui');
	await page.goto('/login?next=%2Fgated');

	await page.locator('input.anahtar-input').fill(email);
	await page.locator('button.anahtar-submit-icon').click();

	await expect(page.locator('input.anahtar-otp-digit').first()).toBeVisible();
	const code = await otpFor(page, email);
	await page.locator('input.anahtar-otp-digit').first().fill(code);

	await page.locator('.anahtar-passkey-later').click();
	await expect(page).toHaveURL('/gated');
	await expect(page.getByTestId('gated-user')).toHaveText(email);
	await expect(page.locator('.anahtar-pill-email')).toHaveText(email);

	await page.locator('button[title="Sign out"]').click();
	await expect(page.locator('input.anahtar-pill-email-input')).toBeVisible();
	await page.goto('/gated');
	await expect(page).toHaveURL('/login?next=%2Fgated');
});
