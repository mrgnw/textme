<script lang="ts">
	import { onMount } from "svelte";
	import type { CountryCode } from "svelte-tel-input/types";
	import CountryCombobox from "./CountryCombobox.svelte";
	import CountrySheet from "./CountrySheet.svelte";

	interface Props {
		value?: CountryCode | null;
		class?: string;
	}

	let { value = $bindable(), class: className }: Props = $props();

	let isMobile = $state(false);

	onMount(() => {
		const mq = window.matchMedia("(max-width: 640px)");
		isMobile = mq.matches;

		function handleChange(e: MediaQueryListEvent) {
			isMobile = e.matches;
		}

		mq.addEventListener("change", handleChange);
		return () => mq.removeEventListener("change", handleChange);
	});
</script>

{#if isMobile}
	<CountrySheet bind:value />
{:else}
	<CountryCombobox bind:value class={className} />
{/if}
