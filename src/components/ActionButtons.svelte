<script lang="ts">
	import RiTelegramLine from "~icons/ri/telegram-line";
	import RiWhatsappLine from "~icons/ri/whatsapp-line";
	import RiChat3Line from "~icons/ri/chat-3-line";
	import { Button } from "$lib/components/ui/button";
	import { links } from "$lib/phone";

	interface Props {
		e164: string | null;
	}

	let { e164 }: Props = $props();

	const hrefs = $derived(e164 ? links(e164) : null);
	const disabled = $derived(!hrefs);
	const base = "h-12 w-full rounded-full text-xl font-bold [&_svg]:size-5";
	const off = "pointer-events-none opacity-50";
</script>

<div class="grid gap-3">
	<Button
		href={hrefs?.telegram ?? "#"}
		target="_blank"
		size="lg"
		class="{base} bg-telegram text-telegram-foreground hover:bg-telegram/90 {disabled ? off : ''}"
		aria-disabled={disabled}
		tabindex={disabled ? -1 : undefined}
	>
		<RiTelegramLine />
		Telegram
	</Button>
	<Button
		href={hrefs?.whatsapp ?? "#"}
		target="_blank"
		size="lg"
		class="{base} bg-whatsapp text-whatsapp-foreground hover:bg-whatsapp/90 {disabled ? off : ''}"
		aria-disabled={disabled}
		tabindex={disabled ? -1 : undefined}
	>
		<RiWhatsappLine />
		WhatsApp
	</Button>
	<Button
		href={hrefs?.sms ?? "#"}
		target="_blank"
		size="lg"
		class="{base} bg-sms text-sms-foreground hover:bg-sms/90 {disabled ? off : ''}"
		aria-disabled={disabled}
		tabindex={disabled ? -1 : undefined}
	>
		<RiChat3Line />
		SMS
	</Button>
</div>
