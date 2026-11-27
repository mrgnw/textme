import { test } from "node:test";
import assert from "node:assert/strict";
import { OTHER_CARRIER, checkYourPhone, hasCarrierList, isValidCarrier, parseCarrierChoices, peopleSummary, phoneFromUserAgent, reachLevel, summaryLine, supportLevel, verdict } from "./rcs.ts";

/** @type {import("./rcs.ts").AndroidCoverage} */
const unknownAndroid = { status: "unknown", detail: null, date: null, source_url: null, confidence: null };
/** @type {import("./rcs.ts").IphoneCoverage} */
const unknownIphone = { status: "unknown", carriers: [], date: null, source_url: null, confidence: null };

/**
 * @param {string} iso2
 * @param {Partial<import("./rcs.ts").AndroidCoverage>} [android]
 * @param {Partial<import("./rcs.ts").IphoneCoverage>} [iphone]
 * @returns {import("./rcs.ts").CountryCoverage}
 */
function row(iso2, android = {}, iphone = {}) {
	return {
		iso2,
		n: "000",
		name: iso2,
		android: { ...unknownAndroid, ...android },
		iphone: { ...unknownIphone, ...iphone },
		ios_share: null,
		android_share: null,
		note: null
	};
}

const us = row("US", { status: "live" }, { status: "listed", carriers: ["AT&T", "T-Mobile USA", "Verizon Wireless"] });
const mx = row("MX", { status: "live" }, { status: "none_listed" });
const cn = row("CN", {}, { status: "listed", carriers: ["China Mobile"] });
const it = row("IT", { status: "none_listed" }, { status: "none_listed" });
const zz = row("ZZ");

test("support level follows the phone type", () => {
	assert.equal(supportLevel(mx, "android"), "yes");
	assert.equal(supportLevel(mx, "iphone"), "none");
	assert.equal(supportLevel(zz, "android"), "unknown");
	assert.equal(supportLevel(row("PL", { status: "partial" }), "android"), "partial");
});

test("verdict stays short and never lists carriers", () => {
	assert.deepEqual(verdict(us).map((line) => `${line.pair}: ${line.text}`), [
		"Android to Android: Works",
		"iPhone to Android: Works on listed carriers"
	]);
	assert.ok(verdict(us).every((line) => !line.text.includes("Verizon")));
});

test("a chosen carrier answers for that carrier only", () => {
	const listed = verdict(us, "Verizon Wireless")[1];
	assert.equal(listed.text, "Verizon Wireless: listed by Apple");
	assert.equal(listed.level, "yes");
	const other = verdict(us, OTHER_CARRIER)[1];
	assert.equal(other.text, "Your carrier is not on Apple's list here");
	assert.equal(other.level, "none");
	assert.equal(verdict(us, "Not A Carrier")[1].text, "Works on listed carriers");
});

test("verdict keeps unknown as unknown and none_listed as not on Apple's list", () => {
	assert.deepEqual(verdict(zz).map((line) => line.level), ["unknown", "unknown"]);
	assert.equal(verdict(zz)[1].text, "No data yet");
	assert.equal(verdict(mx)[1].text, "Not on Apple's list");
	assert.equal(verdict(mx)[1].level, "none");
	assert.equal(verdict(mx, OTHER_CARRIER)[1].text, "Not on Apple's list");
});

test("iPhone listed with unconfirmed Android is partial, not yes", () => {
	assert.equal(verdict(cn)[1].level, "partial");
	assert.equal(verdict(cn, "China Mobile")[1].text, "China Mobile: listed by Apple");
	assert.equal(verdict(cn, "China Mobile")[1].level, "partial");
});

test("carrier choices are only valid for countries with a carrier list", () => {
	assert.equal(hasCarrierList(us), true);
	assert.equal(hasCarrierList(mx), false);
	assert.equal(isValidCarrier(us, "AT&T"), true);
	assert.equal(isValidCarrier(us, OTHER_CARRIER), true);
	assert.equal(isValidCarrier(us, "Telcel"), false);
	assert.equal(isValidCarrier(mx, OTHER_CARRIER), false);
	assert.equal(isValidCarrier(undefined, "AT&T"), false);
	assert.equal(isValidCarrier(us, 3), false);
});

