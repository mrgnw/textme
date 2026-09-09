<script lang="ts">
	import type { Snippet } from "svelte";
	import { TelInput } from "svelte-tel-input";
	import type { CountryCode, DetailedValue } from "svelte-tel-input/types";
	import ClipboardIcon from "@lucide/svelte/icons/clipboard";
	import CopyIcon from "@lucide/svelte/icons/copy";
	import CircleAlertIcon from "@lucide/svelte/icons/circle-alert";
	import { toast } from "svelte-sonner";
	import { Button } from "$lib/components/ui/button";
	import { copyToClipboard } from "$lib/utils";
	import { replaceDigitWords } from "$lib/normalize.js";
	import { isListPaste, type PhoneState } from "$lib/phone";

	interface Props {
		value: string;
		country: CountryCode | null;
		detailedValue: Partial<DetailedValue> | null;
		status: PhoneState;
		kicker: string;
		stamp: Snippet;
		onValueChange: (value: string, details: Partial<DetailedValue> | null) => void;
		onListPaste: (text: string) => void;
		children?: Snippet;
	}

	let {
		value,
		country = $bindable(),
		detailedValue = $bindable(),
		status,
		kicker,
		stamp,
		onValueChange,
		onListPaste,
		children,
	}: Props = $props();

	let el = $state<HTMLInputElement>();
	let touched = $state(false);

	function acceptText(text: string, insertAt: HTMLInputElement | null) {
		const replaced = replaceDigitWords(text);
		if (isListPaste(replaced, country)) {
			onListPaste(replaced);
			return;
		}
		if (!insertAt) {
			onValueChange(replaced, null);
			return;
		}
		const start = insertAt.selectionStart ?? insertAt.value.length;
		const end = insertAt.selectionEnd ?? insertAt.value.length;
		onValueChange(insertAt.value.slice(0, start) + replaced + insertAt.value.slice(end), null);
	}

	function handlePaste(event: ClipboardEvent) {
		const text = event.clipboardData?.getData("text");
		if (!text) return;
		event.preventDefault();
		acceptText(text, event.target as HTMLInputElement);
	}

	async function pasteFromClipboard() {
		try {
			const text = await navigator.clipboard.readText();
			if (!text.trim()) throw new Error("empty clipboard");
			acceptText(text, null);
		} catch {
			el?.focus();
			toast.message("Paste with ⌘V, or long-press the field");
		}
	}
</script>

<div class="space-y-5 p-6">
	<div class="flex items-center justify-between">
		<span class="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{kicker}</span>
		{@render stamp()}
	</div>

	<TelInput
		bind:el
		bind:country
		bind:detailedValue
		{value}
		{onValueChange}
		initialFormat="national"
		options={{ validateOn: "blur" }}
		onpaste={handlePaste}
		onblur={() => (touched = true)}
		aria-label="Phone number"
		class="w-full bg-transparent p-0 font-display text-4xl font-bold tracking-tight tabular-nums text-foreground placeholder:text-muted-foreground/50 focus:outline-none"
	/>

	{#if status === "invalid" && touched}
		<p class="flex items-center gap-1.5 text-sm text-destructive" role="alert">
			<CircleAlertIcon class="size-4 shrink-0" />
			Not a valid number for this country. Check the country code.
		</p>
	{/if}

	{#if status === "empty"}
		<Button size="lg" class="h-12 w-full rounded-full text-base [&_svg]:size-5" onclick={pasteFromClipboard}>
			<ClipboardIcon />
			Paste number
		</Button>
		<p class="text-center text-sm text-muted-foreground">or type it · paste a whole list to save them all</p>
	{/if}

	{#if status === "valid" && detailedValue?.e164}
		<div class="-my-1 flex items-center gap-1 text-sm text-muted-foreground">
			<span class="tabular-nums">{detailedValue.formatInternational}</span>
			<Button
				variant="ghost"
				size="icon"
				class="h-8 w-8"
				aria-label="Copy {detailedValue.formatInternational}"
				onclick={() => copyToClipboard(detailedValue?.e164 ?? "")}
			>
				<CopyIcon />
			</Button>
		</div>
	{/if}

	{@render children?.()}
</div>
