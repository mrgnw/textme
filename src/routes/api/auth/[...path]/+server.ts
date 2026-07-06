import type { RequestEvent } from '@sveltejs/kit';
import { getAuth } from '$lib/server/auth';

export async function GET(event: RequestEvent) {
	const auth = await getAuth(event.platform!.env);
	return auth.handlers.GET(event);
}

export async function POST(event: RequestEvent) {
	const auth = await getAuth(event.platform!.env);
	return auth.handlers.POST(event);
}
