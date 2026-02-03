import { redirect } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ params }) => {
	const phone = params.phone;
	const e164 = phone.startsWith('+') ? phone : `+${phone}`;
	throw redirect(302, `sms:${e164}`);
};
