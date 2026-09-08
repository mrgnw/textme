<script lang="ts">
	import { page } from "$app/state";
	import * as Tabs from "$lib/components/ui/tabs";
	import { Button } from "$lib/components/ui/button";
	import X from "@lucide/svelte/icons/x";
	import { renderSVG } from "uqr";
	import { parse } from "svelte-tel-input/utils";
	import { links, shareUrl } from "$lib/phone";

	interface Props {
		e164: string;
		onclose: () => void;
	}

	let { e164, onclose }: Props = $props();

	let tab = $state("telegram");

	let value = $derived(
		tab === "telegram" ? links(e164).telegram : shareUrl(page.url.origin, e164)
	);
	let svg = $derived(renderSVG(value, { pixelSize: 4 }));
	let formatted = $derived(parse(e164).formatInternational);
</script>

<div class="flex items-center justify-between">
	<span class="text-xs font-semibold uppercase tracking-wider text-muted-foreground">QR code</span>
	<Button
		variant="ghost"
		size="icon"
		class="h-8 w-8 rounded-full"
		onclick={onclose}
		aria-label="Back to number"
	>
		<X class="h-4 w-4" />
	</Button>
</div>

<Tabs.Root bind:value={tab}>
	<Tabs.List class="w-full">
		<Tabs.Trigger value="telegram" class="flex-1">Telegram</Tabs.Trigger>
		<Tabs.Trigger value="link" class="flex-1">textme link</Tabs.Trigger>
	</Tabs.List>
</Tabs.Root>

<div
	role="img"
	aria-label="QR code"
	class="mx-auto h-52 w-52 rounded-lg border bg-white p-3 text-black [&>svg]:h-full [&>svg]:w-full"
>
	{@html svg}
</div>

<p class="text-center text-sm text-muted-foreground">
	{#if tab === "telegram"}
		Scan to open <b class="font-medium text-foreground">{formatted}</b> in Telegram
	{:else}
		Scan to open this number on textme
	{/if}
</p>
