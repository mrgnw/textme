import { test } from "node:test";
import assert from "node:assert/strict";
import { classify, findContacts, isListPaste, links, resolveInitial, shareUrl } from "./phone.ts";

test("classify walks empty → incomplete → valid while typing a Spanish mobile", () => {
	assert.equal(classify("", "ES").state, "empty");
	assert.equal(classify("6", "ES").state, "incomplete");
	assert.equal(classify("612 34 56", "ES").state, "incomplete");
	const done = classify("612 34 56 78", "ES");
	assert.equal(done.state, "valid");
	assert.equal(done.detail?.e164, "+34612345678");
	assert.equal(done.detail?.formatInternational, "+34 612 34 56 78");
});

test("classify reports invalid once the number is long enough but wrong", () => {
	assert.equal(classify("612 34 56 78 9", "ES").state, "invalid");
	assert.equal(classify("123456789", "ES").state, "invalid");
});

test("an international number overrides the default country", () => {
	const us = classify("+1 202 456 1111", "ES");
	assert.equal(us.state, "valid");
	assert.equal(us.detail?.countryCode, "US");
});

test("links use E.164 for Telegram and SMS, digits for WhatsApp", () => {
	assert.deepEqual(links("+34612345678"), {
		telegram: "https://t.me/+34612345678",
		whatsapp: "https://wa.me/34612345678",
		sms: "sms:+34612345678",
	});
	assert.throws(() => links("34612345678"));
});

test("shareUrl appends an encoded name only when given", () => {
	assert.equal(shareUrl("https://textme.cc", "+34612345678"), "https://textme.cc/34612345678");
	assert.equal(shareUrl("https://textme.cc", "+34612345678", " Ana Belén "), "https://textme.cc/34612345678/Ana%20Bel%C3%A9n");
});

const PASTE = [
	"Maria 34612345678",
	"Luis 34698765432",
	"Ana B 34656781234",
	"",
	"Friends:",
	"Carlos 34634567890",
	"Elena 34678901234",
	"Pablo 655 123 456",
].join("\n");

test("findContacts parses the deck fixture with libphonenumber", () => {
	const found = findContacts(PASTE, "ES");
	assert.deepEqual(
		found.map((c) => c.name),
		["Maria", "Luis", "Ana B", "Carlos", "Elena", "Pablo"],
	);
	assert.deepEqual(
		found.map((c) => c.e164),
		["+34612345678", "+34698765432", "+34656781234", "+34634567890", "+34678901234", "+34655123456"],
	);
	assert.deepEqual(
		found.map((c) => c.inferred),
		[false, false, false, false, false, true],
	);
	assert.equal(found[0].formatInternational, "+34 612 34 56 78");
});

test("findContacts accepts name-after-number and international forms", () => {
	const found = findContacts("+1 (202) 456-1111 Sam\n0034 612 34 56 78 - Rita", "ES");
	assert.deepEqual(found.map((c) => [c.name, c.e164, c.inferred]), [
		["Sam", "+12024561111", false],
		["Rita", "+34612345678", false],
	]);
});

test("isListPaste needs at least two numbers", () => {
	assert.equal(isListPaste("612 34 56 78", "ES"), false);
	assert.equal(isListPaste(PASTE, "ES"), true);
});

test("resolveInitial parses national, digits-only international, and passes junk through", () => {
	assert.deepEqual(resolveInitial(null, "ES"), { value: "", country: "ES" });
	assert.deepEqual(resolveInitial("612345678", "ES"), { value: "+34612345678", country: "ES" });
	assert.deepEqual(resolveInitial("12024561111", "ES"), { value: "+12024561111", country: "US" });
	assert.deepEqual(resolveInitial("1", "ES"), { value: "1", country: "ES" });
});
