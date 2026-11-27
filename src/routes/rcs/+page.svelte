<script lang="ts">
	import { page } from "$app/state";
	import X from "@lucide/svelte/icons/x";
	import Globe from "#components/rcs/Globe.svelte";
	import CountryCard from "#components/rcs/CountryCard.svelte";
	import { LEVEL_LABEL, peopleSummary, supportLevel, summaryLine, type Phone } from "#lib/rcs/rcs.js";
	import { asOf, byIso, hasPerson, loadVersions, minimum, people, phone, rows, togglePerson, versions, versionsOf } from "#lib/rcs/state.svelte.js";
	import { THRESHOLD_CHOICES, binLabels, shareBin, thresholdShare } from "#lib/rcs/versions.js";

	const ipCountry = ((page.data.ip_country as string | undefined) ?? "").toUpperCase();
	const isoByNumeric = new Map(rows.map((row) => [row.n, row.iso2]));

	const start = byIso.has(ipCountry) ? ipCountry : null;

	let home = $state(start);
	let selected = $state(start);
	let flat = $state(false);
	let globe = $state<Globe>();
	let layer = $state<"status" | Phone>("status");
	let thresholds = $state({ ...minimum });

	const LEVELS = ["yes", "partial", "none", "unknown"] as const;
	const OS_KEY = { iphone: "ios", android: "android" } as const;
	const LAYER_NAME = { iphone: "iPhones on iOS", android: "Android phones on Android" } as const;

	loadVersions();

	const selectedRow = $derived(selected ? byIso.get(selected) : undefined);
	const peopleRows = $derived(people.current.map((iso2) => byIso.get(iso2)).filter((row) => row !== undefined));
	const summary = $derived(summaryLine(peopleSummary(peopleRows)));
	const legend = $derived(
		layer === "status"
			? LEVELS.map((level) => ({ cls: level, label: LEVEL_LABEL[phone.current][level] }))
			: [
					...binLabels().map(({ bin, label }) => ({ cls: bin, label })),
					{ cls: "unknown", label: versions.status === "loading" ? "Loading" : "No version data yet" }
				]
	);

	function shareFor(iso2: string, platform: Phone): number | null {
		return thresholdShare(versionsOf(iso2)?.[OS_KEY[platform]] ?? null, thresholds[platform]);
	}

	function classOf(iso2: string): string {
		const row = byIso.get(iso2);
		if (!row) return "unknown";
		if (layer === "status") return supportLevel(row, phone.current);
		return shareBin(shareFor(iso2, layer));
	}

	function nameOf(iso2: string): string {
		const row = byIso.get(iso2);
		if (!row) return iso2;
		if (layer === "status") return `${row.name}: ${LEVEL_LABEL[phone.current][supportLevel(row, phone.current)]}`;
		const share = shareFor(iso2, layer);
		if (share === null) return `${row.name}: no version data yet`;
		return `${row.name}: ${Math.round(share)}% of sampled web traffic from ${LAYER_NAME[layer]} ${thresholds[layer]} or newer`;
	}

	function select(iso2: string) {
		if (!byIso.has(iso2)) return;
		home ??= iso2;
		selected = iso2;
		globe?.rotateTo(iso2);
	}

	function setPhone(next: Phone) {
		phone.current = next;
	}
</script>

<svelte:head>
	<title>Where RCS works · textme</title>
	<meta name="description" content="See where RCS texting works for Android and iPhone, at home, when you travel, and where the people you know live." />
</svelte:head>

