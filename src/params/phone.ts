import type { ParamMatcher } from "@sveltejs/kit";
import { replaceDigitWords } from "$lib/normalize.js";

export const match: ParamMatcher = (param) => {
	if (param.length > 40) return false;
	const digits = replaceDigitWords(param);
	return /\d/.test(digits) && !/[a-z]/i.test(digits);
};
