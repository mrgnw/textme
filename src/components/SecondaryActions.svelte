<script lang="ts">
	import ContactRoundIcon from "@lucide/svelte/icons/contact-round";
	import DownloadIcon from "@lucide/svelte/icons/download";
	import ShareIcon from "@lucide/svelte/icons/share";
	import { Button } from "$lib/components/ui/button";
	import { Input } from "$lib/components/ui/input";
	import { Label } from "$lib/components/ui/label";
	import { downloadVCard } from "$lib/utils";
	import { remember } from "$lib/recent.svelte";

	interface Props {
		e164: string | null;
		name: string;
		onshare: () => void;
	}

	let { e164, name = $bindable(""), onshare }: Props = $props();

	let saving = $state(false);
	const disabled = $derived(!e164);
	const off = "pointer-events-none opacity-50";

	function save() {
		if (!e164) return;
		downloadVCard(e164, name || "Contact");
		remember(e164, name);
		saving = false;
	}
</script>

{#if saving && e164}
	<div class="space-y-2 rounded-lg bg-muted p-3">
		<Label for="contact-name">Name <span class="font-normal text-muted-foreground">(optional)</span></Label>
		<form class="flex gap-2" onsubmit={(e) => { e.preventDefault(); save(); }}>
			<Input id="contact-name" bind:value={name} placeholder="Who is this?" autofocus />
			<Button type="submit" class="shrink-0"><DownloadIcon />Save .vcf</Button>
		</form>
	</div>
{/if}

<div class="grid grid-cols-2 gap-2 border-t pt-4">
	<Button
		variant="ghost"
		size="sm"
		class="{saving ? 'bg-accent text-accent-foreground' : 'text-muted-foreground'} {disabled ? off : ''}"
		aria-disabled={disabled}
		onclick={() => (saving = !saving)}
	>
		<ContactRoundIcon />
		{name ? `Save ${name}` : "Save contact"}
	</Button>
	<Button variant="ghost" size="sm" class="text-muted-foreground {disabled ? off : ''}" aria-disabled={disabled} onclick={onshare}>
		<ShareIcon />
		Share link
	</Button>
</div>
