import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ params }) => {
	const phone = params.phone;
	const e164 = phone.startsWith('+') ? phone : `+${phone}`;
	const clean = phone.replace(/\D/g, '');

	return json({
		phone: e164,
		links: {
			telegram: `https://t.me/${e164}`,
			whatsapp: `https://wa.me/${clean}`,
			sms: `sms:${e164}`
		}
	});
};
