import { test } from "node:test";
import assert from "node:assert/strict";
import { peopleSummary, phoneFromUserAgent, reachLevel, summaryLine, supportLevel, verdict } from "./rcs.ts";

const unknownAndroid = { status: "unknown", detail: null, date: null, source_url: null, confidence: null };
const unknownIphone = { status: "unknown", carriers: [], date: null, source_url: null, confidence: null };

function row(iso2, android = {}, iphone = {}) {
	return {
		iso2,
		n: null,
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

test("verdict names the iPhone carriers when both sides are live", () => {
	assert.deepEqual(verdict(us).map((line) => `${line.pair}: ${line.text}`), [
		"Android to Android: yes.",
		"iPhone to Android: yes on AT&T, T-Mobile USA, and Verizon Wireless."
	]);
});

test("verdict keeps unknown as unknown and none_listed as not listed", () => {
	assert.deepEqual(verdict(zz).map((line) => line.level), ["unknown", "unknown"]);
	assert.equal(verdict(mx)[1].text, "Apple lists no carrier here.");
	assert.equal(verdict(mx)[1].level, "none");
});

test("iPhone listed with unconfirmed Android is partial, not yes", () => {
	const line = verdict(cn)[1];
	assert.equal(line.level, "partial");
	assert.match(line.text, /China Mobile/);
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
	assert.equal(summaryLine(summary), "RCS can reach people in 2 of 3 countries with data. No data yet for 2 countries.");
});

test("summary line handles empty, all unknown and singular cases", () => {
	assert.equal(summaryLine(peopleSummary([])), "");
	assert.equal(summaryLine(peopleSummary([zz])), "No RCS data yet for your 1 country.");
	assert.equal(summaryLine(peopleSummary([us])), "RCS can reach people in 1 of 1 country with data.");
});

test("user agent picks iPhone only for iOS devices", () => {
	assert.equal(phoneFromUserAgent("Mozilla/5.0 (iPhone; CPU iPhone OS 26_1 like Mac OS X)"), "iphone");
	assert.equal(phoneFromUserAgent("Mozilla/5.0 (Linux; Android 16; Pixel 10)"), "android");
	assert.equal(phoneFromUserAgent("Mozilla/5.0 (Macintosh; Intel Mac OS X 15_0)"), "android");
});
