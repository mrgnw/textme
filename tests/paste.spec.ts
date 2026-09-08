import { test, expect } from "@playwright/test";
import { pasteInto } from "./helpers";

const VALID_US_NUMBER = "+1 202 456 1111";
const VALID_US_DIGITS = "2024561111";
const EXPECTED_DIGITS = "12024561111";

function whatsappLink(page: import("@playwright/test").Page) {
	return page.getByRole("link", { name: "WhatsApp" });
}

test("pasting a valid number enables the action buttons", async ({ page }) => {
	await page.goto("/", { waitUntil: "networkidle" });
	const input = page.locator('input[type="tel"]');

	await expect(whatsappLink(page)).toHaveCount(0);

	await input.focus();
	await pasteInto(input, VALID_US_NUMBER);

	await expect(whatsappLink(page)).not.toHaveAttribute("aria-disabled", "true");
	await expect(whatsappLink(page)).toHaveAttribute("href", `https://wa.me/${EXPECTED_DIGITS}`);
});

test("pasting digit-word forms is normalized and enables the buttons", async ({ page }) => {
	await page.goto("/");
	const input = page.locator('input[type="tel"]');

	await input.focus();
	await pasteInto(input, "two zero two four five six one one one one");

	await expect(whatsappLink(page)).not.toHaveAttribute("aria-disabled", "true");
	await expect(whatsappLink(page)).toHaveAttribute("href", `https://wa.me/${EXPECTED_DIGITS}`);
});

test("typing a valid number still enables the buttons", async ({ page }) => {
	await page.goto("/");
	const input = page.locator('input[type="tel"]');

	await input.pressSequentially(VALID_US_DIGITS, { delay: 15 });

	await expect(whatsappLink(page)).not.toHaveAttribute("aria-disabled", "true");
});

test("deep-linking to /{number} enables the buttons", async ({ page }) => {
	await page.goto(`/${VALID_US_DIGITS}`);

	await expect(whatsappLink(page)).not.toHaveAttribute("aria-disabled", "true");
});

test.describe("with a non-matching geo default country", () => {
	test.use({ extraHTTPHeaders: { "cf-ipcountry": "ES" } });

	test("pasting an international number overrides the geo country", async ({ page }) => {
		await page.goto("/", { waitUntil: "networkidle" });
		const input = page.locator('input[type="tel"]');

		await expect(page.getByRole("button", { name: "Change country" })).toContainText("🇪🇸");

		await input.focus();
		await pasteInto(input, VALID_US_NUMBER);

		await page.waitForURL(/\/12024561111$/);

		await expect(whatsappLink(page)).not.toHaveAttribute("aria-disabled", "true");
		await expect(whatsappLink(page)).toHaveAttribute("href", `https://wa.me/${EXPECTED_DIGITS}`);
	});
});
