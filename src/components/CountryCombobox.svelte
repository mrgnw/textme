<script lang="ts">
	import { Combobox } from "bits-ui";
	import { cn } from "$lib/utils.js";
	import { ChevronDown, Check } from "lucide-svelte";
	import { normalizedCountries } from "svelte-tel-input";
	import type { CountryCode } from "svelte-tel-input/types";

	interface Props {
		value?: CountryCode | null;
		class?: string;
	}

	let { value = $bindable(), class: className }: Props = $props();

	let searchValue = $state("");
	let open = $state(false);

	const countryFlags: Record<string, string> = {
		AF: "🇦🇫", AL: "🇦🇱", DZ: "🇩🇿", AS: "🇦🇸", AD: "🇦🇩", AO: "🇦🇴", AI: "🇦🇮", AG: "🇦🇬",
		AR: "🇦🇷", AM: "🇦🇲", AW: "🇦🇼", AU: "🇦🇺", AT: "🇦🇹", AZ: "🇦🇿", BS: "🇧🇸", BH: "🇧🇭",
		BD: "🇧🇩", BB: "🇧🇧", BY: "🇧🇾", BE: "🇧🇪", BZ: "🇧🇿", BJ: "🇧🇯", BM: "🇧🇲", BT: "🇧🇹",
		BO: "🇧🇴", BA: "🇧🇦", BW: "🇧🇼", BR: "🇧🇷", BN: "🇧🇳", BG: "🇧🇬", BF: "🇧🇫", BI: "🇧🇮",
		KH: "🇰🇭", CM: "🇨🇲", CA: "🇨🇦", CV: "🇨🇻", KY: "🇰🇾", CF: "🇨🇫", TD: "🇹🇩", CL: "🇨🇱",
		CN: "🇨🇳", CO: "🇨🇴", KM: "🇰🇲", CG: "🇨🇬", CD: "🇨🇩", CK: "🇨🇰", CR: "🇨🇷", CI: "🇨🇮",
		HR: "🇭🇷", CU: "🇨🇺", CY: "🇨🇾", CZ: "🇨🇿", DK: "🇩🇰", DJ: "🇩🇯", DM: "🇩🇲", DO: "🇩🇴",
		EC: "🇪🇨", EG: "🇪🇬", SV: "🇸🇻", GQ: "🇬🇶", ER: "🇪🇷", EE: "🇪🇪", ET: "🇪🇹", FK: "🇫🇰",
		FO: "🇫🇴", FJ: "🇫🇯", FI: "🇫🇮", FR: "🇫🇷", GF: "🇬🇫", PF: "🇵🇫", GA: "🇬🇦", GM: "🇬🇲",
		GE: "🇬🇪", DE: "🇩🇪", GH: "🇬🇭", GI: "🇬🇮", GR: "🇬🇷", GL: "🇬🇱", GD: "🇬🇩", GP: "🇬🇵",
		GU: "🇬🇺", GT: "🇬🇹", GN: "🇬🇳", GW: "🇬🇼", GY: "🇬🇾", HT: "🇭🇹", HN: "🇭🇳", HK: "🇭🇰",
		HU: "🇭🇺", IS: "🇮🇸", IN: "🇮🇳", ID: "🇮🇩", IR: "🇮🇷", IQ: "🇮🇶", IE: "🇮🇪", IL: "🇮🇱",
		IT: "🇮🇹", JM: "🇯🇲", JP: "🇯🇵", JO: "🇯🇴", KZ: "🇰🇿", KE: "🇰🇪", KI: "🇰🇮", KP: "🇰🇵",
		KR: "🇰🇷", KW: "🇰🇼", KG: "🇰🇬", LA: "🇱🇦", LV: "🇱🇻", LB: "🇱🇧", LS: "🇱🇸", LR: "🇱🇷",
		LY: "🇱🇾", LI: "🇱🇮", LT: "🇱🇹", LU: "🇱🇺", MO: "🇲🇴", MK: "🇲🇰", MG: "🇲🇬", MW: "🇲🇼",
		MY: "🇲🇾", MV: "🇲🇻", ML: "🇲🇱", MT: "🇲🇹", MH: "🇲🇭", MQ: "🇲🇶", MR: "🇲🇷", MU: "🇲🇺",
		YT: "🇾🇹", MX: "🇲🇽", FM: "🇫🇲", MD: "🇲🇩", MC: "🇲🇨", MN: "🇲🇳", ME: "🇲🇪", MS: "🇲🇸",
		MA: "🇲🇦", MZ: "🇲🇿", MM: "🇲🇲", NA: "🇳🇦", NR: "🇳🇷", NP: "🇳🇵", NL: "🇳🇱", NC: "🇳🇨",
		NZ: "🇳🇿", NI: "🇳🇮", NE: "🇳🇪", NG: "🇳🇬", NU: "🇳🇺", NF: "🇳🇫", MP: "🇲🇵", NO: "🇳🇴",
		OM: "🇴🇲", PK: "🇵🇰", PW: "🇵🇼", PS: "🇵🇸", PA: "🇵🇦", PG: "🇵🇬", PY: "🇵🇾", PE: "🇵🇪",
		PH: "🇵🇭", PL: "🇵🇱", PT: "🇵🇹", PR: "🇵🇷", QA: "🇶🇦", RE: "🇷🇪", RO: "🇷🇴", RU: "🇷🇺",
		RW: "🇷🇼", KN: "🇰🇳", LC: "🇱🇨", PM: "🇵🇲", VC: "🇻🇨", WS: "🇼🇸", SM: "🇸🇲", ST: "🇸🇹",
		SA: "🇸🇦", SN: "🇸🇳", RS: "🇷🇸", SC: "🇸🇨", SL: "🇸🇱", SG: "🇸🇬", SK: "🇸🇰", SI: "🇸🇮",
		SB: "🇸🇧", SO: "🇸🇴", ZA: "🇿🇦", SS: "🇸🇸", ES: "🇪🇸", LK: "🇱🇰", SD: "🇸🇩", SR: "🇸🇷",
		SZ: "🇸🇿", SE: "🇸🇪", CH: "🇨🇭", SY: "🇸🇾", TW: "🇹🇼", TJ: "🇹🇯", TZ: "🇹🇿", TH: "🇹🇭",
		TL: "🇹🇱", TG: "🇹🇬", TK: "🇹🇰", TO: "🇹🇴", TT: "🇹🇹", TN: "🇹🇳", TR: "🇹🇷", TM: "🇹🇲",
		TC: "🇹🇨", TV: "🇹🇻", UG: "🇺🇬", UA: "🇺🇦", AE: "🇦🇪", GB: "🇬🇧", US: "🇺🇸", UY: "🇺🇾",
		UZ: "🇺🇿", VU: "🇻🇺", VA: "🇻🇦", VE: "🇻🇪", VN: "🇻🇳", VG: "🇻🇬", VI: "🇻🇮", WF: "🇼🇫",
		EH: "🇪🇭", YE: "🇾🇪", ZM: "🇿🇲", ZW: "🇿🇼", XK: "🇽🇰"
	};

	function getFlag(iso2: string): string {
		return countryFlags[iso2] || "🏳️";
	}

	let filteredCountries = $derived(
		searchValue
			? normalizedCountries.filter((c) =>
					c.name.toLowerCase().includes(searchValue.toLowerCase()) ||
					c.iso2.toLowerCase().includes(searchValue.toLowerCase()) ||
					String(c.dialCode).includes(searchValue)
				)
			: normalizedCountries
	);

	let selectedCountry = $derived(
		normalizedCountries.find((c) => c.iso2 === value)
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
		<Combobox.Input
			oninput={(e) => (searchValue = e.currentTarget.value)}
			placeholder={selectedCountry
				? `${getFlag(selectedCountry.iso2)} ${selectedCountry.iso2} (+${selectedCountry.dialCode})`
				: "Select country..."}
			class="flex h-10 w-full rounded-xl border border-input bg-background px-3 py-2 pr-8 text-sm ring-offset-background placeholder:text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
		/>
		<Combobox.Trigger
			class="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground"
		>
			<ChevronDown class="h-4 w-4" />
		</Combobox.Trigger>
	</div>

	<Combobox.Portal>
		<Combobox.Content
			class="z-50 max-h-60 min-w-[var(--bits-combobox-anchor-width)] overflow-y-auto rounded-xl border bg-popover p-1 text-popover-foreground shadow-lg"
			sideOffset={8}
		>
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
		</Combobox.Content>
	</Combobox.Portal>
</Combobox.Root>
