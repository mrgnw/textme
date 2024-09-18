<script>

	import { page } from '$app/stores';
	import { tweened } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { normalize } from '$lib/normalize';
	import * as Card from "$lib/components/ui/card";
	import { MessageCircle, Send, Phone } from 'lucide-svelte';
	import { Badge } from "$lib/components/ui/badge";
	import { Input } from "$lib/components/ui/input";

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

	// todo: separate number and country code logic?
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

<Card.Root class="max-w-2xl mx-auto p-6 sm:p-8 lg:p-10 my-8">
	<Card.Header>
		<Card.Title class="text-3xl sm:text-4xl lg:text-5xl">Social message links</Card.Title>
		<Card.Description class="text-xl sm:text-2xl lg:text-3xl">Enter a phone number to get direct message links on
			supported apps</Card.Description>
	</Card.Header>
	<Card.Content>
		<div class="inputs-container text-center">
			<Input bind:value={country_code} placeholder="country code" size="3"
				class="text-lg sm:text-xl lg:text-2xl p-2 sm:p-3 lg:p-4" />
			<Input bind:value={value} type="tel" placeholder="11 2222 3333" size="12"
				class="text-lg sm:text-xl lg:text-2xl p-2 sm:p-3 lg:p-4" />
		</div>
		<div class="flex justify-center items-center py-4">
			<!-- TODO: separate country code visually from phone number with a space -->
			<Badge variant={is_valid ? 'default' : 'outline' } class="text-lg sm:text-xl lg:text-2xl">
				{normed}
			</Badge>
		</div>
		<div>
			<div>
				<ul class="flex justify-center space-x-4 sm:space-x-6 lg:space-x-8">
					<li>
						<a href={smsLink} target="_blank">
							<MessageCircle size="24" class="sm:size-20 lg:size-24" />
						</a>
					</li>
					<li>
						<a href={whatsappLink} target="_blank">
							<Phone size="24" class="sm:size-20 lg:size-24" />
						</a>
					</li>
					<li>
						<a href={telegramLink} target="_blank">
							<Send size="24" class="sm:size-20 lg:size-24" />
						</a>
					</li>
				</ul>
			</div>
		</div>
	</Card.Content>
</Card.Root>