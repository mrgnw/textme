<script lang="ts">
	import ChevronDownIcon from "@lucide/svelte/icons/chevron-down";
	import { getCountryByIso2 } from "svelte-tel-input/utils";
	import type { CountryCode } from "svelte-tel-input/types";
	import { Button } from "$lib/components/ui/button";
	import { getFlag } from "$lib/countryFlags.js";
	import CountrySelector from "./CountrySelector.svelte";

	let { country = $bindable() }: { country: CountryCode | null } = $props();

	let open = $state(false);
	const dialCode = $derived(country ? getCountryByIso2(country)?.dialCode : undefined);
</script>

<Button
	variant="outline"
	size="sm"
	class="h-8 gap-1.5 rounded-full px-3 font-medium"
	aria-label="Change country"
	onclick={() => (open = true)}
>
	<span>{country ? getFlag(country) : "🌐"}</span>
	<span class="tabular-nums">{dialCode ? `+${dialCode}` : ""}</span>
	<ChevronDownIcon class="size-3.5 text-muted-foreground" />
</Button>
<CountrySelector bind:value={country} bind:open />
