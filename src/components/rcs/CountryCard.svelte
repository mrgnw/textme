<script lang="ts">
	import Check from "@lucide/svelte/icons/check";
	import Contrast from "@lucide/svelte/icons/contrast";
	import Minus from "@lucide/svelte/icons/minus";
	import CircleQuestionMark from "@lucide/svelte/icons/circle-question-mark";
	import ChevronRight from "@lucide/svelte/icons/chevron-right";
	import type { Snippet } from "svelte";
	import {
		HOW_TO,
		OTHER_CARRIER,
		checkYourPhone,
		hasCarrierList,
		supportLevel,
		verdict,
		type CountryCoverage,
		type Level,
		type Phone,
		type Sourced
	} from "#lib/rcs/rcs.js";
	import { formatShare, thresholdShare } from "#lib/rcs/versions.js";
	import { carrierFor, minimum, requirements, setCarrier, versions, versionsOf } from "#lib/rcs/state.svelte.js";
	import VersionBars from "./VersionBars.svelte";

	interface Props {
		row: CountryCoverage;
		phone: Phone;
		isHome: boolean;
		isPerson: boolean;
		ontoggleperson: () => void;
	}

	let { row, phone, isHome, isPerson, ontoggleperson }: Props = $props();

	const ICONS = { yes: Check, partial: Contrast, none: Minus, unknown: CircleQuestionMark };
	const CONFIDENCE = { measured: "Measured", "vendor-claim": "Vendor claim", estimate: "Estimate" };

	const carrier = $derived(carrierFor(row.iso2));
	const lines = $derived(verdict(row, carrier));
	const androidLevel = $derived(supportLevel(row, "android"));
	const iphoneLevel = $derived(supportLevel(row, "iphone"));
	const showCarrier = $derived(phone === "iphone" && hasCarrierList(row));
	const howTo = $derived(HOW_TO[phone]);
	const check = $derived(checkYourPhone(phone, requirements));
	const excluded = $derived(requirements.iphone_excluded);
	const rowVersions = $derived(versionsOf(row.iso2));
	const iosReady = $derived(thresholdShare(rowVersions?.ios ?? null, minimum.iphone));
	const androidReady = $derived(thresholdShare(rowVersions?.android ?? null, minimum.android));

	function host(url: string): string {
		return new URL(url).hostname.replace(/^www\./, "");
	}

	function percent(value: number): string {
		return `${Math.round(value)}%`;
	}

	function readyLine(): string {
		if (versions.status === "loading") return "Loading";
		if (versions.status === "error") return "Did not load";
		const parts = [
			iosReady === null ? null : `iOS ${minimum.iphone}+ ${formatShare(iosReady)}`,
			androidReady === null ? null : `Android ${minimum.android}+ ${formatShare(androidReady)}`
		].filter((part) => part !== null);
		return parts.length > 0 ? parts.join(" · ") : "No data yet";
	}
</script>

