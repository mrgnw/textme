<script lang="ts">
	import { page } from "$app/state";
	import { renderSVG } from "uqr";
	import { CHANNELS, channelUrl, shownUrl, type Channel } from "$lib/channels";

	interface Props {
		e164: string;
		channel: Channel;
	}

	let { e164, channel }: Props = $props();

	let value = $derived(channelUrl(page.url.origin, e164, channel));
	let shown = $derived(shownUrl(value));
	let svg = $derived(renderSVG(value, { pixelSize: 4 }));
</script>

<div class="space-y-3 rounded-2xl p-5 shadow-sm {CHANNELS[channel].fill}">
	<div
		role="img"
		aria-label="QR code"
		class="mx-auto aspect-square w-full max-w-56 rounded-xl bg-white p-3 text-black [&>svg]:h-full [&>svg]:w-full"
	>
		{@html svg}
	</div>
	<p class="truncate text-center font-mono text-sm opacity-90">{shown}</p>
</div>
