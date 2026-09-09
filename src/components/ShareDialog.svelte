<script lang="ts">
	import { page } from "$app/state";
	import { onMount } from "svelte";
	import * as Dialog from "$lib/components/ui/dialog";
	import Sheet from "$lib/components/ui/sheet/sheet.svelte";
	import { Button } from "$lib/components/ui/button";
	import { Input } from "$lib/components/ui/input";
	import { Label } from "$lib/components/ui/label";
	import Copy from "@lucide/svelte/icons/copy";
	import Share from "@lucide/svelte/icons/share";
	import { shareUrl } from "$lib/phone";
	import { copyToClipboard } from "$lib/utils";
	import { isMobile } from "$lib/media.svelte";

	interface Props {
		open?: boolean;
		e164: string;
		name?: string;
	}

	let { open = $bindable(false), e164, name = $bindable("") }: Props = $props();

	let url = $derived(shareUrl(page.url.origin, e164, name));
	let canShare = $state(false);

	onMount(() => {
		canShare = typeof navigator !== "undefined" && "share" in navigator;
	});
</script>

{#snippet content()}
	<p class="text-sm text-muted-foreground">
		Anyone with the link gets these buttons for this number.
	</p>
	<div class="space-y-1.5">
		<Label for="share-name">Name <span class="font-normal text-muted-foreground">(optional)</span></Label>
		<Input id="share-name" bind:value={name} placeholder="e.g. Maria" />
	</div>
	<div class="flex gap-2">
		<Input readonly value={url} class="font-mono" />
		<Button onclick={() => copyToClipboard(url)}><Copy />Copy</Button>
	</div>
	{#if canShare}
		<Button variant="outline" class="w-full" onclick={() => navigator.share({ url })}>
			<Share />Share…
		</Button>
	{/if}
{/snippet}

{#if isMobile.current}
	<Sheet bind:open title="Share link">
		<div class="space-y-4 px-4 pb-6">
			{@render content()}
		</div>
	</Sheet>
{:else}
	<Dialog.Root bind:open>
		<Dialog.Content>
			<Dialog.Header>
				<Dialog.Title>Share link</Dialog.Title>
			</Dialog.Header>
			<div class="space-y-4">
				{@render content()}
			</div>
		</Dialog.Content>
	</Dialog.Root>
{/if}
