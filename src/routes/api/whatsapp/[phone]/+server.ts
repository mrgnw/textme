import { redirect } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ params }) => {
	const phone = params.phone;
	const clean = phone.replace(/\D/g, '');
	throw redirect(302, `https://wa.me/${clean}`);
};
