import { error, json } from '@sveltejs/kit';
import type { RequestEvent } from '@sveltejs/kit';
import { capturedOtp } from '$lib/server/auth';

export function GET({ platform, url }: RequestEvent) {
	if (platform?.env?.OTP_TEST_HOOK !== '1') error(404, 'Not found');
	const code = capturedOtp(url.searchParams.get('email') ?? '');
	if (!code) error(404, 'No code captured');
	return json({ code });
}
