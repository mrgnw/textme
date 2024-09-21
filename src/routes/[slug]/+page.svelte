<script>
	import { page } from '$app/stores';
	import Normalizer from "../Normalizer.svelte";
	
	let value = $state($page.params.slug);
	
</script>

<title># to t.me/wa.me</title>

<Normalizer data={$page.data} value={value} />

