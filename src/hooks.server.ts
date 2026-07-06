import type { Handle } from '@sveltejs/kit';
import { getAuth } from '$lib/server/auth';

export const handle: Handle = async ({ event, resolve }) => {
	const auth = await getAuth(event.platform!.env);
	return auth.handle({ event, resolve });
};
