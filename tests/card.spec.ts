import { test, expect } from "@playwright/test";
import { readFile } from "node:fs/promises";
import { pasteInto } from "./helpers";

const LIST = [
	"Maria 34612345678",
	"Luis 34698765432",
	"Ana B 34656781234",
	"",
	"Friends:",
	"Carlos 34634567890",
	"Elena 34678901234",
	"Pablo 655 123 456",
].join("\n");

test.use({ extraHTTPHeaders: { "cf-ipcountry": "ES" } });

test("an incomplete number shows no error; a wrong complete one does after blur", async ({ page }) => {
	await page.goto("/", { waitUntil: "networkidle" });
	const input = page.locator('input[type="tel"]');

	await input.pressSequentially("612 34 5", { delay: 15 });
	await expect(page.getByRole("alert")).toHaveCount(0);

	await input.fill("");
	await input.pressSequentially("123456789", { delay: 15 });
	await expect(page.getByRole("alert")).toHaveCount(0);
	await page.keyboard.press("Tab");
	await expect(page.getByRole("alert")).toContainText("Not a valid number");
});

test("the Paste button reads the clipboard", async ({ page, context }) => {
	await context.grantPermissions(["clipboard-read", "clipboard-write"]);
	await page.goto("/", { waitUntil: "networkidle" });
	await page.evaluate(() => navigator.clipboard.writeText("+1 202 456 1111"));

	await page.getByRole("button", { name: "Paste number" }).click();

	await expect(page.getByRole("link", { name: "WhatsApp" })).toHaveAttribute("href", "https://wa.me/12024561111");
});

test("the Paste button falls back to a hint when the clipboard is unavailable", async ({ page }) => {
	await page.addInitScript(() => {
		Object.defineProperty(navigator, "clipboard", {
			value: { readText: () => Promise.reject(new Error("denied")) },
		});
	});
	await page.goto("/", { waitUntil: "networkidle" });

	await page.getByRole("button", { name: "Paste number" }).click();

	await expect(page.getByText("Paste with")).toBeVisible();
	await expect(page.locator('input[type="tel"]')).toBeFocused();
});

test("a multi-number paste becomes the list editor", async ({ page }) => {
	await page.goto("/", { waitUntil: "networkidle" });
	await pasteInto(page.locator('input[type="tel"]'), LIST);

	await expect(page.getByText("6 contacts")).toBeVisible();
	await expect(page.getByText("+34 added")).toBeVisible();
	await expect(page.getByRole("link", { name: "WhatsApp" })).toHaveCount(6);

	const download = page.waitForEvent("download");
	await page.getByRole("button", { name: "Download all .vcf" }).click();
	const file = await (await download).path();
	const vcf = await readFile(file!, "utf8");
	expect(vcf.match(/BEGIN:VCARD/g)).toHaveLength(6);
	expect(vcf).toContain("FN:Pablo");
	expect(vcf).toContain("TEL;TYPE=CELL:+34655123456");

	await page.getByRole("button", { name: "Clear" }).click();
	await expect(page.getByRole("button", { name: "Paste number" })).toBeVisible();
});

test("/bulk opens the list editor directly", async ({ page }) => {
	await page.goto("/bulk");
	await expect(page.getByText("Pasted list")).toBeVisible();
});

test("a named link shows the contact card", async ({ page }) => {
	await page.goto("/34612345678/Maria");

	await expect(page.getByRole("heading", { name: "Maria" })).toBeVisible();
	await expect(page.getByRole("button", { name: "Save Maria" })).toBeVisible();
	await expect(page.getByRole("link", { name: "WhatsApp" })).toHaveAttribute("href", "https://wa.me/34612345678");
	await expect(page.getByRole("link", { name: "Make your own link" })).toBeVisible();
});

