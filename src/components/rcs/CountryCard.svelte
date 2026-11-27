<script lang="ts">
	import Check from "@lucide/svelte/icons/check";
	import Contrast from "@lucide/svelte/icons/contrast";
	import Minus from "@lucide/svelte/icons/minus";
	import CircleQuestionMark from "@lucide/svelte/icons/circle-question-mark";
	import { HOW_TO, LEVEL_LABEL, checkYourPhone, osVersionLine, supportLevel, verdict, type CountryCoverage, type Level, type Phone, type Sourced } from "#lib/rcs/rcs.js";
	import { requirements } from "#lib/rcs/state.svelte.js";

	interface Props {
		row: CountryCoverage;
		phone: Phone;
		isHome: boolean;
		isPerson: boolean;
		ontoggleperson: () => void;
	}

	let { row, phone, isHome, isPerson, ontoggleperson }: Props = $props();

	const ICONS = { yes: Check, partial: Contrast, none: Minus, unknown: CircleQuestionMark };
	const PLATFORMS: Phone[] = ["iphone", "android"];
	const CONFIDENCE = { measured: "Measured", "vendor-claim": "Vendor claim", estimate: "Estimate" };

	const lines = $derived(verdict(row));
	const androidLevel = $derived(supportLevel(row, "android"));
	const iphoneLevel = $derived(supportLevel(row, "iphone"));
	const howTo = $derived(HOW_TO[phone]);
	const check = $derived(checkYourPhone(phone, requirements));
	const osLines = $derived(PLATFORMS.map((platform) => osVersionLine(row, platform, requirements)));

	function host(url: string): string {
		return new URL(url).hostname.replace(/^www\./, "");
	}

	function percent(value: number): string {
		return `${Math.round(value)}%`;
	}
</script>

{#snippet mark(level: Level)}
	{@const Icon = ICONS[level]}
	<span class={["mark", level]}><Icon size={14} strokeWidth={2.5} aria-hidden="true" /></span>
{/snippet}

{#snippet source(entry: Sourced, known: boolean)}
	{#if entry.source_url}
		<span class="source">
			<a href={entry.source_url} target="_blank" rel="noreferrer">{host(entry.source_url)}</a>{#if entry.date}, {entry.date}{/if}
			{#if known && entry.confidence}<span class={["confidence", entry.confidence]}>{CONFIDENCE[entry.confidence]}</span>{/if}
		</span>
	{/if}
{/snippet}

<article class="rounded-2xl border bg-card p-5 text-card-foreground shadow-sm sm:p-6" aria-labelledby="card-{row.iso2}">
	<header class="flex flex-wrap items-center gap-x-3 gap-y-2">
		<h2 id="card-{row.iso2}" class="font-display text-2xl font-bold tracking-tight">{row.name}</h2>
		{#if isHome}<span class="rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium text-muted-foreground">You are here</span>{/if}
		<button type="button" class={["person-toggle", { on: isPerson }]} aria-pressed={isPerson} onclick={ontoggleperson}>
			{isPerson ? "In my people" : "I know people here"}
		</button>
	</header>

	<ul class="mt-4 space-y-1.5">
		{#each lines as line (line.pair)}
			<li class="flex items-start gap-2">
				{@render mark(line.level)}
				<p><strong class="font-semibold">{line.pair}:</strong> {line.text}</p>
			</li>
		{/each}
	</ul>

	<dl class="mt-5 space-y-3 border-t pt-4 text-sm">
		<div>
			<dt class="font-medium">RCS on Android: {LEVEL_LABEL.android[androidLevel]}</dt>
			<dd class="text-muted-foreground">
				{#if row.android.detail}{row.android.detail}{/if}
				{@render source(row.android, androidLevel !== "unknown")}
			</dd>
		</div>
		<div>
			<dt class="font-medium">RCS on iPhone: {LEVEL_LABEL.iphone[iphoneLevel]}</dt>
			<dd class="text-muted-foreground">
				{#if row.iphone.carriers.length > 0}Apple lists {row.iphone.carriers.join(", ")}.{/if}
				{@render source(row.iphone, iphoneLevel !== "unknown")}
			</dd>
		</div>
		<div>
			<dt class="font-medium">Phones here</dt>
			<dd class="text-muted-foreground">
				{#if row.ios_share && row.android_share}
					iPhone {percent(row.ios_share.value)}, Android {percent(row.android_share.value)} of mobile web use.
					{@render source(row.ios_share, true)}
				{:else}
					iPhone and Android share not known.
				{/if}
			</dd>
			{#each osLines as line (line.text)}
				<dd class="text-muted-foreground">
					{line.text}
					{#if line.source}{@render source(line.source, true)}{/if}
				</dd>
			{/each}
			<dd class="text-xs text-muted-foreground">Software versions come from web traffic. They are an OS-version share, not a count of phones that can use RCS.</dd>
		</div>
	</dl>

	{#if row.note}<p class="mt-3 text-sm text-muted-foreground">{row.note}</p>{/if}

	{#if isHome}
		<p class="mt-4 rounded-xl bg-muted p-3 text-sm">
			<strong class="font-semibold">Check your phone.</strong>
			{check.text}
			{#if check.source?.source_url}<a class="underline underline-offset-4" href={check.source.source_url} target="_blank" rel="noreferrer">Source</a>{/if}
		</p>
		<p class="mt-2 rounded-xl bg-muted p-3 text-sm">
			<strong class="font-semibold">Turn RCS on.</strong>
			{howTo.text}
			<a class="underline underline-offset-4" href={howTo.source_url} target="_blank" rel="noreferrer">{phone === "iphone" ? "Apple" : "Google"} help</a>
		</p>
	{/if}
</article>

<style>
	.mark {
		display: inline-grid;
		flex: none;
		place-items: center;
		width: 1.25rem;
		height: 1.25rem;
		margin-top: 0.125rem;
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

	.source {
		display: block;
	}

	.source a {
		text-decoration: underline;
		text-underline-offset: 3px;
	}

	.confidence {
		margin-left: 0.375rem;
		border: 1px solid hsl(var(--border));
		border-radius: 999px;
		padding: 0 0.5rem;
		font-size: 0.75rem;
		color: hsl(var(--foreground));
	}

	.confidence.estimate {
		border-style: dashed;
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
</style>
