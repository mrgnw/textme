<script lang="ts">
	import type { CountryCode } from "svelte-tel-input/types";
	import type { FoundContact } from "$lib/phone";
	import { findContacts } from "$lib/phone";
	import { Button } from "$lib/components/ui/button";
	import { Textarea } from "$lib/components/ui/textarea";
	import { Card } from "$lib/components/ui/card";
	import { copyToClipboard, downloadVCards } from "$lib/utils";
	import { TextareaAutosize } from "runed";
	import ContactRow from "./ContactRow.svelte";
	import CountryStamp from "./CountryStamp.svelte";
	import ContactRound from "@lucide/svelte/icons/contact-round";
	import Copy from "@lucide/svelte/icons/copy";

	let {
		text = $bindable(),
		country = $bindable(),
		countryLabel,
		onclear,
	}: {
		text: string;
		country: CountryCode | null;
		countryLabel: string;
		onclear: () => void;
	} = $props();

	let ref = $state<HTMLTextAreaElement | null>(null);
	new TextareaAutosize({ element: () => ref ?? undefined, input: () => text });

	let names = $state<Record<string, string>>({});

	let contacts = $derived(findContacts(text, country));
	let inferredCount = $derived(contacts.filter((c) => c.inferred).length);

	function nameOf(contact: FoundContact) {
		return names[contact.e164] ?? contact.name;
	}

	function downloadAll() {
		downloadVCards(contacts.map((c) => ({ phone: c.e164, name: nameOf(c) })));
	}

	function copyAll() {
		copyToClipboard(contacts.map((c) => c.e164).join("\n"));
	}
</script>

<Card class="rounded-2xl">
	<div class="space-y-4 p-6">
		<div class="flex items-center justify-between">
			<span class="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
				Pasted list
			</span>
			<CountryStamp bind:country />
		</div>
		<Textarea bind:ref bind:value={text} class="h-auto resize-none font-mono leading-6" />
		<div class="flex items-center gap-2">
			{#if contacts.length === 0}
				<span class="font-display text-lg font-semibold">No numbers found yet</span>
			{:else}
				<span class="font-display text-lg font-semibold">
					{contacts.length} contact{contacts.length === 1 ? "" : "s"}
				</span>
				{#if inferredCount > 0}
					<span class="text-sm text-muted-foreground">· {inferredCount} got {countryLabel}</span>
				{/if}
			{/if}
			<Button variant="ghost" size="sm" class="ml-auto text-muted-foreground" onclick={onclear}>
				Clear
			</Button>
		</div>
		<div class="flex gap-2">
			<Button class="flex-1" onclick={downloadAll}>
				<ContactRound />
				Save all contacts
			</Button>
			<Button variant="outline" onclick={copyAll}>
				<Copy />
				Copy all
			</Button>
		</div>
	</div>
</Card>
{#if contacts.length > 0}
	<Card class="mt-4 divide-y">
		{#each contacts as contact (contact.e164)}
			<ContactRow
				{contact}
				{countryLabel}
				bind:name={() => nameOf(contact), (v) => (names[contact.e164] = v)}
			/>
		{/each}
	</Card>
{/if}
