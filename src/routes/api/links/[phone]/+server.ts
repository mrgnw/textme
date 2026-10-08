import type { RequestHandler } from './$types';
import { links } from '#lib/phone.js';

export const GET: RequestHandler = async ({ params }) => {
	const phone = params.phone;
	const e164 = phone.startsWith('+') ? phone : `+${phone}`;

	return Response.json({ phone: e164, links: links(e164) });
};
