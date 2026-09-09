import { parse } from "svelte-tel-input/utils";
import type { CountryCode, DetailedValue } from "svelte-tel-input/types";
import { findPhoneNumbersInText, validatePhoneNumberLength } from "libphonenumber-js";

export type PhoneState = "empty" | "incomplete" | "invalid" | "valid";

export interface Classified {
	state: PhoneState;
	detail: DetailedValue | null;
}

export function classify(raw: string, country: CountryCode | null): Classified {
	if (!/\d/.test(raw)) return { state: "empty", detail: null };
	const detail = parse(raw, country);
	const length = validatePhoneNumberLength(raw, country ?? undefined);
	if (length === "TOO_SHORT") return { state: "incomplete", detail };
	if (length === undefined && detail.isValid) return { state: "valid", detail };
	return { state: "invalid", detail };
}

export function digitsOf(e164: string): string {
	if (!e164.startsWith("+")) throw new Error(`expected E.164, got ${e164}`);
	return e164.slice(1);
}

export function links(e164: string) {
	return {
		telegram: `https://t.me/${e164}`,
		whatsapp: `https://wa.me/${digitsOf(e164)}`,
		sms: `sms:${e164}`,
	};
}

export function shareUrl(origin: string, e164: string, name = ""): string {
	const trimmed = name.trim();
	const suffix = trimmed ? `/${encodeURIComponent(trimmed)}` : "";
	return `${origin}/${digitsOf(e164)}${suffix}`;
}

export interface FoundContact {
	name: string;
	e164: string;
	formatInternational: string;
	inferred: boolean;
}

// ponytail: 200 lines is far above any real paste; anything past it is dropped, not parsed
const MAX_LINES = 200;
const HEADER_LINE = /:\s*$/;
const EDGE_SEPARATORS = /^[\s\-:,]+|[\s\-:,]+$/g;

export function findContacts(text: string, country: CountryCode | null): FoundContact[] {
	const contacts: FoundContact[] = [];
	for (const line of text.split("\n").slice(0, MAX_LINES)) {
		const trimmed = line.trim();
		if (!trimmed || HEADER_LINE.test(trimmed)) continue;
		const [found] = findPhoneNumbersInText(trimmed, country ?? undefined);
		if (!found) continue;
		const raw = trimmed.slice(found.startsAt, found.endsAt);
		const rest = `${trimmed.slice(0, found.startsAt)} ${trimmed.slice(found.endsAt)}`;
		contacts.push({
			name: rest.replace(EDGE_SEPARATORS, "").trim(),
			e164: found.number.number as string,
			formatInternational: found.number.formatInternational(),
			inferred: raw.replace(/\D/g, "") === found.number.nationalNumber,
		});
	}
	return contacts;
}

export function isListPaste(text: string, country: CountryCode | null): boolean {
	return findContacts(text, country).length >= 2;
}
