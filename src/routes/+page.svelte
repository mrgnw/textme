<script>
	import { page } from '$app/stores'
	import Normalizer from "./Normalizer.svelte";
	let value = $state($page.params.slug);
	let data = $state($page.data);
	
</script>
<title># to t.me/wa.me</title>

<Normalizer data value />