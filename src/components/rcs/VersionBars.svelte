<script lang="ts">
	import Check from "@lucide/svelte/icons/check";
	import Minus from "@lucide/svelte/icons/minus";
	import type { Phone } from "#lib/rcs/rcs.js";
	import { formatPhones, formatShare, thresholdShare, versionBars, type PhoneEstimate, type PlatformVersions } from "#lib/rcs/versions.js";

	interface Props {
		phone: Phone;
		versions: PlatformVersions | null;
		estimate: PhoneEstimate | null;
		minimum: number;
	}

	let { phone, versions, estimate, minimum }: Props = $props();

	const name = $derived(phone === "iphone" ? "iPhone" : "Android");
	const os = $derived(phone === "iphone" ? "iOS" : "Android");
	const bars = $derived(versions ? versionBars(versions, estimate, phone, minimum) : []);
	const meeting = $derived(thresholdShare(versions, minimum));
</script>

<section class="space-y-2">
	<h4 class="font-medium">{name}</h4>
	{#if !versions || meeting === null}
		<p class="text-muted-foreground">No {os} version data yet for this country.</p>
	{:else}
		<p class="text-muted-foreground">
			{formatShare(meeting)} of sampled {name} web traffic here is on {os} {minimum} or newer, the RCS minimum.
		</p>
		<ul class="space-y-1">
			{#each bars as bar (bar.label)}
				<li class="bar-row">
					<span class={["meets", { below: !bar.meets }]}>
						{#if bar.meets}<Check size={12} strokeWidth={3} aria-hidden="true" />{:else}<Minus size={12} strokeWidth={3} aria-hidden="true" />{/if}
						<span class="sr-only">{bar.meets ? "meets the RCS minimum" : "below the RCS minimum"}</span>
					</span>
					<span class="label">{bar.label}</span>
					<span class="track" aria-hidden="true"><span class={["fill", { below: !bar.meets }]} style:inline-size="{Math.min(100, bar.value)}%"></span></span>
					<span class="value tabular-nums">{bar.value < 1 ? "<1%" : formatShare(bar.value)}</span>
					{#if bar.phones !== null}<span class="phones text-muted-foreground">about {formatPhones(bar.phones)} phones</span>{/if}
				</li>
			{/each}
		</ul>
		<p class="text-xs text-muted-foreground">
			Share of sampled mobile web traffic, <a class="underline underline-offset-2" href={versions.source_url} target="_blank" rel="noreferrer">StatCounter</a>, {versions.date}.
			<span class="confidence">Measured</span>
		</p>
		{#if estimate}
			<p class="text-xs text-muted-foreground">
				Phone counts are estimates: <a class="underline underline-offset-2" href={estimate.base.source_url} target="_blank" rel="noreferrer">a smartphone base of {formatPhones(estimate.base.value)}</a> ({estimate.base.date}), split by the web traffic shares above as a stand-in for the phones in use.
				<span class="confidence estimate">Estimate</span>
			</p>
		{/if}
	{/if}
</section>

<style>
	.bar-row {
		display: grid;
		grid-template-columns: 1rem 7.5rem minmax(3rem, 1fr) 2.5rem;
		align-items: center;
		gap: 0.5rem;
	}

	.phones {
		grid-column: 2 / -1;
		margin-top: -0.25rem;
		font-size: 0.75rem;
	}

	.meets {
		display: grid;
		place-items: center;
		width: 1rem;
		height: 1rem;
		border-radius: 999px;
		background: hsl(var(--primary));
		color: hsl(var(--primary-foreground));
	}

	.meets.below {
		background: hsl(var(--muted));
		color: hsl(var(--muted-foreground));
	}

	.label {
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.track {
		block-size: 0.5rem;
		border-radius: 999px;
		background: hsl(var(--muted));
		overflow: hidden;
	}

	.fill {
		display: block;
		block-size: 100%;
		background: hsl(var(--primary));
	}

	.fill.below {
		background: repeating-linear-gradient(135deg, hsl(var(--muted-foreground)) 0 2px, transparent 2px 4px);
	}

	.value {
		text-align: end;
	}

	.confidence {
		margin-left: 0.25rem;
		border: 1px solid hsl(var(--border));
		border-radius: 999px;
		padding: 0 0.5rem;
		color: hsl(var(--foreground));
	}

	.confidence.estimate {
		border-style: dashed;
	}
</style>
