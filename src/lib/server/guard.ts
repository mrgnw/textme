import { redirect } from '@sveltejs/kit';

type GuardEvent = { locals: App.Locals; url: URL };

export function requireUser(event: GuardEvent): NonNullable<App.Locals['user']> {
	const { user } = event.locals;
	if (!user) {
		const next = encodeURIComponent(event.url.pathname + event.url.search);
		redirect(303, `/login?next=${next}`);
	}
	return user;
}
