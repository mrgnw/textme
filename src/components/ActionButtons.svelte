<script lang="ts">
	import RiTelegramLine from "~icons/ri/telegram-line";
	import RiWhatsappLine from "~icons/ri/whatsapp-line";
	import RiChat3Line from "~icons/ri/chat-3-line";
	import CheckIcon from "@lucide/svelte/icons/check";
	import CopyIcon from "@lucide/svelte/icons/copy";
	import QrCodeIcon from "@lucide/svelte/icons/qr-code";
	import { copyToClipboard } from "$lib/utils";
	import { links, type App } from "$lib/phone";

	interface Props {
		e164: string | null;
		onqr: (app: App) => void;
	}

	let { e164, onqr }: Props = $props();

	let mode = $state<"copy" | "qr">("copy");
	let copied = $state<App | null>(null);

	const hrefs = $derived(e164 ? links(e164) : null);
	const disabled = $derived(!hrefs);

	const APPS = [
		{ app: "telegram", label: "Telegram", icon: RiTelegramLine, fill: "bg-telegram text-telegram-foreground", line: "border-telegram-foreground/30" },
		{ app: "whatsapp", label: "WhatsApp", icon: RiWhatsappLine, fill: "bg-whatsapp text-whatsapp-foreground", line: "border-whatsapp-foreground/30" },
		{ app: "sms", label: "SMS", icon: RiChat3Line, fill: "bg-sms text-sms-foreground", line: "border-sms-foreground/30" },
	] as const;

	const focus = "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-card";
	const seg = "inline-flex h-7 items-center gap-1.5 rounded-full px-2.5 transition-colors aria-pressed:bg-background aria-pressed:text-foreground aria-pressed:shadow-sm";

	function act(app: App) {
		if (!hrefs) return;
		if (mode === "qr") {
			onqr(app);
			return;
		}
		copyToClipboard(hrefs[app], hrefs[app].replace(/^https:\/\//, ""));
		copied = app;
		setTimeout(() => {
			if (copied === app) copied = null;
		}, 1500);
	}
</script>

<div class="grid gap-3">
	{#each APPS as { app, label, icon: Icon, fill, line } (app)}
		<div class="flex h-12 w-full overflow-hidden rounded-full {fill} {disabled ? 'pointer-events-none opacity-50' : ''}">
			<a
				href={hrefs?.[app] ?? "#"}
				target="_blank"
				class="inline-flex h-12 flex-1 items-center justify-center gap-2 pl-14 text-xl font-bold transition-colors hover:bg-black/10 [&_svg]:size-5 {focus}"
				aria-disabled={disabled}
				tabindex={disabled ? -1 : undefined}
			>
				<Icon />
				{label}
			</a>
			<button
				type="button"
				class="inline-flex h-12 w-14 items-center justify-center border-l {line} transition-colors hover:bg-black/10 {copied === app ? 'bg-black/10' : ''} {focus}"
				aria-label={mode === "qr" ? `${label} QR code` : `Copy ${label} link`}
				{disabled}
				onclick={() => act(app)}
			>
				{#if copied === app}
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
</div>
