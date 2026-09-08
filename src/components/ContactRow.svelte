<script lang="ts">
	import type { FoundContact } from "$lib/phone";
	import { links } from "$lib/phone";
	import { Button } from "$lib/components/ui/button";
	import { Input } from "$lib/components/ui/input";
	import { copyToClipboard, downloadVCard } from "$lib/utils";
	import Copy from "@lucide/svelte/icons/copy";
	import ContactRound from "@lucide/svelte/icons/contact-round";
	import RiTelegramLine from "~icons/ri/telegram-line";
	import RiWhatsappLine from "~icons/ri/whatsapp-line";
	import RiChat3Line from "~icons/ri/chat-3-line";

	let {
		contact,
		name = $bindable(),
		countryLabel,
		editing = $bindable(false),
	}: {
		contact: FoundContact;
		name: string;
		countryLabel: string;
		editing?: boolean;
	} = $props();

	let linkSet = $derived(links(contact.e164));

	function commit() {
		editing = false;
	}
</script>

<div class="flex items-center gap-3 px-4 py-2.5">
	<div class="min-w-0 flex-1">
		{#if editing}
			<Input
				class="h-8 max-w-[11rem]"
				bind:value={name}
				autofocus
				aria-label="Name"
				onkeydown={(e: KeyboardEvent) => e.key === "Enter" && commit()}
				onblur={commit}
			/>
		{:else}
			<button
				type="button"
				class="block truncate text-sm font-medium"
				onclick={() => (editing = true)}
			>
				{name}
			</button>
		{/if}
		<div class="text-sm tabular-nums text-muted-foreground">
			{contact.formatInternational}
			{#if contact.inferred}
				<span class="mt-0.5 block w-max rounded-sm bg-primary/10 px-1.5 text-xs font-medium text-primary">
					{countryLabel} added
				</span>
			{/if}
		</div>
	</div>
	<div class="-mr-2 flex shrink-0">
		<Button
			variant="ghost"
			size="icon"
			class="h-9 w-9 text-muted-foreground"
			aria-label="Copy"
			onclick={() => copyToClipboard(contact.e164)}
		>
			<Copy />
		</Button>
		<Button
			variant="ghost"
			size="icon"
			class="h-9 w-9 text-telegram"
			aria-label="Telegram"
			href={linkSet.telegram}
			target="_blank"
		>
			<RiTelegramLine class="h-[18px] w-[18px]" />
		</Button>
		<Button
			variant="ghost"
			size="icon"
			class="h-9 w-9 text-whatsapp"
			aria-label="WhatsApp"
			href={linkSet.whatsapp}
			target="_blank"
		>
			<RiWhatsappLine class="h-[18px] w-[18px]" />
		</Button>
		<Button
			variant="ghost"
			size="icon"
			class="h-9 w-9 text-sms"
			aria-label="SMS"
			href={linkSet.sms}
		>
			<RiChat3Line class="h-[18px] w-[18px]" />
		</Button>
		<Button
			variant="ghost"
			size="icon"
			class="h-9 w-9 text-muted-foreground"
			aria-label="Save contact"
			onclick={() => downloadVCard(contact.e164, name)}
		>
			<ContactRound />
		</Button>
	</div>
</div>
