<script lang="ts">
	import { page } from "$app/state";
	import * as Tabs from "$lib/components/ui/tabs";
	import { Button } from "$lib/components/ui/button";
	import CopyIcon from "@lucide/svelte/icons/copy";
	import { renderSVG } from "uqr";
	import { parse } from "svelte-tel-input/utils";
	import { links, shareUrl, type App } from "$lib/phone";
	import { copyToClipboard } from "$lib/utils";

	type Tab = App | "link";

	interface Props {
		e164: string;
		app: Tab;
	}

	let { e164, app }: Props = $props();

	// svelte-ignore state_referenced_locally
	let tab = $state<Tab>(app);

	const LABELS: Record<Tab, string> = { telegram: "Telegram", whatsapp: "WhatsApp", sms: "SMS", link: "textme" };

	let value = $derived(tab === "link" ? shareUrl(page.url.origin, e164) : links(e164)[tab]);
	let shown = $derived(value.replace(/^https:\/\//, ""));
	let svg = $derived(renderSVG(value, { pixelSize: 4 }));
	let formatted = $derived(parse(e164).formatInternational);
</script>

<Tabs.Root bind:value={tab}>
	<Tabs.List class="w-full">
		{#each Object.entries(LABELS) as [key, label] (key)}
			<Tabs.Trigger value={key} class="flex-1 px-2">{label}</Tabs.Trigger>
		{/each}
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
	{#if tab === "link"}
		Scan to open this number on textme
	{:else}
		Scan to open <b class="font-medium text-foreground">{formatted}</b> in {LABELS[tab]}
	{/if}
</p>

<Button variant="outline" size="sm" class="w-full" onclick={() => copyToClipboard(value, shown)}>
	<CopyIcon />
	<span class="truncate font-mono">{shown}</span>
</Button>
