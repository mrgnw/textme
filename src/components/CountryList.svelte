<script lang="ts">
	import { countries } from "svelte-tel-input";
	import type { CountryCode } from "svelte-tel-input/types";
	import CheckIcon from "@lucide/svelte/icons/check";
	import SearchIcon from "@lucide/svelte/icons/search";
	import { getFlag } from "$lib/countryFlags.js";

	interface Props {
		value: CountryCode | null;
		onselect: (iso2: CountryCode) => void;
	}

	let { value, onselect }: Props = $props();

	let query = $state("");

	const filtered = $derived.by(() => {
		const q = query.trim().toLowerCase();
		if (!q) return countries;
		return countries.filter(
			(c) => c.name.toLowerCase().includes(q) || c.iso2.toLowerCase() === q || String(c.dialCode).includes(q.replace("+", "")),
		);
	});
</script>

<div class="border-b p-2">
	<div class="flex h-10 items-center gap-2 rounded-md border border-input px-3">
		<SearchIcon class="size-4 shrink-0 text-muted-foreground" />
		<input
			bind:value={query}
			type="search"
			placeholder="Search country or code"
			aria-label="Search country or code"
			class="flex-1 bg-transparent text-sm outline-none placeholder:text-muted-foreground"
		/>
	</div>
</div>
<ul class="max-h-[60vh] overflow-y-auto p-1 text-sm">
	{#each filtered as c (c.id)}
		<li>
			<button
				type="button"
				class="flex h-10 w-full items-center gap-3 rounded-sm px-2 hover:bg-accent hover:text-accent-foreground {value === c.iso2 ? 'bg-accent text-accent-foreground' : ''}"
				onclick={() => onselect(c.iso2 as CountryCode)}
			>
				<span class="text-lg">{getFlag(c.iso2)}</span>
				<span class="flex-1 truncate text-left">{c.name}</span>
				<span class="tabular-nums text-muted-foreground">+{c.dialCode}</span>
				{#if value === c.iso2}
					<CheckIcon class="size-4 text-primary" />
				{:else}
					<span class="w-4"></span>
				{/if}
			</button>
		</li>
	{:else}
		<li class="px-2 py-6 text-center text-muted-foreground">No countries found</li>
	{/each}
</ul>
