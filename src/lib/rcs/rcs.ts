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
}

export interface OsVersion {
	ios_18_plus: Share | null;
	android_7_plus: Share | null;
}

export interface SourcedLine {
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
	os_version: OsVersion;
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

function androidToAndroid(row: CountryCoverage): VerdictLine {
	const level = supportLevel(row, "android");
	const text = { yes: "yes.", partial: "on some providers.", none: "no provider listed.", unknown: "no data yet." }[level];
	return { pair: "Android to Android", level, text };
}

function iphoneToAndroid(row: CountryCoverage): VerdictLine {
	const pair = "iPhone to Android";
	const android = supportLevel(row, "android");
	const { status, carriers } = row.iphone;
	if (status === "unknown") return { pair, level: "unknown", text: "no data yet." };
	if (status === "none_listed") return { pair, level: "none", text: "no carrier here is on Apple's list yet." };
	const on = carriers.length > 0 ? ` on ${list.format(carriers)}` : " on listed carriers";
	if (android === "yes") return { pair, level: "yes", text: `yes${on}.` };
	const androidSide = android === "partial" ? "Android RCS is confirmed on some providers." : "No data yet for Android here.";
	return { pair, level: "partial", text: `iPhone RCS is listed${on}. ${androidSide}` };
}

export function verdict(row: CountryCoverage): VerdictLine[] {
	return [androidToAndroid(row), iphoneToAndroid(row)];
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

function percentOf(value: number): string {
	return value >= 99.5 && value < 100 ? "Over 99%" : `${Math.round(value)}%`;
}

function major(version: string | null): string {
	return (version ?? "").replace(/\.0$/, "");
}

export function osVersionLine(row: CountryCoverage, phone: Phone, requirements: Requirements): SourcedLine {
	if (phone === "iphone") {
		const share = row.os_version.ios_18_plus;
		const version = `iOS ${major(requirements.ios_min.value)}`;
		if (!share) return { text: `No data yet on how many iPhones here run ${version} or newer.`, source: null };
		return { text: `${percentOf(share.value)} of sampled iPhone web traffic here comes from ${version} or newer.`, source: share };
	}
	const share = row.os_version.android_7_plus;
	const version = `Android ${major(requirements.android_google_play_services_floor.value)}`;
	if (!share) return { text: `No data yet on how many Android phones here run ${version} or newer.`, source: null };
	return { text: `${percentOf(share.value)} of sampled Android web traffic here comes from ${version} or newer.`, source: share };
}

export function checkYourPhone(phone: Phone, requirements: Requirements): SourcedLine {
	if (phone === "iphone") {
		const { ios_min, iphone_models } = requirements;
		const version = major(ios_min.value);
		return {
			text: `You need iOS ${version} or newer and a carrier on Apple's list. ${iphone_models.note} iPhone X, iPhone 8 and older models cannot run iOS ${version}.`,
			source: ios_min
		};
	}
	const floor = requirements.android_google_play_services_floor;
	return {
		text: `You need Android ${major(floor.value)} or newer with Google Play services, and Google Messages as your default texting app.`,
		source: floor
	};
}
