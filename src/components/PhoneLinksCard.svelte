<script lang="ts">
	import { page } from "$app/state";
	import { replaceState } from "$app/navigation";
	import { useDebounce } from "runed";
	import { parse, getCountryByIso2 } from "svelte-tel-input/utils";
	import type { CountryCode, DetailedValue } from "svelte-tel-input/types";
	import { Popover } from "bits-ui";
	import { Sheet } from "$lib/components/ui/sheet";
	import { flushSync } from "svelte";
	import { isWide } from "$lib/media.svelte";
	import { CHANNELS, type Channel } from "$lib/channels";
	import { classify, digitsOf, resolveInitial } from "$lib/phone";
	import { remember } from "$lib/recent.svelte";
	import ActionButtons from "./ActionButtons.svelte";
	import CountryStamp from "./CountryStamp.svelte";
	import ListEditor from "./ListEditor.svelte";
	import NumberCard from "./NumberCard.svelte";
	import QrPanel from "./QrPanel.svelte";
	import RecentNumbers from "./RecentNumbers.svelte";
	import SecondaryActions from "./SecondaryActions.svelte";
	import ShareDialog from "./ShareDialog.svelte";

	interface Props {
		initialValue?: string | null;
		initialName?: string;
		mode?: "single" | "list";
	}

	let { initialValue = null, initialName = "", mode: initialMode = "single" }: Props = $props();

	const geoCountry = ((page.data.ip_country as string | undefined)?.toUpperCase() as CountryCode) || "US";
	// svelte-ignore state_referenced_locally
	const initial = resolveInitial(initialValue, geoCountry);

	let country = $state<CountryCode | null>(initial.country);
	let value = $state(initial.value);
	let detailedValue = $state<Partial<DetailedValue> | null>(null);
	// svelte-ignore state_referenced_locally
	let mode = $state(initialMode);
	let listText = $state("");
	// svelte-ignore state_referenced_locally
	let name = $state(initialName);
	let qrApp = $state<Channel | null>(null);
	let shareOpen = $state(false);

	const classified = $derived(classify(value, country));
	const e164 = $derived(classified.state === "valid" ? (classified.detail?.e164 ?? null) : null);
	const landing = $derived(initialName !== "");
	const sideQr = $derived(qrApp !== null && e164 !== null && isWide.current);

	function setQr(next: Channel | null) {
		if (!isWide.current || !document.startViewTransition) {
			qrApp = next;
			return;
		}
		document.startViewTransition(() => {
			qrApp = next;
			flushSync();
		});
	}

	function toggleQr(channel: Channel) {
		setQr(qrApp === channel ? null : channel);
	}
	const dialCode = $derived(country ? getCountryByIso2(country)?.dialCode : undefined);
	const countryLabel = $derived(dialCode ? `+${dialCode}` : "");

	const syncUrl = useDebounce(() => {
		if (!e164) return;
		const path = `/${digitsOf(e164)}`;
		if (page.url.pathname === path) return;
		replaceState(path, page.state);
		remember(e164, "");
	}, 500);

	function onValueChange(next: string, details: Partial<DetailedValue> | null) {
		value = next;
		qrApp = null;
		if (details) detailedValue = details;
		syncUrl();
	}

	function pickRecent(picked: string) {
		const detail = parse(picked, country);
		if (detail.countryCode) country = detail.countryCode;
		onValueChange(picked, detail);
	}

	function enterList(text: string) {
		listText = text;
		mode = "list";
	}

	function clearList() {
		listText = "";
		mode = "single";
	}
</script>

<div class="flex min-h-svh flex-col">
	<header class="flex h-24 shrink-0 items-center justify-center sm:h-28">
		<a href="/" class="font-display text-4xl font-bold tracking-tight sm:text-5xl">text<span class="text-primary">me</span></a>
	</header>

	<main class="mx-auto w-full {mode === 'list' ? 'max-w-xl' : 'max-w-md'} px-4 pb-6 pt-1 sm:px-6 sm:pt-8">
		{#if mode === "list"}
			<ListEditor bind:text={listText} bind:country {countryLabel} onclear={clearList} />
		{:else}
			<div class="rounded-2xl border bg-card text-card-foreground shadow-sm">
				{#if landing && e164}
					<div class="space-y-5 p-6">
						<div class="flex items-start justify-between">
							<div class="flex h-12 w-12 items-center justify-center rounded-full bg-primary font-display text-xl font-bold text-primary-foreground">
								{initialName[0].toUpperCase()}
							</div>
							<CountryStamp bind:country />
						</div>
						<h1 class="font-display text-3xl font-bold tracking-tight">{initialName}</h1>
						<ActionButtons {e164} showing={qrApp} onqr={toggleQr} />
						<SecondaryActions {e164} bind:name onshare={() => (shareOpen = true)} />
					</div>
				{:else}
					<NumberCard
						{value}
						bind:country
						bind:detailedValue
						status={classified.state}
						kicker={initialValue && !landing ? "Shared number" : "Phone number"}
						{onValueChange}
						onListPaste={enterList}
					>
						{#if classified.state !== "empty"}
							<ActionButtons {e164} showing={qrApp} onqr={toggleQr} />
							<SecondaryActions {e164} bind:name onshare={() => (shareOpen = true)} />
						{/if}
					</NumberCard>
				{/if}
			</div>

			{#if classified.state === "empty"}
				<RecentNumbers onpick={pickRecent} />
			{/if}

			{#if initialValue}
				<p class="pt-6 text-center text-sm text-muted-foreground">
					Shared with textme · <a href="/" class="font-medium text-foreground underline underline-offset-4">Make your own link</a>
				</p>
			{/if}
		{/if}
	</main>
</div>

{#if e164}
	<ShareDialog bind:open={shareOpen} {e164} bind:name />
	{#if !isWide.current}
		<Sheet bare open={qrApp !== null} onOpenChange={(o) => { if (!o) qrApp = null; }} title={qrApp ? `${CHANNELS[qrApp].label} QR code` : "QR code"}>
			{#if qrApp}
				{#key qrApp}
					<QrPanel {e164} channel={qrApp} class="rounded-b-none pb-10 pt-6 shadow-none" />
				{/key}
			{/if}
		</Sheet>
	{:else}
		<Popover.Root bind:open={() => sideQr, (o) => { if (!o) setQr(null); }}>
			<Popover.Portal>
				<Popover.Content
					customAnchor={qrApp ? `[data-qr-row="${qrApp}"]` : null}
					side="right"
					sideOffset={12}
					collisionPadding={16}
					trapFocus={false}
					onOpenAutoFocus={(e) => e.preventDefault()}
					onCloseAutoFocus={(e) => e.preventDefault()}
					onInteractOutside={(e) => { if ((e.target as Element | null)?.closest("[data-qr-segment]")) e.preventDefault(); }}
					onFocusOutside={(e) => { if ((e.target as Element | null)?.closest("[data-qr-segment]")) e.preventDefault(); }}
					class="z-50 w-72 outline-none [view-transition-name:qr-card]"
				>
					{#if qrApp}
						{#key qrApp}
							<QrPanel {e164} channel={qrApp} />
						{/key}
						<Popover.Arrow width={20} height={10} class={CHANNELS[qrApp].color} />
					{/if}
				</Popover.Content>
			</Popover.Portal>
		</Popover.Root>
	{/if}
{/if}
