<script lang="ts">
	import { page } from "$app/state";
	import { replaceState } from "$app/navigation";
	import { useDebounce } from "runed";
	import { parse, getCountryByIso2 } from "svelte-tel-input/utils";
	import type { CountryCode, DetailedValue } from "svelte-tel-input/types";
	import { Sheet } from "$lib/components/ui/sheet";
	import { flushSync } from "svelte";
	import { isMobile } from "$lib/media.svelte";
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
	const sideQr = $derived(qrApp !== null && e164 !== null && !isMobile.current);

	function setQr(next: Channel | null) {
		if (isMobile.current || !document.startViewTransition) {
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
	<header class="flex h-14 shrink-0 items-center justify-center">
		<a href="/" class="font-display text-lg font-bold tracking-tight">text<span class="text-primary">me</span></a>
	</header>

	<main class="mx-auto w-full {mode === 'list' ? 'max-w-xl' : sideQr ? 'max-w-[47rem]' : 'max-w-md'} px-4 pb-6 pt-1 sm:px-6 sm:pt-8">
		{#if mode === "list"}
			<ListEditor bind:text={listText} bind:country {countryLabel} onclear={clearList} />
		{:else}
			<div class="relative flex items-start gap-4">
				<div class="min-w-0 flex-1 rounded-2xl border bg-card text-card-foreground shadow-sm [view-transition-name:number-card]">
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
			{#if sideQr && qrApp && e164}
				<aside class="w-72 shrink-0 [view-transition-name:qr-card]" style:anchor-name="--qr-aside">
					{#key qrApp}
						<QrPanel {e164} channel={qrApp} />
					{/key}
				</aside>
				<div class="notch size-4 rotate-45 rounded-sm {CHANNELS[qrApp].fill} [view-transition-name:qr-notch]" aria-hidden="true"></div>
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
	{#if isMobile.current}
		<Sheet open={qrApp !== null} onOpenChange={(o) => { if (!o) qrApp = null; }} title={qrApp ? CHANNELS[qrApp].label : "QR code"}>
			{#if qrApp}
				<div class="px-4 pb-8 pt-4">
					{#key qrApp}
						<QrPanel {e164} channel={qrApp} />
					{/key}
				</div>
			{/if}
		</Sheet>
	{/if}
{/if}

<style>
	.notch {
		position: absolute;
		left: anchor(--qr-aside left);
		top: anchor(--qr-row center);
		translate: -50% -50%;
	}

	@supports not (anchor-name: --a) {
		.notch {
			display: none;
		}
	}
</style>
