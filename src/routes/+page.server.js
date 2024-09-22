import { getCloudflareData } from '$lib/cloudflare.js';

/** @type {import('./$types').PageServerLoad} */
export function load({ request }) {
	const cloudflareData = getCloudflareData(request);

	return {
		...cloudflareData
	};
}