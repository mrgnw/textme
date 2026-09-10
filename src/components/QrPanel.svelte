<script lang="ts">
	import { page } from "$app/state";
	import { renderSVG } from "uqr";
	import { CHANNELS, channelUrl, shownUrl, type Channel } from "$lib/channels";

	interface Props {
		e164: string;
		channel: Channel;
		class?: string;
	}

	let { e164, channel, class: klass = "" }: Props = $props();

	let value = $derived(channelUrl(page.url.origin, e164, channel));
	let shown = $derived(shownUrl(value));
	let svg = $derived(renderSVG(value, { pixelSize: 4 }));
</script>

<div class="space-y-4 rounded-2xl p-5 text-center shadow-sm {CHANNELS[channel].fill} {klass}">
	<h2 class="font-display text-lg font-bold tracking-tight">{CHANNELS[channel].label}</h2>
	<div
		role="img"
		aria-label="QR code"
		class="mx-auto aspect-square w-full max-w-56 rounded-xl bg-white p-3 text-black [&>svg]:h-full [&>svg]:w-full"
	>
		{@html svg}
	</div>
	<p class="break-all font-mono text-sm leading-snug opacity-90">{shown}</p>
</div>