test("the share dialog builds the link and adds the name", async ({ page }) => {
	await page.goto("/34612345678");
	await page.getByRole("button", { name: "Share link" }).click();

	const dialog = page.getByRole("dialog");
	await expect(dialog).toBeVisible();
	const url = dialog.locator("input[readonly]");
	await expect(url).toHaveValue(/\/34612345678$/);

	await dialog.getByLabel("Name").fill("Maria");
	await expect(url).toHaveValue(/\/34612345678\/Maria$/);
});

test("the QR is rendered locally", async ({ page }) => {
	const external: string[] = [];
	await page.route("**/api.qrserver.com/**", (route) => {
		external.push(route.request().url());
		route.abort();
	});
	await page.goto("/34612345678");
	await page.getByRole("button", { name: "QR", exact: true }).click();
	await page.getByRole("button", { name: "WhatsApp QR code" }).click();

	await expect(page.locator("[aria-label='QR code'] svg").first()).toBeVisible();
	await expect(page.getByText("wa.me/34612345678")).toBeVisible();

	await page.getByRole("button", { name: "textme QR code" }).click();
	await expect(page.getByText(`${new URL(page.url()).host}/34612345678`)).toBeVisible();
	await expect(page.getByRole("button", { name: "WhatsApp QR code" })).toHaveAttribute("aria-pressed", "false");

	await page.getByRole("button", { name: "textme QR code" }).click();
	await expect(page.locator("[aria-label='QR code']")).toHaveCount(0);
	expect(external).toHaveLength(0);
});

test("the number row copies the number and its segment copies the textme link", async ({ page, context }) => {
	await context.grantPermissions(["clipboard-read", "clipboard-write"]);
	await page.goto("/34612345678");

	await page.getByRole("button", { name: "Copy +34 612 34 56 78" }).click();
	expect(await page.evaluate(() => navigator.clipboard.readText())).toBe("+34612345678");

	await page.getByRole("button", { name: "Copy textme link" }).click();
	expect(await page.evaluate(() => navigator.clipboard.readText())).toMatch(/\/34612345678$/);
});

test("the pill segment copies the app link", async ({ page, context }) => {
	await context.grantPermissions(["clipboard-read", "clipboard-write"]);
	await page.goto("/34612345678");
	await page.getByRole("button", { name: "Copy Telegram link" }).click();

	await expect(page.getByText("Copied t.me/+34612345678")).toBeVisible();
	expect(await page.evaluate(() => navigator.clipboard.readText())).toBe("https://t.me/+34612345678");
});

test("recent numbers are offered on the empty screen", async ({ page }) => {
	await page.addInitScript(() => {
		localStorage.setItem("textme:recent", JSON.stringify([{ e164: "+34698765432", name: "Luis", at: 1 }]));
	});
	await page.goto("/", { waitUntil: "networkidle" });

	await expect(page.getByText("Recent")).toBeVisible();
	await page.getByRole("button", { name: "+34 698 76 54 32" }).click();
	await expect(page.getByRole("link", { name: "WhatsApp" })).toHaveAttribute("href", "https://wa.me/34698765432");
});

test("the country picker changes the stamp and the default country", async ({ page }) => {
	await page.goto("/", { waitUntil: "networkidle" });
	await page.getByRole("button", { name: "Change country" }).click();

	const dialog = page.getByRole("dialog");
	await dialog.getByLabel("Search country or code").fill("portu");
	await dialog.getByRole("button", { name: /Portugal/ }).click();

	await expect(page.getByRole("button", { name: "Change country" })).toContainText("+351");
	await page.locator('input[type="tel"]').pressSequentially("912345678", { delay: 15 });
	await expect(page.getByRole("link", { name: "WhatsApp" })).toHaveAttribute("href", "https://wa.me/351912345678");
});

test("junk slugs are not phone pages", async ({ request }) => {
	expect((await request.get("/bulk/x")).status()).toBe(404);
	expect((await request.get("/api/x")).status()).toBe(404);
});

test.describe("dark mode", () => {
	test.use({ colorScheme: "dark" });

	test("follows the system preference", async ({ page }) => {
		await page.goto("/", { waitUntil: "networkidle" });
		await expect(page.locator("html")).toHaveClass(/dark/);
	});
});
