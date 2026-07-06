import { getCloudflareData } from '$lib/cloudflare.js';

export function load({ request, params, locals }) {
    const cloudflareData = getCloudflareData(request);

    return {
        ...cloudflareData,
        slug: params.slug,
        user: locals.user
    };
}
