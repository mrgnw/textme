import { PersistedState } from "runed";
import { phoneFromUserAgent, type CountryCoverage, type Phone, type Requirements } from "./rcs.js";
import type { CountryVersions } from "./versions.js";
import coverage from "./coverage.json";
import versionsUrl from "./versions.json?url";

const MAX_PEOPLE = 30;

export const rows = coverage.countries as CountryCoverage[];
export const asOf = coverage.as_of;
export const requirements = coverage.requirements as Requirements;
export const byIso = new Map(rows.map((row) => [row.iso2, row]));
export const minimum: Record<Phone, number> = {
	iphone: Number.parseInt(requirements.ios_min.value ?? "", 10),
	android: Number.parseInt(requirements.android_google_play_services_floor.value ?? "", 10)
};

interface VersionsFile {
	date: string;
	countries: Record<string, CountryVersions>;
}

class VersionStore {
	status = $state<"loading" | "ready" | "error">("loading");
	data = $state.raw<VersionsFile | null>(null);
}

export const versions = new VersionStore();

let versionsRequested = false;

export function loadVersions(): void {
	if (versionsRequested) return;
	versionsRequested = true;
	fetch(versionsUrl)
		.then((response) => {
			if (!response.ok) throw new Error(`versions: HTTP ${response.status}`);
			return response.json();
		})
		.then((data: VersionsFile) => {
			versions.data = data;
			versions.status = "ready";
		})
		.catch(() => (versions.status = "error"));
}

export function versionsOf(iso2: string): CountryVersions | null {
	return versions.data?.countries[iso2] ?? null;
}

const defaultPhone: Phone = typeof navigator === "undefined" ? "android" : phoneFromUserAgent(navigator.userAgent);

function parseStored(value: string): unknown {
	try {
		return JSON.parse(value);
	} catch {
		return null;
	}
}

export const phone = new PersistedState<Phone>("textme:rcs-phone", defaultPhone, {
	serializer: {
		serialize: JSON.stringify,
		deserialize: (value) => {
			const parsed = parseStored(value);
			return parsed === "android" || parsed === "iphone" ? parsed : defaultPhone;
		}
	}
});
export const people = new PersistedState<string[]>("textme:rcs-people", [], {
	serializer: {
		serialize: JSON.stringify,
		deserialize: (value) => {
			const parsed = parseStored(value);
			if (!Array.isArray(parsed)) return [];
			return [...new Set(parsed.filter((code): code is string => typeof code === "string" && byIso.has(code)))].slice(-MAX_PEOPLE);
		}
	}
});

export function hasPerson(iso2: string): boolean {
	return people.current.includes(iso2);
}

export function togglePerson(iso2: string): void {
	if (hasPerson(iso2)) {
		people.current = people.current.filter((code) => code !== iso2);
		return;
	}
	if (!byIso.has(iso2)) return;
	people.current = [...people.current, iso2].slice(-MAX_PEOPLE);
}
