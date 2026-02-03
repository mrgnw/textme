<script>
	import { page } from "$app/stores";
	import { goto } from "$app/navigation";
	import PhoneInput from "./PhoneInput.svelte";
	import PhoneDebug from "./PhoneDebug.svelte";
	import ActionBar from "./ActionBar.svelte";
	import { copyToClipboard, notifyDownload } from "$lib/utils";
	import { Badge } from "$lib/components/ui/badge";

	import { fly } from "svelte/transition";
	import { scale } from "svelte/transition";

	let { initialValue = null } = $props();

	let cf_data = $state($page.data);
	let country = $state(
		$page.data.ip_country ? $page.data.ip_country.toUpperCase() : "US"
	);
	let valid = $state(false);
	let value = $state(initialValue);
	let detailedValue = $state(null);

	let showDebug = $state(false);
	const konami = [
		"ArrowUp",
		"ArrowUp",
		"ArrowDown",
		"ArrowDown",
		"ArrowLeft",
		"ArrowRight",
		"ArrowLeft",
		"ArrowRight",
		"b",
		"a",
	];
	let pos = $state(0);

	let contactName = $state('');

	$effect(() => {
		const handleKeydown = (event) => {
			if (event.key === konami[pos]) {
				pos++;
				if (pos === konami.length) {
					showDebug = !showDebug;
					pos = 0;
				}
			} else {
				pos = 0;
			}
		};

		window.addEventListener("keydown", handleKeydown);

		return () => {
			window.removeEventListener("keydown", handleKeydown);
		};
	});

	// Navigation effect - clean and focused
	let debounceTimer;
	$effect(() => {
		if (valid && value && value !== initialValue) {
			clearTimeout(debounceTimer);
			debounceTimer = setTimeout(() => {
				const cleanDigits = value.replace(/[^\d]/g, '');
				if (cleanDigits) {
					goto(`/${cleanDigits}`, { replaceState: true, noScroll: true });
				}
			}, 500);
		}
		
		return () => clearTimeout(debounceTimer);
	});

	function focusInputField() {
		document.querySelector('input[type="tel"]').focus();
	}

	function handleCopy() {
		copyToClipboard(detailedValue.nationalNumber);
	}

	function debugTransition(node, { delay = 0, duration = 300 }) {
		return {
			delay,
			duration,
			css: (t, u) => `
				opacity: ${t};
				transform: scale(${1 - 0.1 * u}) translateY(${-10 * u}px);
			`,
		};
	}

	function downloadVCard(name = 'Contact') {
		if (!valid) return;
		const cleanPhone = value.replace(/[^\d]/g, '');
		const formattedPhone = cleanPhone.startsWith('+') ? cleanPhone : `+${cleanPhone}`;
		
		const vcard = [
			'BEGIN:VCARD',
			'VERSION:3.0',
			`FN:${name}`,
			`TEL;TYPE=CELL:${formattedPhone}`,
			`X-SOCIALPROFILE;TYPE=whatsapp:https://wa.me/${formattedPhone}`,
			`X-SOCIALPROFILE;TYPE=telegram:https://t.me/${formattedPhone}`,
			'END:VCARD'
		].join('\n');

		const blob = new Blob([vcard], { type: 'text/vcard' });
		const url = window.URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		const safeName = (name || 'contact').replace(/[^a-z0-9]/gi, '_').toLowerCase();
		a.download = `${safeName}.vcf`;
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
		window.URL.revokeObjectURL(url);
		notifyDownload(`${safeName}.vcf`);
		contactName = '';
	}
</script>

<div class="max-w-2xl mx-auto p-6 sm:p-8 lg:p-10 my-8 pb-32 sm:pb-8">
	<div class="text-center mb-8">
		<h1 class="text-3xl sm:text-4xl lg:text-5xl mb-4">Social message links</h1>
		<p class="text-xl sm:text-2xl lg:text-3xl text-muted-foreground">
			Enter a phone number to get direct message links on supported apps
		</p>
	</div>

	<div class="inputs-container text-center mb-6 flex justify-center">
		<PhoneInput bind:country bind:valid bind:value bind:detailedValue options={{}} />
	</div>

	<div class="flex justify-center items-center py-4">
		{#if valid}
			<div transition:scale={{ duration: 300, start: 0.9 }}>
				<Badge
					variant="default"
					class="text-lg sm:text-xl lg:text-2xl flex items-center gap-2 transition-all duration-200 ease-in-out bg-foreground text-background hover:bg-foreground/90 rounded-2xl px-4 py-2 shadow-lg hover:shadow-xl"
				>
					<span class="select-text">
						{detailedValue?.formatInternational || "Enter a phone number"}
					</span>
				</Badge>
			</div>
		{/if}
	</div>

	{#if valid}
		<div class="flex justify-center mb-4">
			<input
				type="text"
				class="w-48 rounded-xl border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring text-center"
				placeholder="Contact name (optional)"
				bind:value={contactName}
			/>
		</div>
	{/if}

	<ActionBar
		{valid}
		{value}
		onCopy={handleCopy}
		onDownloadContact={() => downloadVCard(contactName || 'Contact')}
	/>
</div>

{#if showDebug}
	<div class="debug" transition:fly={{ x: -300, duration: 300 }}>
		<PhoneDebug bind:value bind:detailedValue bind:cf_data />
	</div>
{/if}

<style>
	:global(.fixed) {
		z-index: 50;
	}
</style>
