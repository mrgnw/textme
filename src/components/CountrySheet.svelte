<script lang="ts">
	import { Dialog } from "bits-ui";
	import { Search, X, Check } from "lucide-svelte";
	import { normalizedCountries } from "svelte-tel-input";
	import type { CountryCode } from "svelte-tel-input/types";
	import { getFlag } from "$lib/countryFlags.js";

	interface Props {
		value?: CountryCode | null;
		open?: boolean;
	}

	let { value = $bindable(), open = $bindable(false) }: Props = $props();

	let searchQuery = $state("");

	let filteredCountries = $derived(
		searchQuery
			? normalizedCountries.filter((c) =>
					c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
					c.iso2.toLowerCase().includes(searchQuery.toLowerCase()) ||
					String(c.dialCode).includes(searchQuery)
				)
			: normalizedCountries
	);

	function handleSelect(iso2: CountryCode) {
		value = iso2;
		searchQuery = "";
		open = false;
	}
</script>

<Dialog.Root bind:open onOpenChange={(o) => { if (!o) searchQuery = ""; }}>
	<Dialog.Portal>
		<Dialog.Overlay class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm" />
		<Dialog.Content
			class="fixed inset-x-0 bottom-0 z-50 flex max-h-[85vh] flex-col rounded-t-2xl bg-background"
		>
			<div class="flex items-center justify-between border-b px-4 py-3">
				<Dialog.Title class="text-lg font-semibold">Select Country</Dialog.Title>
				<Dialog.Close class="rounded-full p-1 hover:bg-muted transition-colors">
					<X class="h-5 w-5" />
				</Dialog.Close>
			</div>

			<div class="border-b px-4 py-2">
				<div class="relative">
					<Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
					<input
						type="text"
						bind:value={searchQuery}
						placeholder="Search countries..."
						class="w-full rounded-xl border border-input bg-background py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
					/>
				</div>
			</div>

			<div class="flex-1 overflow-y-auto">
				{#each filteredCountries as country (country.id)}
					<button
						type="button"
						onclick={() => handleSelect(country.iso2)}
						class="flex w-full items-center gap-3 px-4 py-3 hover:bg-accent/50 active:bg-accent transition-colors {value === country.iso2 ? 'bg-accent/30' : ''}"
					>
						<span class="text-xl">{getFlag(country.iso2)}</span>
						<span class="flex-1 truncate text-left">{country.name}</span>
						<span class="text-muted-foreground text-sm">+{country.dialCode}</span>
						{#if value === country.iso2}
							<Check class="h-4 w-4 text-primary" />
						{/if}
					</button>
				{:else}
					<div class="px-4 py-8 text-center text-muted-foreground">
						No countries found
					</div>
				{/each}
			</div>
		</Dialog.Content>
	</Dialog.Portal>
</Dialog.Root>
