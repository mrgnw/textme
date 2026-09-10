<script lang="ts">
	import { page } from "$app/state";
	import RiTelegramLine from "~icons/ri/telegram-line";
	import RiWhatsappLine from "~icons/ri/whatsapp-line";
	import RiChat3Line from "~icons/ri/chat-3-line";
	import CheckIcon from "@lucide/svelte/icons/check";
	import CopyIcon from "@lucide/svelte/icons/copy";
	import PhoneIcon from "@lucide/svelte/icons/phone";
	import QrCodeIcon from "@lucide/svelte/icons/qr-code";
	import { parse } from "svelte-tel-input/utils";
	import { Popover } from "bits-ui";
	import { fly } from "svelte/transition";
	import { writeClipboard } from "$lib/utils";
	import { CHANNELS, CHANNEL_ORDER, channelUrl, shownUrl, type Channel } from "$lib/channels";

	interface Props {
		e164: string | null;
		showing?: Channel | null;
		onqr: (channel: Channel) => void;
	}

	let { e164, showing = null, onqr }: Props = $props();

	let mode = $state<"copy" | "qr">("copy");
	let copied = $state<{ segment: Channel | null; anchor: string; text: string } | null>(null);
	let copiedOpen = $state(false);
	let copiedTimer: ReturnType<typeof setTimeout> | undefined;

	const disabled = $derived(!e164);
	const formatted = $derived(e164 ? (parse(e164).formatInternational ?? e164) : "");

	const ICONS = { telegram: RiTelegramLine, whatsapp: RiWhatsappLine, sms: RiChat3Line } as const;

	const focus = "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-card";
	const main = "inline-flex h-12 min-w-0 flex-1 items-center justify-center gap-2 whitespace-nowrap pl-4 text-xl font-bold transition-colors hover:bg-black/10 sm:pl-14 [&_svg]:size-5";
	const seg = "inline-flex h-7 items-center gap-1.5 rounded-full px-2.5 transition-colors aria-pressed:bg-background aria-pressed:text-foreground aria-pressed:shadow-sm";

	function url(channel: Channel): string {
		return e164 ? channelUrl(page.url.origin, e164, channel) : "#";
	}

	function confirm(segment: Channel | null, anchor: string, text: string) {
		copied = { segment, anchor, text };
		copiedOpen = true;
		clearTimeout(copiedTimer);
		copiedTimer = setTimeout(() => (copiedOpen = false), 1500);
	}

	async function act(channel: Channel) {
		if (!e164) return;
		if (mode === "qr") {
			onqr(channel);
			return;
		}
		const value = url(channel);
		if (await writeClipboard(value)) confirm(channel, `[data-qr-segment="${channel}"]`, shownUrl(value));
	}

	async function copyNumber() {
		if (!e164) return;
		if (await writeClipboard(e164)) confirm(null, "[data-copy-number]", formatted);
	}
</script>

<div class="grid gap-3">
	{#each CHANNEL_ORDER as channel (channel)}
		{@const { label, fill, line } = CHANNELS[channel]}
		<div
			class="flex h-12 w-full overflow-hidden rounded-full {fill} {disabled ? 'pointer-events-none opacity-50' : ''}"
			data-qr-row={channel}
		>
			{#if channel === "link"}
				<button type="button" class="{main} text-lg tabular-nums max-[359px]:text-base sm:text-xl {focus}" aria-label="Copy {formatted}" data-copy-number {disabled} onclick={copyNumber}>
					<PhoneIcon class="max-[359px]:hidden" />
					{formatted}
				</button>
			{:else}
				{@const Icon = ICONS[channel]}
				<a
					href={url(channel)}
					target="_blank"
					class="{main} {focus}"
					aria-disabled={disabled}
					tabindex={disabled ? -1 : undefined}
				>
					<Icon />
					{label}
				</a>
			{/if}
			<button
				type="button"
				class="inline-flex h-12 w-14 items-center justify-center border-l {line} transition-colors hover:bg-black/10 {(copiedOpen && copied?.segment === channel) || (mode === 'qr' && showing === channel) ? 'bg-black/10' : ''} {focus}"
				aria-label={mode === "qr" ? `${label} QR code` : `Copy ${label} link`}
				aria-pressed={mode === "qr" ? showing === channel : undefined}
				data-qr-segment={channel}
				{disabled}
				onclick={() => act(channel)}
			>
				{#if copiedOpen && copied?.segment === channel}
					<CheckIcon class="size-[18px] opacity-90" />
				{:else if mode === "qr"}
					<QrCodeIcon class="size-[18px] opacity-90" />
				{:else}
					<CopyIcon class="size-[18px] opacity-90" />
				{/if}
			</button>
		</div>
	{/each}

	<div class="-mt-1 flex justify-end">
		<div class="inline-flex h-8 items-center rounded-full bg-muted p-0.5 text-xs font-medium text-muted-foreground" role="group" aria-label="Side button">
			<button type="button" class={seg} aria-pressed={mode === "qr"} onclick={() => (mode = "qr")}>
				<QrCodeIcon class="size-3.5" />
				QR
			</button>
			<button type="button" class={seg} aria-pressed={mode === "copy"} onclick={() => (mode = "copy")}>
				<CopyIcon class="size-3.5" />
				Copy
			</button>
		</div>
	</div>

	<Popover.Root bind:open={() => copiedOpen, (o) => (copiedOpen = o)}>
		<Popover.Portal>
			<Popover.Content
				forceMount
				customAnchor={copied?.anchor ?? null}
				side="top"
				sideOffset={6}
				collisionPadding={12}
				trapFocus={false}
				onOpenAutoFocus={(e) => e.preventDefault()}
				onCloseAutoFocus={(e) => e.preventDefault()}
			>
				{#snippet child({ props, wrapperProps, open })}
					{#if open && copied}
						<div {...wrapperProps}>
							<div
								{...props}
								class="z-50 flex items-center gap-1.5 rounded-full bg-foreground px-3 py-1.5 text-xs font-medium text-background shadow-md outline-none"
								transition:fly={{ y: 4, duration: 150 }}
							>
								<CheckIcon class="size-3.5" />
								Copied <span class="font-mono">{copied.text}</span>
								<Popover.Arrow class="text-foreground" />
							</div>
						</div>
					{/if}
				{/snippet}
			</Popover.Content>
		</Popover.Portal>
	</Popover.Root>
</div>
