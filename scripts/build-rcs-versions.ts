import { readFileSync, writeFileSync } from "node:fs";
import { collapseMajors, type CountryVersions, type PhoneEstimate, type PlatformVersions } from "../src/lib/rcs/versions.ts";

interface ShareRow {
	geo_id: string;
	geo_type: string;
	os: "ios" | "android";
	version: string;
	major_version: number | null;
	value: number;
	date: string;
	source_url: string;
}

interface EstimateRow {
	geo_id: string;
	os: "ios" | "android";
	version: string;
	estimated_phones: number;
	inputs: { smartphone_base: { value: number; date: string; source_url: string } };
}

const SOURCE = "research/rcs/devices-by-region.json";
const OUT = "src/lib/rcs/versions.json";

const research = JSON.parse(readFileSync(SOURCE, "utf8"));
const shares = (research.os_share as ShareRow[]).filter((row) => row.geo_type === "country");
const estimates = research.estimated_phones_by_version as EstimateRow[];

function groupBy<T>(rows: T[], key: (row: T) => string): Map<string, T[]> {
	const groups = new Map<string, T[]>();
	for (const row of rows) groups.set(key(row), [...(groups.get(key(row)) ?? []), row]);
	return groups;
}

const sharesBy = groupBy(shares, (row) => `${row.geo_id}:${row.os}`);
const majorOf = new Map(shares.map((row) => [`${row.geo_id}:${row.os}:${row.version}`, row.major_version]));
const estimatesBy = groupBy(estimates, (row) => `${row.geo_id}:${row.os}`);

function platform(iso2: string, os: "ios" | "android"): PlatformVersions | null {
	const rows = sharesBy.get(`${iso2}:${os}`);
	if (!rows) return null;
	return { date: rows[0].date, source_url: rows[0].source_url, ...collapseMajors(rows) };
}

function estimate(iso2: string, os: "ios" | "android"): PhoneEstimate | null {
	const rows = estimatesBy.get(`${iso2}:${os}`);
	if (!rows) return null;
	const collapsed = collapseMajors(
		rows.map((row) => ({ major_version: majorOf.get(`${iso2}:${os}:${row.version}`) ?? null, value: row.estimated_phones }))
	);
	const { value, date, source_url } = rows[0].inputs.smartphone_base;
	return { majors: collapsed.majors.map(([major, phones]) => [major, Math.round(phones)]), base: { value, date, source_url } };
}

const countries: Record<string, CountryVersions> = {};
for (const iso2 of new Set(shares.map((row) => row.geo_id))) {
	const hasEstimate = estimatesBy.has(`${iso2}:ios`) || estimatesBy.has(`${iso2}:android`);
	countries[iso2] = {
		ios: platform(iso2, "ios"),
		android: platform(iso2, "android"),
		estimate: hasEstimate ? { ios: estimate(iso2, "ios"), android: estimate(iso2, "android") } : null
	};
}

writeFileSync(OUT, `${JSON.stringify({ date: shares[0].date, countries })}\n`);
console.log(Object.keys(countries).length, "countries ->", OUT);
