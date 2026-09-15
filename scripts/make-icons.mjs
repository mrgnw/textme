import { chromium } from "@playwright/test";
import { writeFileSync } from "node:fs";

// Full-bleed coral tile with a white speech bubble + typing dots.
// Content sits inside the maskable safe zone (all points within radius ~151
// of centre; safe zone radius at 512px is ~205), so the same PNGs serve
// `purpose: any` and `purpose: maskable`.
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
	<rect width="512" height="512" fill="#f07142"/>
	<path d="M160 176h192a32 32 0 0 1 32 32v96a32 32 0 0 1-32 32h-96l-56 40v-40h-40a32 32 0 0 1-32-32v-96a32 32 0 0 1 32-32z" fill="#fff"/>
	<circle cx="208" cy="256" r="14" fill="#f07142"/>
	<circle cx="256" cy="256" r="14" fill="#f07142"/>
	<circle cx="304" cy="256" r="14" fill="#f07142"/>
</svg>`;

const targets = [
	["static/icon-192.png", 192],
	["static/icon-512.png", 512],
	["static/apple-touch-icon.png", 180],
	["static/favicon.png", 128],
];

const browser = await chromium.launch();
const page = await browser.newPage();
for (const [path, size] of targets) {
	await page.setViewportSize({ width: size, height: size });
	await page.setContent(
		`<body style="margin:0">${svg.replace("<svg ", `<svg width="${size}" height="${size}" `)}</body>`,
	);
	writeFileSync(path, await page.screenshot());
	console.log(path, `${size}x${size}`);
}
await browser.close();
