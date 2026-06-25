<script lang="ts">
	import { TelInput } from "svelte-tel-input";
	import type {
		DetailedValue,
		CountryCode,
		TelInputOptions,
	} from "svelte-tel-input/types";
	import { replaceDigitWords } from "$lib/normalize.js";
	import { getFlag } from "$lib/countryFlags.js";
	import CountrySelector from "./CountrySelector.svelte";

	interface Props {
		value: string | null;
		country?: CountryCode | null;
		valid: boolean;
		detailedValue?: Partial<DetailedValue> | null;
		options: TelInputOptions;
	}

	let {
		value = $bindable(""),
		country = $bindable(null),
		valid = $bindable(),
		detailedValue = $bindable(null),
		options
	}: Props = $props();

	let countryPickerOpen = $state(false);

	let flag = $derived(country ? getFlag(country) : "🌐");

	function handlePaste(event: ClipboardEvent) {
		const pastedText = event.clipboardData?.getData("text");
		if (!pastedText) return;
		event.preventDefault();
		const replacedText = replaceDigitWords(pastedText);
		const input = event.target as HTMLInputElement;
		const start = input.selectionStart ?? input.value.length;
		const end = input.selectionEnd ?? input.value.length;
		value = input.value.slice(0, start) + replacedText + input.value.slice(end);
	}
</script>

<div class="relative w-full max-w-md">
	<div class="phone-input-container relative rounded-2xl border-2 border-input bg-background
				shadow-sm hover:shadow-md transition-all
				focus-within:border-[hsl(var(--coral))]
				focus-within:ring-2 focus-within:ring-[hsl(var(--coral))]/20
				{valid ? '' : 'border-destructive focus-within:border-destructive focus-within:ring-destructive/20'}">

		<button
			type="button"
			class="absolute left-4 top-1/2 -translate-y-1/2 z-10
				   text-2xl p-1 rounded-lg hover:bg-accent/50
				   hover:scale-110 transition-all cursor-pointer"
			onclick={() => countryPickerOpen = true}
			aria-label="Change country"
		>
			{flag}
		</button>

		<TelInput
			{options}
			initialFormat="national"
			bind:country
			value={value ?? ""}
			onValueChange={(newValue) => (value = newValue)}
			bind:valid
			bind:detailedValue
			onpaste={handlePaste}
			class="w-full pl-16 pr-4 py-4 text-2xl sm:text-3xl
				   bg-transparent focus:outline-none rounded-2xl"
		/>
	</div>

	<CountrySelector bind:value={country} bind:open={countryPickerOpen} />
</div>
