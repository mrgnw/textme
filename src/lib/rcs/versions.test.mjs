import { test } from "node:test";
import assert from "node:assert/strict";
import { binLabels, collapseMajors, formatPhones, formatShare, shareBin, thresholdShare, versionBars } from "./versions.ts";

/** @type {import("./versions.ts").PlatformVersions} */
const za = {
	date: "2026-10",
	source_url: "https://gs.statcounter.com",
	majors: [[27, 17.8], [26, 63.22], [18, 11.81], [17, 1.54], [16, 3.53], [15, 1.91], [14, 0.03], [12, 0.07]],
	unclassified: 0.08
};

test("collapse sums point releases into majors and keeps unknown labels apart", () => {
	const collapsed = collapseMajors([
		{ major_version: 26, value: 54.56 },
		{ major_version: 18, value: 10.36 },
		{ major_version: 26, value: 6.11 },
		{ major_version: null, value: 0.04 },
		{ major_version: 27, value: 10.64 },
		{ major_version: null, value: 0.23 }
	]);
	assert.deepEqual(collapsed, { majors: [[27, 10.64], [26, 60.67], [18, 10.36]], unclassified: 0.27 });
});

test("threshold share counts majors at or above the minimum, never unclassified", () => {
	assert.equal(thresholdShare(za, 18), 92.83);
	assert.equal(thresholdShare(za, 26), 81.02);
	assert.equal(thresholdShare(za, 17), 94.37);
});

test("no version data stays unknown, not zero", () => {
	assert.equal(thresholdShare(null, 18), null);
	assert.equal(thresholdShare({ ...za, majors: [] }, 18), null);
	assert.equal(shareBin(null), "unknown");
});

test("share bins split at 95, 90 and 80", () => {
	assert.equal(shareBin(97), "bin0");
	assert.equal(shareBin(95), "bin0");
	assert.equal(shareBin(92.8), "bin1");
	assert.equal(shareBin(85), "bin2");
	assert.equal(shareBin(40), "bin3");
	assert.deepEqual(binLabels().map((bin) => bin.label), ["95% or more", "90 to 95%", "80 to 90%", "Under 80%"]);
});

test("bars show the top majors and group the rest by whether they meet the minimum", () => {
	const bars = versionBars(za, null, "iphone", 18);
	assert.deepEqual(bars.map((bar) => [bar.label, bar.value, bar.meets]), [
		["iOS 27", 17.8, true],
		["iOS 26", 63.22, true],
		["iOS 18", 11.81, true],
		["iOS 17", 1.54, false],
		["iOS 16", 3.53, false],
		["iOS 15", 1.91, false],
		["iOS 12–14", 0.1, false]
	]);
	assert.ok(bars.every((bar) => bar.phones === null));
});

test("bars carry phone estimates only when the market has them", () => {
	/** @type {import("./versions.ts").PhoneEstimate} */
	const estimate = { majors: [[27, 1000], [26, 4000], [14, 5], [12, 7]], base: { value: 1, date: "2024", source_url: "https://ericsson.com" } };
	const bars = versionBars(za, estimate, "iphone", 18);
	assert.equal(bars[0].phones, 1000);
	assert.equal(bars[2].phones, null);
	assert.equal(bars.at(-1)?.phones, 12);
});

test("shares never round up to 100% or down to 0%", () => {
	assert.equal(formatShare(99.62), "over 99%");
	assert.equal(formatShare(100), "100%");
	assert.equal(formatShare(0.4), "under 1%");
	assert.equal(formatShare(92.83), "93%");
});

test("phone counts read in words", () => {
	assert.equal(formatPhones(120987425), "121 million");
	assert.equal(formatPhones(1710000000), "1.7 billion");
	assert.equal(formatPhones(45200), "45 thousand");
});
