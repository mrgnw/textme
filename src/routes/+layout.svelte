<script>
	import "../app.css";
	import { Toaster } from "svelte-sonner";
	/** @type {{children?: import('svelte').Snippet}} */
	let { children } = $props();
</script>

{@render children?.()}
<Toaster position="bottom-center" richColors />
