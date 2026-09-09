import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { cubicOut } from "svelte/easing";
import type { TransitionConfig } from "svelte/transition";
import { toast } from "svelte-sonner";
import { links } from "$lib/phone";

export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}

type FlyAndScaleParams = {
	y?: number;
	x?: number;
	start?: number;
	duration?: number;
};

export const flyAndScale = (
	node: Element,
	params: FlyAndScaleParams = { y: -8, x: 0, start: 0.95, duration: 150 }
): TransitionConfig => {
	const style = getComputedStyle(node);
	const transform = style.transform === "none" ? "" : style.transform;

	const scaleConversion = (
		valueA: number,
		scaleA: [number, number],
		scaleB: [number, number]
	) => {
		const [minA, maxA] = scaleA;
		const [minB, maxB] = scaleB;

		const percentage = (valueA - minA) / (maxA - minA);
		const valueB = percentage * (maxB - minB) + minB;

		return valueB;
	};

	const styleToString = (
		style: Record<string, number | string | undefined>
	): string => {
		return Object.keys(style).reduce((str, key) => {
			if (style[key] === undefined) return str;
			return str + `${key}:${style[key]};`;
		}, "");
	};

	return {
		duration: params.duration ?? 200,
		delay: 0,
		css: (t) => {
			const y = scaleConversion(t, [0, 1], [params.y ?? 5, 0]);
			const x = scaleConversion(t, [0, 1], [params.x ?? 0, 0]);
			const scale = scaleConversion(t, [0, 1], [params.start ?? 0.95, 1]);

			return styleToString({
				transform: `${transform} translate3d(${x}px, ${y}px, 0) scale(${scale})`,
				opacity: t
			});
		},
		easing: cubicOut
	};
};

export function copyToClipboard(text: string, label = "to clipboard") {
	navigator.clipboard.writeText(text).then(() => {
		toast.success(`Copied ${label}`);
	}).catch(() => {
		toast.error("Failed to copy");
	});
}

export function notifyDownload(filename: string) {
	toast.success(`Downloaded ${filename}`);
}

export function generateVCard(phone: string, name?: string): string {
	const clean = phone.replace(/[^\d]/g, "");
	const formatted = clean.startsWith("+") ? clean : `+${clean}`;
	const displayName = name || "Contact";
	const hrefs = links(formatted);

	return [
		"BEGIN:VCARD",
		"VERSION:3.0",
		`FN:${displayName}`,
		`TEL;TYPE=CELL:${formatted}`,
		`X-SOCIALPROFILE;TYPE=whatsapp:${hrefs.whatsapp}`,
		`X-SOCIALPROFILE;TYPE=telegram:${hrefs.telegram}`,
		"END:VCARD",
	].join("\n");
}

function downloadText(filename: string, text: string, mime: string): void {
	const blob = new Blob([text], { type: mime });
	const url = window.URL.createObjectURL(blob);
	const a = document.createElement("a");
	a.href = url;
	a.download = filename;
	document.body.appendChild(a);
	a.click();
	document.body.removeChild(a);
	window.URL.revokeObjectURL(url);
	notifyDownload(filename);
}

export function downloadVCard(phone: string, name?: string): void {
	const vcard = generateVCard(phone, name);
	const safeName = (name || "contact")
		.replace(/[^a-z0-9]/gi, "_")
		.toLowerCase();
	downloadText(`${safeName}.vcf`, vcard, "text/vcard");
}

export function generateVCards(entries: { phone: string; name?: string }[]): string {
	return entries.map((entry) => generateVCard(entry.phone, entry.name)).join("\n");
}

export function downloadVCards(entries: { phone: string; name?: string }[]): void {
	downloadText("contacts.vcf", generateVCards(entries), "text/vcard");
}
