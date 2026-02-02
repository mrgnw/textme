<script lang="ts">
	import { Dialog } from "bits-ui";
	import { Search, X, ChevronDown, Check } from "lucide-svelte";
	import { normalizedCountries } from "svelte-tel-input";
	import type { CountryCode } from "svelte-tel-input/types";

	interface Props {
		value?: CountryCode | null;
	}

	let { value = $bindable() }: Props = $props();

	let open = $state(false);
	let searchQuery = $state("");

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
		searchQuery
			? normalizedCountries.filter((c) =>
					c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
					c.iso2.toLowerCase().includes(searchQuery.toLowerCase()) ||
					String(c.dialCode).includes(searchQuery)
				)
			: normalizedCountries
	);

	let selectedCountry = $derived(
		normalizedCountries.find((c) => c.iso2 === value)
	);

	function handleSelect(iso2: CountryCode) {
		value = iso2;
		searchQuery = "";
		open = false;
	}
</script>

<Dialog.Root bind:open onOpenChange={(o) => { if (!o) searchQuery = ""; }}>
	<Dialog.Trigger
		class="flex h-10 items-center gap-2 rounded-xl border border-input bg-background px-3 py-2 text-sm hover:bg-accent/50 transition-colors"
	>
		{#if selectedCountry}
			<span class="text-lg">{getFlag(selectedCountry.iso2)}</span>
			<span>{selectedCountry.iso2}</span>
			<span class="text-muted-foreground">+{selectedCountry.dialCode}</span>
		{:else}
			<span class="text-muted-foreground">Select country</span>
		{/if}
		<ChevronDown class="h-4 w-4 ml-auto text-muted-foreground" />
	</Dialog.Trigger>

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
