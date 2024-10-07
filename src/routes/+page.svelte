<script>
	import { page } from '$app/stores';
	import PhoneInput from "$components/PhoneInput.svelte";
	import PhoneDebug from "$components/PhoneDebug.svelte";
	import { copyToClipboard } from "$lib/utils";
	
	import RiChat3Line from "~icons/ri/chat-3-line";
	import RiWhatsappLine from "~icons/ri/whatsapp-line";
	import RiTelegramLine from "~icons/ri/telegram-line";
	import { CopyIcon } from "lucide-svelte";
	
	import * as Card from "$lib/components/ui/card";
	import { Badge } from "$lib/components/ui/badge";
	
	import { fly } from 'svelte/transition';
	import { scale } from 'svelte/transition';

	let cf_data = $state($page.data);
	let country = $state(cf_data.ip_country ? cf_data.ip_country.toUpperCase() : "US");
	let valid = $state(false);
	let value = $state(null);
	let detailedValue = $state(null);

	let showDebug = $state(false);
	const konami = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
	let pos = $state(0);

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

		window.addEventListener('keydown', handleKeydown);

		return () => {
			window.removeEventListener('keydown', handleKeydown);
		};
	});

	function focusInputField() {
		document.querySelector('input[type="tel"]').focus();
	}

	function handleCopy(){
		copyToClipboard(detailedValue.nationalNumber);
	}

	function debugTransition(node, { delay = 0, duration = 300 }) {
		return {
			delay,
			duration,
			css: (t, u) => `
				opacity: ${t};
				transform: scale(${1 - 0.1 * u}) translateY(${-10 * u}px);
			`
		};
	}
</script>

<Card.Root class="max-w-2xl mx-auto p-6 sm:p-8 lg:p-10 my-8">
	<Card.Header>
		<Card.Title class="text-3xl sm:text-4xl lg:text-5xl">Social message links</Card.Title>
		<Card.Description class="text-xl sm:text-2xl lg:text-3xl">Enter a phone number to get direct message links on supported apps</Card.Description>
	</Card.Header>
	<Card.Content>
		<div class="inputs-container text-center mb-6">
			<PhoneInput bind:country bind:valid bind:value bind:detailedValue />
		</div>
		<div>
			<ul class="flex justify-center space-x-4 sm:space-x-6 lg:space-x-8">
				<li class={valid ? '' : 'text-gray-500'}>
					<a href={valid ? `sms:${value}` : '#'} target="_blank" class={valid ? 'hover:text-blue-500' : 'cursor-not-allowed'}>
						<RiChat3Line width="4em" height="4em" />
					</a>
				</li>
				<li class={valid ? '' : 'text-gray-500'}>
					<a href={valid ? `https://wa.me/${value}` : '#'} target="_blank" class={valid ? 'hover:text-green-500' : 'cursor-not-allowed'}>
						<RiWhatsappLine width="4em" height="4em" />
					</a>
				</li>
				<li class={valid ? '' : 'text-gray-500'}>
					<a href={valid ? `https://t.me/${value}` : '#'} target="_blank" class={valid ? 'hover:text-blue-400' : 'cursor-not-allowed'}>
						<RiTelegramLine width="4em" height="4em" />
					</a>
				</li>
			</ul>
		</div>
		<div class="flex justify-center items-center py-4">
			{#if valid}
			<div transition:scale={{ duration: 300, start: 0.9 }}>
				<Badge 
					variant={valid ? 'default' : 'outline'} 
					class="text-lg sm:text-xl lg:text-2xl flex items-center group transition-colors duration-200 ease-in-out bg-black text-white hover:bg-black"
				>
					<span class="select-text">{detailedValue?.formatInternational || 'Enter a phone number'}</span>
					<button 
						on:click={handleCopy} 
						class="ml-2 p-1 rounded focus:outline-none focus:ring-2 focus:ring-white/50"
						aria-label="Copy number"
					>
						<CopyIcon size={20} class="transition-colors duration-200 ease-in-out hover:text-blue-500" />
					</button>
				</Badge>
			</div>
			{/if}
		</div>
	</Card.Content>
</Card.Root>

{#if showDebug}
	<div class="debug" transition:fly={{ x: -300, duration: 300 }}>
		<PhoneDebug bind:value bind:detailedValue bind:cf_data />
	</div>
{/if}

<style>
	:global(.inputs-container input) {
		@apply text-lg sm:text-xl lg:text-2xl p-2 sm:p-3 lg:p-4;
	}	
</style>
