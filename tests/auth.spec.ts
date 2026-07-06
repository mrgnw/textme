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
