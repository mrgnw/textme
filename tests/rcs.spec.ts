import { test, expect, type Page } from "@playwright/test";

const VIEWPORTS = [
	{ name: "390", width: 390, height: 844 },
	{ name: "1280", width: 1280, height: 860 }
];

function watchErrors(page: Page): string[] {
	const errors: string[] = [];
	page.on("pageerror", (error) => errors.push(error.message));
	page.on("console", (message) => {
		if (message.type() === "error") errors.push(message.text());
	});
	return errors;
}

async function openGlobe(page: Page) {
	await page.goto("/rcs");
	await expect(page.locator('path[data-iso="ES"]')).toBeVisible();
}

test.describe("visitor in Spain", () => {
	test.use({ extraHTTPHeaders: { "cf-ipcountry": "ES" } });

	test("starts on the visitor's country with how-to and a centred globe", async ({ page }) => {
		const errors = watchErrors(page);
		await openGlobe(page);
		await expect(page.getByRole("heading", { level: 2, name: "Spain" })).toBeVisible();
		await expect(page.getByText("You are here")).toBeVisible();
		await expect(page.getByText("Turn RCS on.")).toBeVisible();
		const globe = await page.getByRole("application").boundingBox();
		const spain = await page.locator('path[data-iso="ES"]').boundingBox();
		expect(globe && spain).toBeTruthy();
		const dx = spain!.x + spain!.width / 2 - (globe!.x + globe!.width / 2);
		const dy = spain!.y + spain!.height / 2 - (globe!.y + globe!.height / 2);
		expect(Math.hypot(dx, dy)).toBeLessThan(globe!.width * 0.08);
		expect(errors).toEqual([]);
	});

	test("drag turns the globe and a tap selects a country", async ({ page }) => {
		await openGlobe(page);
		const spain = page.locator('path[data-iso="ES"]');
		const before = await spain.getAttribute("d");
		const box = (await page.getByRole("application").boundingBox())!;
		await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
		await page.mouse.down();
		await page.mouse.move(box.x + box.width / 2 + 80, box.y + box.height / 2 + 10, { steps: 6 });
		await page.mouse.up();
		expect(await spain.getAttribute("d")).not.toEqual(before);
		await page.locator('path[data-iso="DE"]').click({ force: true });
		await expect(page.getByRole("heading", { level: 2, name: "Germany" })).toBeVisible();
	});

	test("keyboard turns the globe and Enter picks the middle country", async ({ page }) => {
		await openGlobe(page);
		await page.getByRole("application").focus();
		for (let step = 0; step < 3; step++) await page.keyboard.press("ArrowRight");
		await expect(page.getByText("Middle: Türkiye")).toBeVisible();
		await page.keyboard.press("Enter");
		await expect(page.getByRole("heading", { level: 2, name: "Türkiye" })).toBeVisible();
		await page.getByRole("combobox", { name: "Country" }).selectOption("JP");
		await expect(page.getByRole("heading", { level: 2, name: "Japan" })).toBeVisible();
		await page.getByRole("button", { name: "Back to Spain" }).click();
		await expect(page.getByRole("heading", { level: 2, name: "Spain" })).toBeVisible();
	});

	test("flat map toggle and phone toggle", async ({ page }) => {
		await openGlobe(page);
		await page.getByText("Flat map").click();
		await expect(page.getByRole("application")).toHaveAttribute("aria-roledescription", "map");
		await page.getByText("iPhone", { exact: true }).click();
		await expect(page.getByText("Settings, Apps, Messages")).toBeVisible();
	});

	test("people list persists and summarises reach", async ({ page }) => {
		await openGlobe(page);
		await page.getByRole("button", { name: "I know people here" }).click();
		await page.getByRole("combobox", { name: "Country" }).selectOption("AQ");
		await page.getByRole("button", { name: "I know people here" }).click();
		await expect(page.getByText("RCS can reach people in 1 of 1 country with data. No data yet for 1 country.")).toBeVisible();
		await page.reload();
		await expect(page.getByRole("button", { name: "Remove Antarctica" })).toBeVisible();
	});

	for (const viewport of VIEWPORTS) {
		for (const scheme of ["light", "dark"] as const) {
			test(`capture ${viewport.name} ${scheme}`, async ({ page }) => {
				const errors = watchErrors(page);
				await page.setViewportSize(viewport);
				await page.emulateMedia({ colorScheme: scheme, reducedMotion: "reduce" });
				await openGlobe(page);
				await page.getByRole("button", { name: "I know people here" }).click();
				await page.getByRole("combobox", { name: "Country" }).selectOption("MX");
				await page.getByRole("button", { name: "I know people here" }).click();
				await page.getByRole("combobox", { name: "Country" }).selectOption("ES");
				await page.screenshot({ path: `captures/rcs-${viewport.name}-${scheme}.png`, fullPage: true });
				await page.getByText("Flat map").click();
				await expect(page.getByRole("application")).toHaveAttribute("aria-roledescription", "map");
				await page.waitForTimeout(300);
				await page.screenshot({ path: `captures/rcs-${viewport.name}-${scheme}-flat.png`, fullPage: true });
				expect(errors).toEqual([]);
			});
		}
	}
});

test.describe("visitor with unknown country", () => {
	test.use({ extraHTTPHeaders: { "cf-ipcountry": "XX" } });

	test("shows a neutral globe and asks for a country", async ({ page }) => {
		await openGlobe(page);
		await expect(page.getByText("We could not tell where you are.")).toBeVisible();
		await page.getByRole("combobox", { name: "Country" }).selectOption("BR");
		await expect(page.getByText("You are here")).toBeVisible();
		await page.screenshot({ path: "captures/rcs-unknown-country.png" });
	});
});

test("invalid stored preferences do not break the page", async ({ page }) => {
	await page.addInitScript(() => {
		localStorage.setItem("textme:rcs-phone", '"invalid"');
		localStorage.setItem("textme:rcs-people", '["ES","ES",null,"invalid"]');
	});
	await openGlobe(page);
	await expect(page.getByRole("button", { name: "Remove Spain" })).toHaveCount(1);
	await page.getByRole("button", { name: "Remove Spain" }).click();
	await expect(page.getByRole("button", { name: "Remove Spain" })).toHaveCount(0);
});
