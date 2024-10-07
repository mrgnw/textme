<script>
	import PhoneInput from "$components/PhoneInput.svelte";
	import RiChat3Line from "~icons/ri/chat-3-line";
	import RiWhatsappLine from "~icons/ri/whatsapp-line";
	import RiTelegramLine from "~icons/ri/telegram-line";
	import RiPhoneLine from "~icons/ri/phone-line";

	let country = $state("ES");
	let valid = $state(false);
	let value = $state(null);
	let detailedValue = $state(null);
	let over_icon = $state(null);
	$effect(() => {
		console.log(over_icon);
	});
</script>

<PhoneInput bind:country bind:valid bind:value bind:detailedValue />

<div>
	<div>
		<ul class="flex justify-center space-x-4 sm:space-x-6 lg:space-x-8">
			{#if valid}
				<li>
					<a href={`sms:${value}`} target="_blank">
						<RiChat3Line width="4em" height="4em" />
					</a>
				</li>
				<!-- <li>
				<a href={`tel:${value}`} target="_blank">
					<RiPhoneLine width="4em" height="4em"/>
				</a>
			</li> -->
				<li>
					<a href={`https://wa.me/${value}`} target="_blank">
						<RiWhatsappLine width="4em" height="4em" />
					</a>
				</li>
				<li>
					<a href={`https://t.me/${value}`} target="_blank">
						<RiTelegramLine width="4em" height="4em" />
					</a>
				</li>
			{:else}
				<li class="text-gray-500">
					<RiChat3Line width="4em" height="4em" />
				</li>
				<!-- <li class="text-gray-500">
					<RiPhoneLine width="4em" height="4em"/>
				</li> -->
				<li class="text-gray-500">
					<RiWhatsappLine width="4em" height="4em" />
				</li>
				<li class="text-gray-500">
					<RiTelegramLine width="4em" height="4em" />
				</li>
			{/if}
		</ul>
	</div>
</div>

<pre><code class={valid ? "valid" : "invalid"}>{valid}</code></pre>
<pre><code>{JSON.stringify(detailedValue, null, 2)}</code></pre>

<style>
	.valid {
		color: rgb(1, 231, 135);
		font-weight: bold;
	}

	.invalid {
		border: 1px solid red;
	}
</style>
