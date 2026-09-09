import { test } from "node:test";
import assert from "node:assert/strict";
import { replaceDigitWords } from "./normalize.js";

test("converts english and spanish digit words", () => {
	assert.equal(replaceDigitWords("SEIS-CERO-SIETE"), "6-0-7");
	assert.equal(replaceDigitWords("one two three"), "1 2 3");
});

test("converts circled digits", () => {
	assert.equal(replaceDigitWords("⑥①②❸"), "6123");
});
