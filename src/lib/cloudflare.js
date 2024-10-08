import {countries} from '$lib/countries.js'

export function getCloudflareData(request) {
	const { headers } = request;
	const ip_country = headers.get('cf-ipcountry') || '';
	const accept_language = headers.get('accept-language');
	const country = ip_country
		? countries.find((c) => c.code === ip_country.toUpperCase())
		: null;
	const country_phone = country ? country.phone : null;

	return {
		ip_country,
		country_phone,
		accept_language
	};
}