import type { Locator } from "@playwright/test";

export async function pasteInto(input: Locator, text: string) {
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
