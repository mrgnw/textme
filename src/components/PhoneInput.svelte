<script lang="ts">
	import { TelInput } from "svelte-tel-input";
	import type {
		DetailedValue,
		E164Number,
		CountryCode,
		TelInputOptions,
	} from "svelte-tel-input/types";
	import { replaceDigitWords } from "$lib/normalize.js";
	import CountrySelector from "./CountrySelector.svelte";

	interface Props {
		value: E164Number | null;
		country?: CountryCode | null;
		valid: boolean;
		detailedValue?: DetailedValue | null;
		options: TelInputOptions;
	}

	let {
		value = $bindable(),
		country = $bindable(null),
		valid = $bindable(),
		detailedValue = $bindable(null),
		options
	}: Props = $props();

	function handlePaste(event: ClipboardEvent) {
		event.preventDefault();
		const pastedText = event.clipboardData?.getData("text");
		if (pastedText) {
			const replacedText = replaceDigitWords(pastedText);
			const input = event.target as HTMLInputElement;
			const start = input.selectionStart || 0;
			const end = input.selectionEnd || 0;
			const newValue =
				input.value.slice(0, start) + replacedText + input.value.slice(end);
			input.value = newValue;
			input.setSelectionRange(
				start + replacedText.length,
				start + replacedText.length,
			);
			input.dispatchEvent(new Event("input", { bubbles: true }));
		}
	}
</script>

<div class="flex max-w-md gap-2">
	<CountrySelector bind:value={country} />

	<TelInput
		{options}
		bind:country
		bind:valid
		bind:value
		bind:detailedValue
		on:paste={handlePaste}
		class="px-4 py-2 w-full bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring rounded-xl {valid
			? 'border border-input'
			: 'border-2 border-destructive'}"
	/>
</div>
