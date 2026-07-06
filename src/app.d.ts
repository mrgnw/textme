import type { D1Database } from '@cloudflare/workers-types';

declare global {
	namespace App {
		interface Locals {
			user: { id: string; email: string } | null;
		}
		interface Platform {
			env: {
				DB: D1Database;
				OTP_TEST_HOOK?: string;
				RESEND_API_KEY?: string;
			};
		}
	}
}

export {};
