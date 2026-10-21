// Real offline proof: boot a preview server, let the service worker install,
// KILL the server, then reload and generate a link with no network at all.
// Playwright's `setOffline` does not apply to service-worker fetches, so the
// only honest test is to take the origin away. Group-kills the server so no
// vite preview is ever left orphaned.
import { spawn } from "node:child_process";
import { chromium } from "@playwright/test";

const PORT = 4327;
const url = `http://localhost:${PORT}/`;

const server = spawn("./node_modules/.bin/vite", ["preview", "--port", String(PORT), "--strictPort"], {
	stdio: "ignore",
	detached: true,
});

const killServer = () => {
	try {
		process.kill(-server.pid, "SIGTERM");
	} catch {}
};

try {
	let up = false;
	for (let i = 0; i < 60 && !up; i++) {
		try {
			await fetch(url);
			up = true;
		} catch {
			await new Promise((r) => setTimeout(r, 500));
		}
	}
	if (!up) throw new Error("preview server never came up");

	const browser = await chromium.launch();
	const page = await browser.newPage();
	await page.goto(url);
	await page.waitForFunction(async () => {
		const reg = await navigator.serviceWorker.ready;
		return reg.active?.state === "activated";
	});

	killServer();
	await new Promise((r) => setTimeout(r, 1000));

	await page.reload();
	const input = page.locator('input[type="tel"]');
	await input.waitFor({ state: "visible", timeout: 5000 });
	await input.pressSequentially("2024561111", { delay: 15 });
	const href = await page.getByRole("link", { name: "WhatsApp" }).getAttribute("href");
	if (!href || !href.includes("+12024561111")) {
		throw new Error(`offline link generation failed: ${href}`);
	}
	console.log("OFFLINE OK:", href);
	await browser.close();
} finally {
	killServer();
}
