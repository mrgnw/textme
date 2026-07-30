import { test, expect, type Locator } from "@playwright/test";

const VALID_US_NUMBER = "+1 202 456 1111";
const VALID_US_DIGITS = "2024561111";
const EXPECTED_E164 = "+12024561111";

async function pasteInto(input: Locator, text: string) {
	await input.evaluate((el, value) => {
		const data = new DataTransfer();
		data.setData("text", value);
		el.dispatchEvent(
			new ClipboardEvent("paste", {
				clipboardData: data,
				bubbles: true,
				cancelable: true,
			}),
		);
	}, text);
}

function whatsappLink(page: import("@playwright/test").Page) {
	return page.getByRole("link", { name: "WhatsApp" });
}

test("pasting a valid number enables the action buttons", async ({ page }) => {
	await page.goto("/");
	const input = page.locator('input[type="tel"]');

	await expect(whatsappLink(page)).toHaveClass(/disabled/);

	await input.focus();
	await pasteInto(input, VALID_US_NUMBER);

	await expect(whatsappLink(page)).not.toHaveClass(/disabled/);
	await expect(whatsappLink(page)).toHaveAttribute(
		"href",
		`https://wa.me/${EXPECTED_E164}`,
	);
});

test("pasting digit-word forms is normalized and enables the buttons", async ({
	page,
}) => {
	await page.goto("/");
	const input = page.locator('input[type="tel"]');

	await input.focus();
	await pasteInto(input, "two zero two four five six one one one one");

	await expect(whatsappLink(page)).not.toHaveClass(/disabled/);
	await expect(whatsappLink(page)).toHaveAttribute(
		"href",
		`https://wa.me/${EXPECTED_E164}`,
	);
});

test("typing a valid number still enables the buttons", async ({ page }) => {
	await page.goto("/");
	const input = page.locator('input[type="tel"]');

	await input.pressSequentially(VALID_US_DIGITS, { delay: 15 });

	await expect(whatsappLink(page)).not.toHaveClass(/disabled/);
});

test("deep-linking to /{number} enables the buttons", async ({ page }) => {
	await page.goto(`/${VALID_US_DIGITS}`);

	await expect(whatsappLink(page)).not.toHaveClass(/disabled/);
});
