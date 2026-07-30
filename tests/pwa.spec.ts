import { test, expect } from "@playwright/test";

test("manifest is served with install-required fields", async ({ request }) => {
	const res = await request.get("/manifest.webmanifest");
	expect(res.ok()).toBe(true);
	const manifest = JSON.parse(await res.text());
	expect(manifest.name).toBe("textme");
	expect(manifest.display).toBe("standalone");
	expect(manifest.start_url).toBe("/");
	const sizes = manifest.icons.map((i: { sizes: string }) => i.sizes);
	expect(sizes).toContain("192x192");
	expect(sizes).toContain("512x512");
});

test("icons and apple-touch-icon are served as PNG", async ({ request }) => {
	for (const path of ["/icon-192.png", "/icon-512.png", "/apple-touch-icon.png"]) {
		const res = await request.get(path);
		expect(res.ok()).toBe(true);
		expect(res.headers()["content-type"]).toContain("image/png");
	}
});

test("page head links manifest, theme color, apple-touch-icon", async ({ page }) => {
	await page.goto("/");
	await expect(page.locator('link[rel="manifest"]')).toHaveAttribute(
		"href",
		/\/manifest\.webmanifest$/,
	);
	await expect(page.locator('meta[name="theme-color"]')).toHaveAttribute(
		"content",
		"#f07142",
	);
	await expect(page.locator('link[rel="apple-touch-icon"]')).toHaveAttribute(
		"href",
		/\/apple-touch-icon\.png$/,
	);
});

test("service worker activates and precaches the app shell", async ({ page }) => {
	await page.goto("/");
	await page.waitForFunction(async () => {
		const reg = await navigator.serviceWorker.ready;
		return reg.active?.state === "activated";
	});
	const cached = await page.evaluate(async () => {
		const keys = await caches.keys();
		const key = keys.find((k) => k.startsWith("textme-"));
		if (!key) return { hasShell: false, assetCount: 0 };
		const cache = await caches.open(key);
		const shell = await cache.match("/");
		const entries = await cache.keys();
		return { hasShell: Boolean(shell), assetCount: entries.length };
	});
	expect(cached.hasShell).toBe(true);
	expect(cached.assetCount).toBeGreaterThan(5);
});
