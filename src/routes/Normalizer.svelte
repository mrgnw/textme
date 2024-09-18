<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { scale } from 'svelte/transition';
	import { tweened } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import Share from './Share.svelte';
	import { normalize } from '$lib/normalize';

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

	const updateScale = () => {
		const viewportWidth = window.innerWidth;
		const viewportHeight = window.innerHeight;
		const widthScale = viewportWidth / contentWidth;
		const heightScale = viewportHeight / contentHeight;
		const newScale = Math.min(widthScale, heightScale);
		contentScale.set(newScale);
	};

	// Update the scale whenever the window is resized
	onMount(() => {
		updateScale();
		window.addEventListener('resize', updateScale);
	});

	$: normed = normalize(value, country_code);
	$: ready = normed.length > 0;

	// function copy_number(){
	// 	navigator.clipboard.writeText(normed);
	// }
	function focusInputField(){
		document.querySelector('input[type="tel"]').focus();
	}
</script>

<div class="base">
<div class="container">
	<div
		class="content"
	>
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
							<img src="/sms.svg" height="24px" alt="Telegram" />
						</a>
					</li>
					<li style="margin-right: 16px;">
						<a href="https://t.me/{normed}" target="_blank" rel="noreferrer" style={ready ? '' : 'color: grey; pointer-events: none'}>
							<img src="/telegram.svg" height="24px" alt="Telegram" />
						</a>
					</li>
					<li>
						<a href="https://wa.me/{normed}" target="_blank" rel="noreferrer" style={ready ? '' : 'color: grey; pointer-events: none'}>
							<img src="/WhatsApp.svg" height="24px" alt="Fucking WhatsApp, god help us all" />
						</a>
					</li>
				</ul>
			</div>
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
		/* display: none; */
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

	.container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100%;
	}
	.base {
		height: 100%;
		width: 100%;
	}

</style>
