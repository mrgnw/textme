// export const prerender = false;

import {countries} from './countries.js'

export const load = async ({ request }) => {
	const { headers } = request;
	const ip_country = headers.get('cf-ipcountry');
	const accept_language = headers.get('accept_language');
	const country = countries.find((c) => c.code === ip_country);
	const country_phone = country ? country.phone : null;

	return {
		ip_country,
		country_phone,
		accept_language
	};
};