<div class="mx-auto flex min-h-svh w-full max-w-6xl flex-col px-4 pb-10 sm:px-6">
	<header class="flex h-20 shrink-0 items-center sm:h-24">
		<a href="/" class="font-display text-3xl font-bold tracking-tight">text<span class="text-primary">me</span></a>
	</header>

	<main class="grid gap-8 lg:grid-cols-[minmax(0,1fr)_26rem] lg:items-start">
		<div class="space-y-5">
			<div class="space-y-2">
				<h1 class="font-display text-4xl font-bold tracking-tight [text-wrap:balance] sm:text-5xl">Where RCS works</h1>
				<p class="max-w-prose text-muted-foreground [text-wrap:pretty]">
					RCS is the chat upgrade to SMS: typing dots, read receipts, full quality photos. Check it where you are, where you travel, and where your people live.
				</p>
			</div>

			<div class="flex flex-wrap items-end gap-x-5 gap-y-3">
				<fieldset class="segmented">
					<legend>My phone</legend>
					<div class="options">
						<label><input type="radio" name="phone" checked={phone.current === "android"} onchange={() => setPhone("android")} />Android</label>
						<label><input type="radio" name="phone" checked={phone.current === "iphone"} onchange={() => setPhone("iphone")} />iPhone</label>
					</div>
				</fieldset>
				<fieldset class="segmented">
					<legend>View</legend>
					<div class="options">
						<label><input type="radio" name="view" checked={!flat} onchange={() => (flat = false)} />Globe</label>
						<label><input type="radio" name="view" checked={flat} onchange={() => (flat = true)} />Flat map</label>
					</div>
				</fieldset>
				<label class="grid gap-1 text-sm font-medium">
					Colour by
					<select class="h-10 rounded-lg border border-input bg-card px-3 text-base" bind:value={layer}>
						<option value="status">RCS status</option>
						<option value="iphone">iPhones on iOS {thresholds.iphone} or newer</option>
						<option value="android">Android on {thresholds.android} or newer</option>
					</select>
				</label>
				{#if layer !== "status"}
					<label class="grid gap-1 text-sm font-medium">
						{layer === "iphone" ? "iOS" : "Android"} version
						<select class="h-10 rounded-lg border border-input bg-card px-3 text-base" bind:value={thresholds[layer]}>
							{#each THRESHOLD_CHOICES[layer] as choice (choice)}
								<option value={choice}>{choice} or newer{choice === minimum[layer] ? " (RCS minimum)" : ""}</option>
							{/each}
						</select>
					</label>
				{/if}
				<label class="grid gap-1 text-sm font-medium">
					Country
					<select
						class="h-10 rounded-lg border border-input bg-card px-3 text-base"
						value={selected ?? ""}
						onchange={(event) => select(event.currentTarget.value)}
					>
						{#if !selected}<option value="" disabled>Pick a country</option>{/if}
						{#each rows as row (row.iso2)}
							<option value={row.iso2}>{row.name}</option>
						{/each}
					</select>
				</label>
			</div>

			<Globe
				bind:this={globe}
				{flat}
				{selected}
				people={people.current}
				{isoByNumeric}
				{classOf}
				{nameOf}
				{legend}
				onselect={select}
			/>
		</div>

		<aside class="space-y-5">
			{#if selectedRow}
				<CountryCard
					row={selectedRow}
					phone={phone.current}
					isHome={selectedRow.iso2 === home}
					isPerson={hasPerson(selectedRow.iso2)}
					ontoggleperson={() => togglePerson(selectedRow.iso2)}
				/>
				{#if home && selected !== home}
					<button type="button" class="text-sm font-medium underline underline-offset-4" onclick={() => home && select(home)}>
						Back to {byIso.get(home)?.name}
					</button>
				{/if}
			{:else}
				<p class="rounded-2xl border border-dashed p-5 text-muted-foreground">
					We could not tell where you are. Pick your country in the list or on the map to start.
				</p>
			{/if}

			<section class="space-y-3" aria-labelledby="people-title">
				<h2 id="people-title" class="font-display text-xl font-bold tracking-tight">Where my people are</h2>
				{#if peopleRows.length === 0}
					<p class="text-sm text-muted-foreground">Open a country and tap "I know people here". Your list stays on this device.</p>
				{:else}
					<p>{summary}</p>
					<ul class="flex flex-wrap gap-2">
						{#each peopleRows as row (row.iso2)}
							<li class="person-chip">
								<button type="button" class="px-3" onclick={() => select(row.iso2)}>{row.name}</button>
								<button type="button" class="remove" aria-label="Remove {row.name}" onclick={() => togglePerson(row.iso2)}>
									<X size={14} aria-hidden="true" />
								</button>
							</li>
						{/each}
					</ul>
				{/if}
			</section>
		</aside>
	</main>

	<footer class="mt-auto pt-10 text-sm text-muted-foreground">
		Coverage from Apple's carrier lists, Google, carriers and GSMA, checked up to {asOf}. Phone shares from StatCounter. No data yet means nobody has checked, not that RCS is missing.
	</footer>
</div>

<style>
	.segmented {
		margin: 0;
		border: 0;
		padding: 0;
	}

	.segmented legend {
		margin-bottom: 0.25rem;
		padding: 0;
		font-size: 0.875rem;
		font-weight: 500;
	}

	.options {
		display: flex;
	}

	.segmented label {
		display: flex;
		align-items: center;
		min-height: 2.5rem;
		padding: 0 0.875rem;
		border: 1px solid hsl(var(--input));
		background: hsl(var(--card));
		font-size: 0.9375rem;
		font-weight: 500;
		white-space: nowrap;
		cursor: pointer;
		transition: background-color 150ms ease, color 150ms ease;
	}

	.segmented label:first-of-type {
		border-radius: 0.5rem 0 0 0.5rem;
	}

	.segmented label:last-of-type {
		border-left: 0;
		border-radius: 0 0.5rem 0.5rem 0;
	}

	.segmented label:has(:checked) {
		background: hsl(var(--primary));
		border-color: hsl(var(--primary));
		color: hsl(var(--primary-foreground));
	}

	.segmented label:has(:focus-visible) {
		outline: 2px solid hsl(var(--ring));
		outline-offset: 2px;
	}

	.segmented input {
		position: absolute;
		opacity: 0;
		pointer-events: none;
	}

	.person-chip {
		display: flex;
		align-items: stretch;
		min-height: 2.25rem;
		border: 1.5px solid oklch(0.7 0.17 50);
		border-radius: 999px;
		font-size: 0.875rem;
		font-weight: 500;
	}

	.person-chip .remove {
		display: grid;
		place-items: center;
		width: 2.25rem;
		border-left: 1px solid hsl(var(--border));
		color: hsl(var(--muted-foreground));
	}
</style>
