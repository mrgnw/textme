<script>

	import { page } from '$app/stores';
	import { tweened } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { normalize } from '$lib/normalize';
	import * as Card from "$lib/components/ui/card";
	import { MessageCircle, Send, Phone } from 'lucide-svelte';
	import { Badge } from "$lib/components/ui/badge";

	let { data, value = '' } = $props();
	$effect(() => {
		if (value == '') {
			focusInputField();
		}
	});

	let country_code = $state(data.country_phone || '1');

	let contentWidth = 160;
	let contentHeight = 105;

	const contentScale = tweened(1, {
		duration: 500,
		easing: cubicOut
	});

	let normed = $derived(normalize(value, country_code));
	let smsLink = $derived(`sms:${normed}`);
	let whatsappLink = $derived(`https://wa.me/${normed}`);
	let telegramLink = $derived(`https://t.me/${normed}`);
	let is_valid = $derived(isValidPhoneNumber(normed));

	function focusInputField() {
		document.querySelector('input[type="tel"]').focus();
	}
	function isValidPhoneNumber(phone) {
		const phoneRegex = /^\+?[1-9]\d{1,14}$/;
		return phoneRegex.test(phone);
	}
</script>

<Card.Root class="max-w-lg mx-auto">
	<Card.Header>
		<Card.Title>Social message links</Card.Title>
		<Card.Description>Enter a phone number to get links to send DM's on supported apps</Card.Description>
	</Card.Header>
	<Card.Content>
		<div class="inputs-container" style="text-align: center;">
			<input bind:value={country_code} placeholder="country code" size="3" />
			<input bind:value={value} type="tel" placeholder="11 2222 3333" size="12" />
		</div>
		<div class="flex justify-center items-center py-2">
			<Badge variant={is_valid ? 'default' : 'outline' }>{normed}</Badge>
		</div>
		<div>
			<div>
				<ul style="display: flex; justify-content: center;">
					<li style="margin-right: 16px;">
						<a href={smsLink}>
							<MessageCircle size="24" />
						</a>
					</li>
					<li style="margin-right: 16px;">
						<a href={whatsappLink}>
							<Send size="24" />
						</a>
					</li>
					<li>
						<a href={telegramLink}>
							<Phone size="24" />
						</a>
					</li>
				</ul>
			</div>
		</div>
	</Card.Content>
</Card.Root>