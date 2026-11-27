import type { Phone } from "./rcs.ts";

export type MajorShare = [major: number, value: number];

export interface PlatformVersions {
	date: string;
	source_url: string;
	majors: MajorShare[];
	unclassified: number;
}

export interface PhoneEstimate {
	majors: MajorShare[];
	base: { value: number; date: string; source_url: string };
}

export interface CountryVersions {
	ios: PlatformVersions | null;
	android: PlatformVersions | null;
	estimate: { ios: PhoneEstimate | null; android: PhoneEstimate | null } | null;
}

export interface VersionRow {
	major_version: number | null;
	value: number;
}

export interface VersionBar {
	label: string;
	value: number;
	meets: boolean;
	phones: number | null;
}

export const MINIMUM: Record<Phone, number> = { iphone: 18, android: 7 };
export const THRESHOLD_CHOICES: Record<Phone, number[]> = { iphone: [17, 18, 26], android: [5, 7, 8] };
const SHARE_BINS = [95, 90, 80] as const;
const MAX_BARS = 6;

function round(value: number, places = 2): number {
	const factor = 10 ** places;
	return Math.round(value * factor) / factor;
}

export function collapseMajors(rows: VersionRow[]): { majors: MajorShare[]; unclassified: number } {
	const byMajor = new Map<number, number>();
	let unclassified = 0;
	for (const row of rows) {
		if (row.major_version === null) {
			unclassified += row.value;
			continue;
		}
		byMajor.set(row.major_version, (byMajor.get(row.major_version) ?? 0) + row.value);
	}
	const majors = [...byMajor].map(([major, value]): MajorShare => [major, round(value)]).sort((a, b) => b[0] - a[0]);
	return { majors, unclassified: round(unclassified) };
}

export function thresholdShare(versions: PlatformVersions | null, minimum: number): number | null {
	if (!versions || versions.majors.length === 0) return null;
	return round(versions.majors.filter(([major]) => major >= minimum).reduce((sum, [, value]) => sum + value, 0));
}

export function shareBin(share: number | null): string {
	if (share === null) return "unknown";
	const bin = SHARE_BINS.findIndex((floor) => share >= floor);
	return bin === -1 ? `bin${SHARE_BINS.length}` : `bin${bin}`;
}

export function binLabels(): { bin: string; label: string }[] {
	return [
		...SHARE_BINS.map((floor, index) => ({ bin: `bin${index}`, label: index === 0 ? `${floor}% or more` : `${floor} to ${SHARE_BINS[index - 1]}%` })),
		{ bin: `bin${SHARE_BINS.length}`, label: `Under ${SHARE_BINS.at(-1)}%` }
	];
}

function sumOf(entries: MajorShare[]): number {
	return entries.reduce((sum, [, value]) => sum + value, 0);
}

export function versionBars(versions: PlatformVersions, estimate: PhoneEstimate | null, phone: Phone, minimum: number): VersionBar[] {
	const name = phone === "iphone" ? "iOS" : "Android";
	const phonesFor = (majors: number[]) => {
		const matched = estimate?.majors.filter(([major]) => majors.includes(major)) ?? [];
		return matched.length > 0 ? sumOf(matched) : null;
	};
	const shown = versions.majors.slice(0, MAX_BARS);
	const rest = versions.majors.slice(MAX_BARS);
	const bars: VersionBar[] = shown.map(([major, value]) => ({
		label: `${name} ${major}`,
		value,
		meets: major >= minimum,
		phones: phonesFor([major])
	}));
	for (const meets of [true, false]) {
		const group = rest.filter(([major]) => major >= minimum === meets);
		if (group.length === 0) continue;
		const majors = group.map(([major]) => major);
		bars.push({
			label: `Other ${name} ${Math.min(...majors)} to ${Math.max(...majors)}`,
			value: round(sumOf(group)),
			meets,
			phones: phonesFor(majors)
		});
	}
	return bars;
}

export function formatPhones(count: number): string {
	if (count >= 1e9) return `${round(count / 1e9, 1)} billion`;
	if (count >= 1e6) return `${round(count / 1e6, 1)} million`;
	if (count >= 1e3) return `${Math.round(count / 1e3)} thousand`;
	return `${count}`;
}