{#snippet mark(level: Level)}
	{@const Icon = ICONS[level]}
	<span class={["mark", level]}><Icon size={14} strokeWidth={2.5} aria-hidden="true" /></span>
{/snippet}

{#snippet source(entry: Sourced, known: boolean)}
	{#if entry.source_url}
		<p class="source">
			<a href={entry.source_url} target="_blank" rel="noreferrer">{host(entry.source_url)}</a>{#if entry.date}, {entry.date}{/if}{#if known && entry.confidence}{` · ${CONFIDENCE[entry.confidence]}`}{/if}
		</p>
	{/if}
{/snippet}

{#snippet fact(label: string, value: string, level: Level | null, body: Snippet)}
	<details class="fact">
		<summary>
			{#if level}{@render mark(level)}{:else}<span class="mark-space"></span>{/if}
			<span class="fact-text"><span class="fact-label">{label}</span> <span class="fact-value">{value}</span></span>
			<ChevronRight class="chevron" size={16} aria-hidden="true" />
		</summary>
		<div class="fact-body">{@render body()}</div>
	</details>
{/snippet}

{#snippet carrierPicker()}
	<label class="carrier">
		<span class="text-sm font-medium">{isHome ? "Your carrier" : `Carrier in ${row.name}`}</span>
		<select
			class="h-10 w-full min-w-0 rounded-lg border border-input bg-card px-3 text-base"
			value={carrier}
			onchange={(event) => setCarrier(row.iso2, event.currentTarget.value)}
		>
			<option value="">I don't know</option>
			{#each row.iphone.carriers as name (name)}
				<option value={name}>{name}</option>
			{/each}
			<option value={OTHER_CARRIER}>Another carrier</option>
		</select>
	</label>
{/snippet}

{#snippet androidBody()}
	{#if row.android.detail}<p>{row.android.detail}</p>{/if}
	{@render source(row.android, androidLevel !== "unknown")}
{/snippet}

{#snippet iphoneBody()}
	{#if hasCarrierList(row)}
		<details class="nested">
			<summary>{row.iphone.carriers.length} listed {row.iphone.carriers.length === 1 ? "carrier" : "carriers"}</summary>
			<ul class="chips">
				{#each row.iphone.carriers as name (name)}
					<li class={{ chosen: name === carrier }}>{name}</li>
				{/each}
			</ul>
		</details>
	{/if}
	<details class="nested">
		<summary>iPhones that cannot use RCS</summary>
		<p>Models that cannot run iOS {excluded.major_version}:</p>
		<ul class="chips">
			{#each excluded.excluded_models as model (model)}
				<li>{model}</li>
			{/each}
		</ul>
		{@render source(excluded, true)}
	</details>
	{@render source(row.iphone, iphoneLevel !== "unknown")}
{/snippet}

{#snippet sharesBody()}
	<p>Share of mobile web traffic.</p>
	{#if row.ios_share}{@render source(row.ios_share, true)}{/if}
{/snippet}

{#snippet versionsBody()}
	{#if versions.status === "ready"}
		<VersionBars phone="iphone" versions={rowVersions?.ios ?? null} estimate={rowVersions?.estimate?.ios ?? null} minimum={minimum.iphone} />
		<VersionBars phone="android" versions={rowVersions?.android ?? null} estimate={rowVersions?.estimate?.android ?? null} minimum={minimum.android} />
		<p>Shares of web traffic on each version, not counts of phones that can use RCS.</p>
	{/if}
{/snippet}

{#snippet turnOnBody()}
	<p>{howTo.text}</p>
	<p class="source"><a href={howTo.source_url} target="_blank" rel="noreferrer">{phone === "iphone" ? "Apple" : "Google"} help</a></p>
{/snippet}

{#snippet checkBody()}
	<p>{check.text}</p>
	{#if check.source}{@render source(check.source, true)}{/if}
{/snippet}

<article class="rounded-2xl border bg-card p-5 text-card-foreground shadow-sm sm:p-6" aria-labelledby="card-{row.iso2}">
	<header class="flex flex-wrap items-center gap-x-3 gap-y-2">
		<h2 id="card-{row.iso2}" class="font-display text-2xl font-bold tracking-tight">{row.name}</h2>
		{#if isHome}<span class="rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium text-muted-foreground">You are here</span>{/if}
		<button type="button" class={["person-toggle", { on: isPerson }]} aria-pressed={isPerson} onclick={ontoggleperson}>
			{isPerson ? "In my people" : "I know people here"}
		</button>
	</header>

	{#if showCarrier && isHome}{@render carrierPicker()}{/if}

	<div class="facts">
		{@render fact(lines[0].pair, lines[0].text, lines[0].level, androidBody)}
		{@render fact(lines[1].pair, lines[1].text, lines[1].level, iphoneBody)}
		{#if showCarrier && !isHome}{@render carrierPicker()}{/if}
		{#if isHome}
			{@render fact("Turn on", phone === "iphone" ? "Settings › Apps › Messages" : "Google Messages settings", null, turnOnBody)}
			{@render fact("Needs", check.summary, null, checkBody)}
		{/if}
		{@render fact(
			"Phones here",
			row.ios_share && row.android_share ? `iPhone ${percent(row.ios_share.value)} · Android ${percent(row.android_share.value)}` : "No data yet",
			null,
			sharesBody
		)}
		{@render fact("Recent OS", readyLine(), null, versionsBody)}
	</div>

	{#if row.note}<p class="mt-3 text-sm text-muted-foreground">{row.note}</p>{/if}
</article>

<style>
	.facts {
		margin-top: 1rem;
		border-top: 1px solid hsl(var(--border));
	}

	.fact {
		border-bottom: 1px solid hsl(var(--border));
	}

	.fact > summary {
		display: grid;
		grid-template-columns: 1.25rem 1fr 1rem;
		align-items: center;
		gap: 0.625rem;
		min-height: 2.75rem;
		padding: 0.375rem 0;
		cursor: pointer;
		list-style: none;
	}

	.fact > summary::-webkit-details-marker {
		display: none;
	}

	.fact > summary:focus-visible {
		outline: 2px solid hsl(var(--ring));
		outline-offset: 2px;
		border-radius: 0.375rem;
	}

	.fact-text {
		display: grid;
		min-width: 0;
	}

	.fact-label {
		font-weight: 600;
	}

	.fact-value {
		color: hsl(var(--muted-foreground));
	}

	.fact :global(.chevron) {
		color: hsl(var(--muted-foreground));
		transition: rotate 150ms ease;
	}

	.fact[open] > summary :global(.chevron) {
		rotate: 90deg;
	}

	.fact-body {
		display: grid;
		gap: 0.5rem;
		padding: 0 0 0.875rem 1.875rem;
		font-size: 0.875rem;
		color: hsl(var(--muted-foreground));
	}

	.nested > summary {
		cursor: pointer;
		color: hsl(var(--foreground));
	}

	.nested[open] > summary {
		margin-bottom: 0.375rem;
	}

	.chips {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem 0.375rem;
	}

	.chips li {
		border: 1px solid hsl(var(--border));
		border-radius: 999px;
		padding: 0.0625rem 0.5rem;
		font-size: 0.8125rem;
	}

	.chips li.chosen {
		border-color: hsl(var(--primary));
		color: hsl(var(--foreground));
		font-weight: 600;
	}

	.source {
		font-size: 0.75rem;
	}

	.source a {
		text-decoration: underline;
		text-underline-offset: 3px;
	}

	.carrier {
		display: grid;
		gap: 0.25rem;
		margin-block: 1rem 0.75rem;
	}

	.mark,
	.mark-space {
		display: inline-grid;
		place-items: center;
		width: 1.25rem;
		height: 1.25rem;
		border-radius: 999px;
	}

	.mark.yes {
		background: hsl(var(--primary));
		color: hsl(var(--primary-foreground));
	}

	.mark.partial {
		background: hsl(var(--primary) / 0.2);
		color: hsl(var(--primary));
	}

	.mark.none,
	.mark.unknown {
		background: hsl(var(--muted));
		color: hsl(var(--muted-foreground));
	}

	.person-toggle {
		min-height: 2.25rem;
		border: 1.5px solid var(--rcs-people, oklch(0.7 0.17 50));
		border-radius: 999px;
		padding: 0 0.875rem;
		font-size: 0.875rem;
		font-weight: 500;
		transition: background-color 150ms ease;
	}

	.person-toggle.on {
		background: oklch(0.7 0.17 50 / 0.18);
	}

	@media (prefers-reduced-motion: reduce) {
		.fact :global(.chevron) {
			transition: none;
		}
	}
</style>
