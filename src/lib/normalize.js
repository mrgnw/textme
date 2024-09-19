// add function words-to-digits
function replaceDigitWords(phone) {
	// takes english or spanish words like 'one' or 'uno' and converts to '1'
	// example: SEIS-CERO-SIETEblah
	// returns: 6-0-7blah
	const wordToDigitMap = {
		'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
		'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
		'cero': '0', 'uno': '1', 'dos': '2', 'tres': '3', 'cuatro': '4',
		'cinco': '5', 'seis': '6', 'siete': '7', 'ocho': '8', 'nueve': '9',
	};

	return phone.replace(/([a-zA-Z]+)/g, word => {
		const lowerWord = word.toLowerCase();
		return wordToDigitMap.hasOwnProperty(lowerWord) ? wordToDigitMap[lowerWord] : word;
	});
}

export function normalize(phone, country_code = '1') {
	if (typeof phone !== 'string') {
		phone = String(phone);
	}
	phone = replaceDigitWords(phone);
	country_code = country_code.replace(/^0+/, '').replace(/[^0-9]/g, '');
	phone = phone.replace(/^0+/, '').replace(/[^0-9+]/g, '');
	let last10 = phone.slice(-10);
	// if (last10.length === 8) {
	// 	last10 = `11${last10}`;
	// }

	const prefix = phone.slice(0, -10).replace(/^\+/, '');
	const strippedPrefix = prefix;

	let result = '';

	if (strippedPrefix.match(/^\d+$/)) {
		result = `+${strippedPrefix}${last10}`;
	} else {
		result = `+${country_code}${last10}`;
	}
	return result;
}
