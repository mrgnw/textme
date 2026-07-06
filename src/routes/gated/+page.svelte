<script lang="ts">
	let { data } = $props();
</script>

<main class="mx-auto mt-[15vh] max-w-sm px-4 text-center">
	<h1 class="text-xl font-semibold">Gated</h1>
	<p class="mt-2 text-sm text-gray-500">Signed in as</p>
	<p data-testid="gated-user">{data.user.email}</p>
</main>
