<script>
	
	import { page } from '$app/stores';
	import { tweened } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { normalize } from '$lib/normalize';
	import * as Card from "$lib/components/ui/card";
	import { MessageCircle, Send, Phone } from 'lucide-svelte';

	export let data;
	export let value = '';
	let normed = '';
	let country_code = data.country_phone || '1';

	let contentWidth = 160;
	let contentHeight = 105;

	const contentScale = tweened(1, {
		duration: 500,
		easing: cubicOut
	});

	$: normed = normalize(value, country_code);
	$: ready = normed.length > 0;

	function focusInputField() {
		document.querySelector('input[type="tel"]').focus();
	}
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>Normalizer</Card.Title>
		<Card.Description>Enter your phone number to generate messaging links</Card.Description>
	</Card.Header>
	<Card.Content>
		<div class="inputs-container" style="text-align: center;">
			<input bind:value={country_code} placeholder="country code" size="3" />
			<input bind:value autofocus type="tel" placeholder="11 2222 3333" size="12" />
		</div>
		{normed}
		<div class="wrappa">
			<div>
				<ul style="display: flex; justify-content: center;">
					<li style="margin-right: 16px;">
						<a href="sms:+{normed}" style={ready ? '' : 'color: grey; pointer-events: none'}>
							<MessageCircle size="24" />
						</a>
					</li>
					<li style="margin-right: 16px;">
						<a href="https://t.me/{normed}" target="_blank" rel="noreferrer" style={ready ? '' : 'color: grey; pointer-events: none'}>
							<Send size="24" />
						</a>
					</li>
					<li>
						<a href="https://wa.me/{normed}" target="_blank" rel="noreferrer" style={ready ? '' : 'color: grey; pointer-events: none'}>
							<Phone size="24" />
						</a>
					</li>
				</ul>
			</div>
		</div>
	</Card.Content>
</Card.Root>

