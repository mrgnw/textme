import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { toast } from "svelte-sonner";
import { links } from "$lib/phone";

export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}

export function copyToClipboard(text: string, label = "to clipboard") {
	navigator.clipboard.writeText(text).then(() => {
		toast.success(`Copied ${label}`);
	}).catch(() => {
		toast.error("Failed to copy");
	});
}

export function generateVCard(phone: string, name?: string): string {
	const formatted = `+${phone.replace(/\D/g, "")}`;
	const hrefs = links(formatted);

	return [
		"BEGIN:VCARD",
		"VERSION:3.0",
		`FN:${name || "Contact"}`,
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
	toast.success(`Downloaded ${filename}`);
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
