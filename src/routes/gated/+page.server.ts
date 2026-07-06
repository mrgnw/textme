import type { PageServerLoad } from './$types';
import { requireUser } from '$lib/server/guard';

export const load: PageServerLoad = (event) => {
	return { user: requireUser(event) };
};
