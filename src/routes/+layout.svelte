<script>
	import "../app.css";
	import "@fontsource-variable/bricolage-grotesque";
	import { ModeWatcher } from "mode-watcher";
	import { Toaster } from "svelte-sonner";
	/** @type {{children?: import('svelte').Snippet}} */
	let { children } = $props();
</script>

<ModeWatcher />
{@render children?.()}
<Toaster position="bottom-center" richColors />
