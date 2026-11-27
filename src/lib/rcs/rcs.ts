export type Phone = "android" | "iphone";
export type Level = "yes" | "partial" | "none" | "unknown";
export type Confidence = "measured" | "vendor-claim" | "estimate" | null;

export interface Sourced {
	date: string | null;
	source_url: string | null;
	confidence: Confidence;
}

export interface AndroidCoverage extends Sourced {
	status: "live" | "partial" | "none_listed" | "unknown";
	detail: string | null;
}

export interface IphoneCoverage extends Sourced {
	status: "listed" | "none_listed" | "unknown";
	carriers: string[];
}

export interface Share extends Sourced {
	value: number;
}

export interface Requirement extends Sourced {
	value: string | null;
	requirement_text: string | null;
	note: string | null;
}

export interface Requirements {
	ios_min: Requirement;
	iphone_models: Requirement;
	android_google_play_services_floor: Requirement;
	android_google_messages_setup: Requirement;
	iphone_excluded: Sourced & { major_version: number; excluded_models: string[] };
}

export interface SourcedLine {
	summary: string;
	text: string;
	source: Sourced | null;
}

export interface CountryCoverage {
	iso2: string;
	n: string;
	name: string;
	android: AndroidCoverage;
	iphone: IphoneCoverage;
	ios_share: Share | null;
	android_share: Share | null;
	note: string | null;
}

export interface VerdictLine {
	pair: string;
	level: Level;
	text: string;
}

export interface PeopleSummary {
	total: number;
	known: number;
	reach: number;
	unknown: number;
}

const ANDROID_LEVEL = { live: "yes", partial: "partial", none_listed: "none", unknown: "unknown" } as const;
const IPHONE_LEVEL = { listed: "yes", none_listed: "none", unknown: "unknown" } as const;

export const LEVEL_LABEL: Record<Phone, Record<Level, string>> = {
	android: { yes: "Live", partial: "On some providers", none: "Not listed", unknown: "No data yet" },
	iphone: { yes: "Carriers on Apple's list", partial: "Some carriers", none: "Not on Apple's list", unknown: "No data yet" }
};

export const HOW_TO: Record<Phone, { text: string; source_url: string }> = {
	android: {
		text: "Open Google Messages, tap your profile picture, then Messages settings, RCS chats, and turn on RCS.",
		source_url: "https://support.google.com/messages/answer/13508703"
	},
	iphone: {
		text: "Open Settings, Apps, Messages, then turn on RCS Messaging. Your carrier has to support it.",
		source_url: "https://support.apple.com/en-gb/122195"
	}
};

const list = new Intl.ListFormat("en", { type: "conjunction" });

export function phoneFromUserAgent(userAgent: string): Phone {
	return /iPhone|iPad|iPod/.test(userAgent) ? "iphone" : "android";
}

export function supportLevel(row: CountryCoverage, phone: Phone): Level {
	return phone === "android" ? ANDROID_LEVEL[row.android.status] : IPHONE_LEVEL[row.iphone.status];
}

export function reachLevel(row: CountryCoverage): Level {
	const android = supportLevel(row, "android");
	const iphone = supportLevel(row, "iphone");
	if (android === "yes" || iphone === "yes") return "yes";
	if (android === "partial") return "partial";
	if (android === "none" && iphone === "none") return "none";
	return "unknown";
}

export const OTHER_CARRIER = "other";

const ANDROID_SHORT: Record<Level, string> = {
	yes: "Works",
	partial: "On some providers",
	none: "No provider listed",
	unknown: "No data yet"
};

function androidToAndroid(row: CountryCoverage): VerdictLine {
	const level = supportLevel(row, "android");
	return { pair: "Android to Android", level, text: ANDROID_SHORT[level] };
}

export function hasCarrierList(row: CountryCoverage): boolean {
	return row.iphone.status === "listed" && row.iphone.carriers.length > 0;
}

export function isValidCarrier(row: CountryCoverage | undefined, choice: unknown): choice is string {
	if (!row || typeof choice !== "string" || !hasCarrierList(row)) return false;
	return choice === OTHER_CARRIER || row.iphone.carriers.includes(choice);
}

export function parseCarrierChoices(stored: unknown, rows: Map<string, CountryCoverage>): Record<string, string> {
	if (typeof stored !== "object" || stored === null || Array.isArray(stored)) return {};
	return Object.fromEntries(Object.entries(stored).filter(([iso2, choice]) => isValidCarrier(rows.get(iso2), choice)));
}

function iphoneToAndroid(row: CountryCoverage, carrier: string): VerdictLine {
	const pair = "iPhone to Android";
	const { status } = row.iphone;
	if (status === "unknown") return { pair, level: "unknown", text: "No data yet" };
	if (status === "none_listed") return { pair, level: "none", text: "Not on Apple's list" };
	if (carrier === OTHER_CARRIER) return { pair, level: "none", text: "Your carrier is not on Apple's list here" };
	const level: Level = supportLevel(row, "android") === "yes" ? "yes" : "partial";
	if (isValidCarrier(row, carrier)) return { pair, level, text: `${carrier}: listed by Apple` };
	return { pair, level, text: "Works on listed carriers" };
}

export function verdict(row: CountryCoverage, carrier = ""): VerdictLine[] {
	return [androidToAndroid(row), iphoneToAndroid(row, carrier)];
}

export function peopleSummary(rows: CountryCoverage[]): PeopleSummary {
	const levels = rows.map(reachLevel);
	const unknown = levels.filter((level) => level === "unknown").length;
	const reach = levels.filter((level) => level === "yes" || level === "partial").length;
	return { total: rows.length, known: rows.length - unknown, reach, unknown };
}

function countries(count: number): string {
	return count === 1 ? "1 country" : `${count} countries`;
}

export function summaryLine({ total, known, reach, unknown }: PeopleSummary): string {
	if (total === 0) return "";
	if (known === 0) return `No RCS data yet for your ${countries(total)}.`;
	const head = `RCS support is listed in ${reach} of ${countries(known)} with data.`;
	return unknown === 0 ? head : `${head} No data yet for ${countries(unknown)}.`;
}

function major(version: string | null): string {
	return (version ?? "").replace(/\.0$/, "");
}

export function checkYourPhone(phone: Phone, requirements: Requirements): SourcedLine {
	if (phone === "iphone") {
		const { ios_min, iphone_models, iphone_excluded } = requirements;
		const version = major(ios_min.value);
		const newestExcluded = list.format(iphone_excluded.excluded_models.slice(-3).reverse());
		return {
			summary: `iOS ${version} or newer`,
			text: `You need iOS ${version} or newer and a carrier on Apple's list. ${iphone_models.note} ${newestExcluded} and older models cannot run iOS ${version}.`,
			source: ios_min
		};
	}
	const floor = requirements.android_google_play_services_floor;
	return {
		summary: `Android ${major(floor.value)} or newer`,
		text: `You need Android ${major(floor.value)} or newer with Google Play services, and Google Messages as your default texting app.`,
		source: floor
	};
}
