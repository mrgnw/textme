<script>
	// todo: read clipboard on mount
	import { onMount } from 'svelte';
  // get ip country from cloudflare headers
  // https://support.cloudflare.com/hc/en-us/articles/200168236-How-does-Cloudflare-handle-HTTP-Request-headers-
  export async function load({ request }) {
    const country = request.headers['cf-ipcountry'];
    const data = { country };
    return { props: { data } };
  }
  export let data;

	let contentWidth = 200;
	let contentHeight = 105;
	let scale = 3;

	const updateScale = () => {
		const viewportWidth = window.innerWidth;
		const viewportHeight = window.innerHeight;
		const widthScale = viewportWidth / contentWidth;
		const heightScale = viewportHeight / contentHeight;
		scale = Math.min(widthScale, heightScale);
	};

	// Update the scale whenever the window is resized
	onMount(() => {
		updateScale();
		window.addEventListener('resize', updateScale);
	});

  onMount(async () => {
    if (navigator.clipboard === undefined) {
      console.error('Clipboard API not supported');
      return;
    }
    
    try {
      const text = await navigator.clipboard.readText();
      let xx = norm(text);
      console.log(xx);
      ready = true;
    } catch (err) {
      console.error('Failed to read clipboard contents: ', err);
    }
  });

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
<h1>Your geolocation data:</h1>
<ul>
  <li>Country code: {data.country}</li>
</ul>
<div class="container">
	<div class="content" style="transform: scale({scale}); transform-origin: top left;">
		<!-- <div class="flags">
			<span on:click={() => setCountryCode('1')}>🇺🇸</span>
			<span on:click={() => setCountryCode('52')}>🇲🇽</span>
			<span on:click={() => setCountryCode('54')}>🇦🇷</span>
			<span on:click={() => setCountryCode('55')}>🇧🇷</span>
		</div> -->

		<div class="inputs-container" style="text-align: center;">
			<input bind:value={country_code} placeholder="country code" size="3" />
			<input bind:value type="tel" placeholder="11 2222 3333" size="12" />
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
		margin: auto;
	}

	.wrappa {
		min-height: 2em;
	}
	.flags,
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
		/* flex-direction: row; */
		list-style: none;
		padding: 0;
		margin: 0;
	}
	.apps li {
		margin: 0 0.1em;
	}
</style>
