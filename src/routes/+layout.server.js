export function load({ request }) {
	return {
		ip_country: request.headers.get('cf-ipcountry') || ''
	};
}
