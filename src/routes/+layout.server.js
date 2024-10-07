import { getCloudflareData } from '$lib/cloudflare.js';

export function load({ request, params }) {
    const cloudflareData = getCloudflareData(request);

    return {
        ...cloudflareData,
        slug: params.slug
    };
}
