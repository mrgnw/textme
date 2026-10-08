import { defineParams } from '@sveltejs/kit/params';
import { replaceDigitWords } from '#lib/normalize.js';

const matchPhone = (param: string) => {
	if (param.length > 40) return false;

	const digits = replaceDigitWords(param);

	return (/\d/).test(digits) && !(/[a-z]/i).test(digits);
};

export const params = defineParams({
	phone: (param) => (matchPhone(param) ? param : undefined)
});
