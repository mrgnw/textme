export interface ParsedContact {
	name: string;
	phone: string; // cleaned digits with country code prefix
	raw: string; // original line
}

/**
 * Parse bulk text input into contacts.
 * Handles formats like:
 *   Sophia 34638464842
 *   Anna A 34696872888
 *   Friends:
 *   Rita 34691521202
 *
 * Skips blank lines and lines that look like headers (ending with ":")
 */
export function parseBulkText(text: string): ParsedContact[] {
	const lines = text.split('\n');
	const contacts: ParsedContact[] = [];

	for (const raw of lines) {
		const trimmed = raw.trim();
		if (!trimmed) continue;

		// Skip header lines like "Friends:"
		if (/^[^0-9+]*:\s*$/.test(trimmed)) continue;

		const parsed = parseLine(trimmed);
		if (parsed) {
			contacts.push({ ...parsed, raw: trimmed });
		}
	}

	return contacts;
}

function parseLine(line: string): { name: string; phone: string } | null {
	// Strategy: find the phone number chunk (a sequence of digits, possibly
	// prefixed with +, possibly containing spaces/dashes within digits)
	// The rest is the name.

	// Try to find a phone-like sequence: optional + followed by digits,
	// possibly with spaces/dashes/dots between digit groups
	// We want at least 7 digits total to count as a phone number
	const phoneRegex = /(\+?\d[\d\s\-\.]{6,}\d)/;
	const match = line.match(phoneRegex);

	if (!match) return null;

	const phoneRaw = match[1];
	const phone = phoneRaw.replace(/[\s\-\.]/g, '');
	const phoneIndex = match.index!;

	// Everything that's not the phone number is the name
	const before = line.slice(0, phoneIndex).trim();
	const after = line.slice(phoneIndex + phoneRaw.length).trim();

	// Name could be before or after the number
	let name = before || after;
	// Clean trailing/leading separators
	name = name.replace(/^[\s\-:,]+|[\s\-:,]+$/g, '').trim();

	return { name, phone };
}
