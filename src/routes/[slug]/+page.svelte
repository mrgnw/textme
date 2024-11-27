<script>
	import { page } from '$app/stores';
	import PhoneLinksCard from "$components/PhoneLinksCard.svelte";
	import { replaceDigitWords } from '$lib/normalize.js';

	let initialValue = $state($page.params.slug);
	initialValue = replaceDigitWords(initialValue);

</script>

<PhoneLinksCard {initialValue} />
