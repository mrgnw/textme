<script>
	import { CopyIcon, ContactRound } from "lucide-svelte";
	import RiChat3Line from "~icons/ri/chat-3-line";
	import RiWhatsappLine from "~icons/ri/whatsapp-line";
	import RiTelegramLine from "~icons/ri/telegram-line";
	import { copyToClipboard, notifyDownload } from "$lib/utils";

	let { phone, name: initialName } = $props();

	let name = $state(initialName);

	let formatted = $derived(phone.startsWith("+") ? phone : `+${phone}`);
	let clean = $derived(phone.replace(/[^0-9]/g, ""));

	let telegramUrl = $derived(`https://t.me/${formatted}`);
	let whatsappUrl = $derived(`https://wa.me/${clean}`);
	let smsUrl = $derived(`sms:${formatted}`);

	function handleCopy() {
		copyToClipboard(formatted);
	}

	function downloadVCard() {
		const vcard = [
			"BEGIN:VCARD",
			"VERSION:3.0",
			`FN:${name || "Contact"}`,
			`TEL;TYPE=CELL:${formatted}`,
			`X-SOCIALPROFILE;TYPE=whatsapp:https://wa.me/${clean}`,
			`X-SOCIALPROFILE;TYPE=telegram:https://t.me/${formatted}`,
			"END:VCARD",
		].join("\n");

		const blob = new Blob([vcard], { type: "text/vcard" });
		const url = window.URL.createObjectURL(blob);
		const a = document.createElement("a");
		a.href = url;
		const safeName = (name || "contact")
			.replace(/[^a-z0-9]/gi, "_")
			.toLowerCase();
		a.download = `${safeName}.vcf`;
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
		window.URL.revokeObjectURL(url);
		notifyDownload(`${safeName}.vcf`);
	}
</script>

<div class="bulk-row">
	<span class="phone-number">{formatted}</span>

	<div class="actions">
		<button onclick={handleCopy} class="icon-btn copy" aria-label="Copy number">
			<CopyIcon size={18} />
		</button>
		<a
			href={telegramUrl}
			target="_blank"
			class="icon-btn telegram"
			aria-label="Telegram"
		>
			<RiTelegramLine class="w-[18px] h-[18px]" />
		</a>
		<a href={smsUrl} class="icon-btn sms" aria-label="SMS">
			<RiChat3Line class="w-[18px] h-[18px]" />
		</a>
		<a
			href={whatsappUrl}
			target="_blank"
			class="icon-btn whatsapp"
			aria-label="WhatsApp"
		>
			<RiWhatsappLine class="w-[18px] h-[18px]" />
		</a>
		<button
			onclick={downloadVCard}
			class="icon-btn contact"
			aria-label="Download contact"
		>
			<ContactRound size={18} />
		</button>
	</div>

	<input type="text" class="name-input" bind:value={name} placeholder="Name" />
</div>

<style>
	.bulk-row {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 0;
		border-bottom: 1px solid hsl(var(--border));
		flex-wrap: wrap;
	}

	.phone-number {
		font-family: monospace;
		font-size: 0.95rem;
		font-weight: 500;
		white-space: nowrap;
		min-width: 0;
	}

	.actions {
		display: flex;
		align-items: center;
		gap: 0.25rem;
		flex-shrink: 0;
	}

	.icon-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 0.35rem;
		border-radius: 0.5rem;
		border: none;
		background: transparent;
		cursor: pointer;
		color: hsl(var(--muted-foreground));
		transition: all 0.15s ease;
		text-decoration: none;
	}

	.icon-btn:hover {
		background: hsl(var(--muted));
		transform: scale(1.1);
	}

	.icon-btn.telegram:hover {
		color: #0088cc;
	}
	.icon-btn.whatsapp:hover {
		color: #25d366;
	}
	.icon-btn.sms:hover {
		color: #48bb78;
	}
	.icon-btn.contact:hover {
		color: hsl(16, 85%, 55%);
	}
	.icon-btn.copy:hover {
		color: hsl(var(--foreground));
	}

	.name-input {
		flex: 1;
		min-width: 5rem;
		border: 1px solid transparent;
		border-radius: 0.5rem;
		padding: 0.3rem 0.5rem;
		font-size: 0.875rem;
		background: transparent;
		color: hsl(var(--foreground));
	}

	.name-input:hover {
		border-color: hsl(var(--border));
	}

	.name-input:focus {
		outline: none;
		border-color: hsl(var(--ring));
		background: hsl(var(--background));
	}

	.name-input::placeholder {
		color: hsl(var(--muted-foreground));
	}
</style>