test("stored carrier choices drop anything that no longer matches the data", () => {
	const rows = new Map([us, mx, cn].map((r) => [r.iso2, r]));
	assert.deepEqual(parseCarrierChoices({ US: "AT&T", MX: "Telcel", CN: "Nope", XX: "AT&T", ES: 4 }, rows), { US: "AT&T" });
	assert.deepEqual(parseCarrierChoices(null, rows), {});
	assert.deepEqual(parseCarrierChoices(["US"], rows), {});
	assert.deepEqual(parseCarrierChoices("AT&T", rows), {});
});

test("reach is yes when either phone type has RCS", () => {
	assert.equal(reachLevel(us), "yes");
	assert.equal(reachLevel(cn), "yes");
	assert.equal(reachLevel(it), "none");
	assert.equal(reachLevel(zz), "unknown");
	assert.equal(reachLevel(row("FI", { status: "none_listed" })), "unknown");
});

test("people summary counts only known statuses", () => {
	const summary = peopleSummary([us, mx, it, zz, zz]);
	assert.deepEqual(summary, { total: 5, known: 3, reach: 2, unknown: 2 });
	assert.equal(summaryLine(summary), "RCS support is listed in 2 of 3 countries with data. No data yet for 2 countries.");
});

test("summary line handles empty, all unknown and singular cases", () => {
	assert.equal(summaryLine(peopleSummary([])), "");
	assert.equal(summaryLine(peopleSummary([zz])), "No RCS data yet for your 1 country.");
	assert.equal(summaryLine(peopleSummary([us])), "RCS support is listed in 1 of 1 country with data.");
});

test("user agent picks iPhone only for iOS devices", () => {
	assert.equal(phoneFromUserAgent("Mozilla/5.0 (iPhone; CPU iPhone OS 26_1 like Mac OS X)"), "iphone");
	assert.equal(phoneFromUserAgent("Mozilla/5.0 (Linux; Android 16; Pixel 10)"), "android");
	assert.equal(phoneFromUserAgent("Mozilla/5.0 (Macintosh; Intel Mac OS X 15_0)"), "android");
});

/** @type {import("./rcs.ts").Requirements} */
const requirements = {
	ios_min: { value: "18", requirement_text: null, note: null, date: "2026-05-11", source_url: "https://support.apple.com/en-us/122195", confidence: "vendor-claim" },
	iphone_models: { value: null, requirement_text: null, note: "Apple lists iPhone XS, XS Max, XR, and SE (2nd generation or later) among compatible models.", date: null, source_url: null, confidence: "vendor-claim" },
	android_google_play_services_floor: { value: "7.0", requirement_text: null, note: null, date: null, source_url: "https://support.google.com/googleplay/answer/9037938", confidence: "vendor-claim" },
	android_google_messages_setup: { value: null, requirement_text: null, note: null, date: null, source_url: null, confidence: "vendor-claim" },
	iphone_excluded: { major_version: 18, excluded_models: ["iPhone 7", "iPhone SE (1st generation)", "iPhone 8", "iPhone 8 Plus", "iPhone X"], date: "2026-05-27", source_url: "https://support.apple.com/en-is/104985", confidence: "vendor-claim" }
};

test("check your phone quotes the minimum versions from the data", () => {
	assert.match(checkYourPhone("iphone", requirements).text, /^You need iOS 18 or newer .*XS, XS Max, XR.* iPhone X, iPhone 8 Plus, and iPhone 8 and older models cannot run iOS 18\.$/);
	assert.match(checkYourPhone("android", requirements).text, /^You need Android 7 or newer/);
	assert.equal(checkYourPhone("iphone", requirements).summary, "iOS 18 or newer");
	assert.equal(checkYourPhone("android", requirements).summary, "Android 7 or newer");
});
