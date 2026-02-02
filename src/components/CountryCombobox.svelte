<script lang="ts">
	import { Combobox } from "bits-ui";
	import { cn } from "$lib/utils.js";
	import { Check } from "lucide-svelte";
	import { normalizedCountries } from "svelte-tel-input";
	import type { CountryCode } from "svelte-tel-input/types";
	import { getFlag } from "$lib/countryFlags.js";

	interface Props {
		value?: CountryCode | null;
		open?: boolean;
		class?: string;
	}

	let { value = $bindable(), open = $bindable(false), class: className }: Props = $props();

	let searchValue = $state("");

	let filteredCountries = $derived(
		searchValue
			? normalizedCountries.filter((c) =>
					c.name.toLowerCase().includes(searchValue.toLowerCase()) ||
					c.iso2.toLowerCase().includes(searchValue.toLowerCase()) ||
					String(c.dialCode).includes(searchValue)
				)
			: normalizedCountries
	);

	function handleValueChange(newValue: string | undefined) {
		if (newValue) {
			value = newValue as CountryCode;
		}
	}
</script>

<Combobox.Root
	type="single"
	value={value ?? undefined}
	onValueChange={handleValueChange}
	bind:open
	onOpenChange={(o) => {
		if (!o) searchValue = "";
	}}
>
	<div class={cn("relative", className)}>
		<Combobox.Portal>
			<Combobox.Content
				class="z-50 max-h-72 min-w-[280px] overflow-hidden rounded-xl border bg-popover text-popover-foreground shadow-lg"
				sideOffset={8}
			>
				<div class="border-b px-3 py-2">
					<Combobox.Input
						oninput={(e) => (searchValue = e.currentTarget.value)}
						placeholder="Search countries..."
						class="w-full bg-transparent text-sm focus:outline-none placeholder:text-muted-foreground"
					/>
				</div>
				<div class="max-h-60 overflow-y-auto p-1">
					{#each filteredCountries as country (country.id)}
						<Combobox.Item
							value={country.iso2}
							label={country.name}
							class="relative flex cursor-pointer select-none items-center gap-3 rounded-lg px-2 py-1.5 text-sm outline-none transition-colors data-[highlighted]:bg-accent data-[highlighted]:text-accent-foreground"
						>
							{#snippet children({ selected })}
								<span class="text-xl">{getFlag(country.iso2)}</span>
								<span class="flex-1 truncate">{country.name}</span>
								<span class="text-muted-foreground text-sm">+{country.dialCode}</span>
								{#if selected}
									<Check class="h-4 w-4 text-primary" />
								{/if}
							{/snippet}
						</Combobox.Item>
					{:else}
						<div class="px-2 py-4 text-center text-sm text-muted-foreground">
							No countries found
						</div>
					{/each}
				</div>
			</Combobox.Content>
		</Combobox.Portal>
	</div>
</Combobox.Root>
