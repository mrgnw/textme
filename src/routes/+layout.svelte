<script>
	import "../app.css";
	import { Toaster } from "svelte-sonner";
	import { AuthPill } from "@mrgnw/anahtar/components";
	import { invalidateAll } from "$app/navigation";
	import { page } from "$app/state";
	/** @type {{children?: import('svelte').Snippet}} */
	let { children } = $props();
	let user = $derived(page.data.user ?? null);

	async function signOut() {
		await fetch("/api/auth/logout", { method: "POST" });
		await invalidateAll();
	}
</script>

<div class="fixed right-3 top-3 z-50">
	<AuthPill {user} onSuccess={() => invalidateAll()} onSignOut={signOut} />
</div>
{@render children?.()}
<Toaster position="bottom-center" richColors />
