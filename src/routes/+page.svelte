<script>
	// todo: read clipboard on mount
	import { onMount } from 'svelte';

	let value = '';

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
		console.debug(result);
		return result;
	}
	function setCountryCode(code) {
		country_code = code;
	}

	// let value = '';
	let normed = '';
	let country_code = '54';

	$: normed = norm(value, country_code);
	$: ready = normed.length > 0;
</script>

<div class="flags">
	<span on:click={() => setCountryCode('1')}>🇺🇸</span>
	<span on:click={() => setCountryCode('52')}>🇲🇽</span>
	<span on:click={() => setCountryCode('54')}>🇦🇷</span>
	<span on:click={() => setCountryCode('55')}>🇧🇷</span>
</div>
<input bind:value={country_code} placeholder="country code" size="3" />
<input bind:value type="tel" placeholder="11 2222 3333" size="12" />

<div class="wrappa">
	<div class={ready ? 'apps' : 'not-ready'}>
		<ul>
			<li>
				<a href="sms:+{normed}"> <img src="/sms.svg" height="24px" alt="Telegram" /></a>
			</li>
			<li>
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

<style>
	.wrappa {
		min-height: 2em;
	}
	.flags, .apps {
		display: flex;
		flex-direction: row;
		cursor: pointer;
		font-size: 2em;
    margin: 0 0.2em ;
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
		/* flex-direction: row; */
		list-style: none;
		padding: 0;
		margin: 0;
	}
	.apps li {
		margin: 0 0.1em;
	}
</style>
