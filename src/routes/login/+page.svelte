<script lang="ts">
	import { AuthFlow } from '@mrgnw/anahtar/components';
	import { goto, invalidateAll } from '$app/navigation';
	import { page } from '$app/state';

	const next = $derived.by(() => {
		const raw = page.url.searchParams.get('next') ?? '/';
		return raw.startsWith('/') && !raw.startsWith('//') ? raw : '/';
	});

	async function onSuccess() {
		await invalidateAll();
		await goto(next);
	}
</script>

<main class="mx-auto mt-[15vh] max-w-sm px-4">
	<h1 class="mb-6 text-center text-xl font-semibold">Sign in</h1>
	<AuthFlow {onSuccess} />
</main>
