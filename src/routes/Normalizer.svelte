<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores'
	import { scale } from 'svelte/transition';
	import { tweened } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';

	export let data;
	export let value ='';
	let normed = '';
	let country_code = data.country_phone || '1';

	let contentWidth = 138;
	let contentHeight = 105;

	const contentScale = tweened(1, {
		duration: 500,
		easing: cubicOut,
	});

	
	function norm(phone, country_code = '1') {
		country_code = country_code.replace(/^0+/, '').replace(/[^0-9]/g, '');
		phone = phone.replace(/^0+/, '').replace(/[^0-9+]/g, '');
		let last10 = phone.slice(-10);
		// if last10 is 8 digits, add 11 to the front
		if (last10.length === 8) {
			last10 = `11${last10}`;
		}
		if (last10.length !== 10) {
			return '';
		}

		const prefix = phone.slice(0, -10).replace(/^\+/, '');
		const strippedPrefix = prefix;

		let result = '';

		// if strippedPrefix is digits, add country code
		if (strippedPrefix.match(/^\d+$/)) {
			result = `+${strippedPrefix}${last10}`;
		} else {
			result = `+${country_code}${last10}`;
		}
		return result;
	}

	$: normed = norm(value, country_code);
	$: ready = normed.length > 0;
</script>


<div class="container">
	
	<div class="content" 
	in:scale="{{ duration: $contentScale }}"
	style="transform-origin: top left; transform: scale({$contentScale})"
	>
		<div class="inputs-container" style="text-align: center;">
			<input bind:value={country_code} placeholder="country code" size="3" />
			<input bind:value autofocus type="tel" placeholder="11 2222 3333" size="12"/>
		</div>

		<div class="wrappa">
			<div class={ready ? 'apps' : 'not-ready'}>
				<ul style="display: flex; justify-content: center;">
					<li style="margin-right: 16px;">
						<a href="sms:+{normed}"> <img src="/sms.svg" height="24px" alt="Telegram" /></a>
					</li>
					<li style="margin-right: 16px;">
						<a href="https://t.me/{normed}" target="_blank" rel="noreferrer">
							<img src="/telegram.svg" height="24px" alt="Telegram" /></a
						>
					</li>
					<li>
						<a href="https://wa.me/{normed}" target="_blank" rel="noreferrer">
							<img src="/WhatsApp.svg" height="24px" alt="Fucking WhatsApp, god help us all" />
						</a>
					</li>
				</ul>
			</div>
		</div>
	</div>
</div>

<style>
	:root {
		overflow: hidden;
	}
	.inputs-container {
		width: 140px;
	}
	.container {
		display: flex;
		justify-content: center;
	}
	.content {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		margin-top: 2rem;
	}

	.wrappa {
		min-height: 2em;
	}
	.apps {
		font-size: 3em;
		display: flex;
		flex-direction: row;
		cursor: pointer;
		font-size: 2em;
		margin: 0 0.2em;
	}
	.not-ready {
		display: none;
	}
	span {
		-webkit-touch-callout: none;
		-webkit-user-select: none;
		-khtml-user-select: none;
		-moz-user-select: none;
		-ms-user-select: none;
		user-select: none;
	}
	ul {
		display: flex;
		list-style: none;
		padding: 0;
		margin: 0;
	}
	.apps li {
		margin: 0 0.1em;
	}
</style>
