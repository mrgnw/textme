<script>
	import { page } from '$app/stores'
	import Normalizer from "./Normalizer.svelte";
	export let data;
	export let value = $page.url.searchParams.get('n') || ''
</script>

<Normalizer data={data} value={value}>

</Normalizer>