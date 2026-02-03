<script>
	import ActionButton from "./ActionButton.svelte";
	import RiChat3Line from "~icons/ri/chat-3-line";
	import RiWhatsappLine from "~icons/ri/whatsapp-line";
	import RiTelegramLine from "~icons/ri/telegram-line";
	import { CopyIcon, ContactRound } from "lucide-svelte";

	let { valid = false, value = '', onCopy, onDownloadContact } = $props();

	let telegramUrl = $derived(valid ? `https://t.me/${value}` : '#');
	let whatsappUrl = $derived(valid ? `https://wa.me/${value}` : '#');
	let smsUrl = $derived(valid ? `sms:${value}` : '#');
</script>

<div class="action-bar">
	<div class="action-bar-inner">
		<ActionButton
			href={telegramUrl}
			icon={RiTelegramLine}
			label="Telegram"
			highlighted={valid}
			disabled={!valid}
		/>
		<ActionButton
			href={whatsappUrl}
			icon={RiWhatsappLine}
			label="WhatsApp"
			disabled={!valid}
		/>
		<ActionButton
			href={smsUrl}
			icon={RiChat3Line}
			label="SMS"
			disabled={!valid}
		/>
		<ActionButton
			onclick={onDownloadContact}
			icon={ContactRound}
			label="Contact"
			disabled={!valid}
		/>
		<ActionButton
			onclick={onCopy}
			icon={CopyIcon}
			label="Copy"
			disabled={!valid}
		/>
	</div>
</div>

<style>
	.action-bar {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		background: hsl(var(--background) / 0.95);
		backdrop-filter: blur(10px);
		border-top: 1px solid hsl(var(--border));
		padding-bottom: env(safe-area-inset-bottom);
		z-index: 50;
	}

	.action-bar-inner {
		display: flex;
		justify-content: space-around;
		align-items: center;
		padding: 0.75rem 1rem;
		max-width: 28rem;
		margin: 0 auto;
	}

	@media (min-width: 640px) {
		.action-bar {
			position: relative;
			bottom: auto;
			left: auto;
			right: auto;
			background: transparent;
			backdrop-filter: none;
			border-top: none;
			padding-bottom: 0;
		}

		.action-bar-inner {
			padding: 1rem 0;
			gap: 0.5rem;
		}
	}

	:global(.action-bar .action-button.highlighted:not(.disabled)) {
		color: #0088cc;
	}

	:global(.action-bar .action-button:not(.disabled):nth-child(2)) {
		color: #25D366;
	}

	:global(.action-bar .action-button:not(.disabled):nth-child(3)) {
		color: #48bb78;
	}

	:global(.action-bar .action-button:not(.disabled):nth-child(4)) {
		color: hsl(16, 85%, 55%);
	}
</style>
