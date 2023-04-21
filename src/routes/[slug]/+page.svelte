<script>
	import { page } from '$app/stores'
	import Normalizer from "../Normalizer.svelte";
	
	export let data;
	export let value = $page.params.slug;
</script>

<Normalizer data={data} value={value}>

</Normalizer>