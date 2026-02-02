export function getFlag(iso2: string): string {
	if (!iso2 || iso2.length !== 2) return "🏳️";
	return iso2
		.toUpperCase()
		.split("")
		.map(char => String.fromCodePoint(0x1F1E6 - 65 + char.charCodeAt(0)))
		.join("");
}
