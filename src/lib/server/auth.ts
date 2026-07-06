import { createAuth } from '@mrgnw/anahtar';
import { d1Adapter } from '@mrgnw/anahtar/d1';

type Env = App.Platform['env'];
type Auth = Awaited<ReturnType<typeof createAuth>>;

const OTP_CAPTURE_MAX = 32;
const capturedOtps = new Map<string, string>();

export function capturedOtp(email: string): string | null {
	return capturedOtps.get(email.toLowerCase()) ?? null;
}

let authPromise: Promise<Auth> | null = null;

export function getAuth(env: Env): Promise<Auth> {
	if (!authPromise) {
		authPromise = createAuth({
			db: d1Adapter(env.DB),
			rpName: 'textme',
			onSendOTP: async (email, code) => {
				if (env.OTP_TEST_HOOK === '1') {
					if (capturedOtps.size >= OTP_CAPTURE_MAX) capturedOtps.clear();
					capturedOtps.set(email.toLowerCase(), code);
				}
				await sendOtpEmail(env, email, code);
			}
		});
	}
	return authPromise;
}

async function sendOtpEmail(env: Env, email: string, code: string) {
	if (!env.RESEND_API_KEY) {
		console.log(`[otp] ${email}: ${code}`);
		return;
	}
	const res = await fetch('https://api.resend.com/emails', {
		method: 'POST',
		headers: {
			Authorization: `Bearer ${env.RESEND_API_KEY}`,
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			from: 'textme <auth@textme.cc>',
			to: [email],
			subject: `${code} is your textme sign-in code`,
			text: `Your textme sign-in code is ${code}. It expires in 30 minutes.`
		})
	});
	if (!res.ok) throw new Error('Could not send the sign-in code. Try again.');
}
