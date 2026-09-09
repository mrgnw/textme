<script lang="ts">
	import type { CountryCode } from "svelte-tel-input/types";
	import * as Dialog from "$lib/components/ui/dialog";
	import { Sheet } from "$lib/components/ui/sheet";
	import { isMobile } from "$lib/media.svelte";
	import CountryList from "./CountryList.svelte";

	interface Props {
		value?: CountryCode | null;
		open?: boolean;
	}

	let { value = $bindable(null), open = $bindable(false) }: Props = $props();

	function select(iso2: CountryCode) {
		value = iso2;
		open = false;
	}
</script>

{#if isMobile.current}
	<Sheet bind:open title="Country">
		<CountryList {value} onselect={select} />
	</Sheet>
{:else}
	<Dialog.Root bind:open>
		<Dialog.Content class="gap-0 p-0 sm:max-w-sm">
			<Dialog.Header class="px-4 pb-2 pt-4">
				<Dialog.Title>Country</Dialog.Title>
			</Dialog.Header>
			<CountryList {value} onselect={select} />
		</Dialog.Content>
	</Dialog.Root>
{/if}
