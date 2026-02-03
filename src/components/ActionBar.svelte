<script>
	import ActionButton from "./ActionButton.svelte";
	import RiChat3Line from "~icons/ri/chat-3-line";
	import RiWhatsappLine from "~icons/ri/whatsapp-line";
	import RiTelegramLine from "~icons/ri/telegram-line";
	import { ContactRound } from "lucide-svelte";

	let { valid = false, value = '', contactName = $bindable(''), onDownloadContact } = $props();

	let telegramUrl = $derived(valid ? `https://t.me/${value}` : '#');
	let whatsappUrl = $derived(valid ? `https://wa.me/${value}` : '#');
	let smsUrl = $derived(valid ? `sms:${value}` : '#');
</script>

<div class="action-bar">
	{#if valid}
		<div class="contact-name-row">
			<input
				type="text"
				class="contact-input"
				placeholder="Contact name (optional)"
				bind:value={contactName}
			/>
		</div>
	{/if}
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

	.contact-name-row {
		display: flex;
		justify-content: center;
		padding: 0.5rem 1rem 0;
	}

	.contact-input {
		width: 12rem;
		border-radius: 0.75rem;
		border: 1px solid hsl(var(--border));
		background: hsl(var(--background));
		padding: 0.5rem 0.75rem;
		font-size: 0.875rem;
		text-align: center;
	}

	.contact-input:focus {
		outline: none;
		ring: 2px;
		ring-color: hsl(var(--ring));
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
			display: flex;
			flex-direction: column-reverse;
		}

		.contact-name-row {
			padding: 0.5rem 0 0;
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
