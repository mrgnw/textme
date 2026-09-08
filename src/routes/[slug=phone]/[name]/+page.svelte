<script lang="ts">
	import { page } from "$app/state";
	import PhoneLinksCard from "$components/PhoneLinksCard.svelte";
	import { replaceDigitWords } from "$lib/normalize.js";
</script>

<PhoneLinksCard initialValue={replaceDigitWords(page.params.slug ?? "")} initialName={page.params.name ?? ""} />
