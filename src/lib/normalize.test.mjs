import { test } from "node:test";
import assert from "node:assert/strict";
import { normalize } from "./normalize.js";

test("converts word digits to numeric digits", () => {
	assert.equal(normalize("SEIS-CERO-SIETE"), "+1607");
});

test("handles numbers with country code", () => {
	assert.equal(normalize("+54 9 11 1234 5678"), "+5491112345678");
});

test("defaults to country code 1 if none provided", () => {
	assert.equal(normalize("1234567890"), "+11234567890");
});
