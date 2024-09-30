import { getCloudflareData } from '$lib/cloudflare.js';

/** @type {import('./$types').PageServerLoad} */
export function load({ request, params }) {
	const cloudflareData = getCloudflareData(request);

	return {
		...cloudflareData,
		slug: params.slug
	};
}