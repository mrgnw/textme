<script>
	import { page } from '$app/stores';
	import PhoneLinksCard from "$components/PhoneLinksCard.svelte";

	let initialValue = $page.params.slug;
</script>

<PhoneLinksCard {initialValue} />
