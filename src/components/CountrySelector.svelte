<script lang="ts">
	import { onMount } from "svelte";
	import type { CountryCode } from "svelte-tel-input/types";
	import CountryCombobox from "./CountryCombobox.svelte";
	import CountrySheet from "./CountrySheet.svelte";

	interface Props {
		value?: CountryCode | null;
		open?: boolean;
		class?: string;
	}

	let { value = $bindable(), open = $bindable(false), class: className }: Props = $props();

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
	<CountrySheet bind:value bind:open />
{:else}
	<CountryCombobox bind:value bind:open class={className} />
{/if}
