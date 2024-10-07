<script lang="ts">
	import { TelInput, normalizedCountries } from 'svelte-tel-input';
		import type {
		DetailedValue,
		E164Number,
		CountryCode,
		TelInputOptions
	} from 'svelte-tel-input/types';
	import { replaceDigitWords } from '$lib/normalize.js';
	
	export let value: E164Number | null; // the number you should usually store & use
	export let country: CountryCode | null = null;
	export let valid: boolean;
	export let detailedValue: DetailedValue | null = null;
	export let options: TelInputOptions;
	
	function handlePaste(event: ClipboardEvent) {
		event.preventDefault();
		const pastedText = event.clipboardData?.getData('text');
		if (pastedText) {
			const replacedText = replaceDigitWords(pastedText);
			const input = event.target as HTMLInputElement;
			const start = input.selectionStart || 0;
			const end = input.selectionEnd || 0;
			const newValue = input.value.slice(0, start) + replacedText + input.value.slice(end);
			input.value = newValue;
			input.setSelectionRange(start + replacedText.length, start + replacedText.length);
			input.dispatchEvent(new Event('input', { bubbles: true }));
		}
	}
	
	</script>
	
	<div class="flex max-w-md">
	<select
	class="form-select appearance-none block px-3 py-1.5 text-base
		 font-normal bg-clip-padding bg-no-repeat cursor-pointer text-gray-500 bg-gray-100 border border-gray-300 rounded-l-lg hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 dark:text-white dark:border-gray-600 m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none" aria-label="Defau ltselect example"
	name="Country"
	bind:value={country}
		>
		<option value={null} hidden={country !== null}>Please select</option>
		{#each normalizedCountries as currentCountry (currentCountry.id)}
	<option
	value={currentCountry.iso2}
	selected={currentCountry.iso2 === country}
	aria-selected={currentCountry.iso2 === country}
		>
		{currentCountry.iso2} (+{currentCountry.dialCode})
	</option>
	{/each}
		</select>
	
	<TelInput
	{options}
	bind:country
	bind:valid
	bind:value
	bind:detailedValue
	on:paste={handlePaste}
	class="px-4 py-1 w-full bg-gray-50 dark:bg-gray-700 dark:placeholder-gray-400 dark:text-white text-gray-900 focus:outline-none rounded-r-lg {valid 
		? 'border border-gray-300 border-l-gray-100 dark:border-l-gray-700 dark:border-gray-600'
		: 'border-2 border-red-600'}"
	/>
	</div>

