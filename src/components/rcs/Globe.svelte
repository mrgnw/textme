<script lang="ts">
	import { geoArea, geoCentroid, geoContains, geoGraticule10, geoNaturalEarth1, geoOrthographic, geoPath } from "d3-geo";
	import { feature } from "topojson-client";
	import type { Topology, GeometryCollection } from "topojson-specification";
	import type { Feature, FeatureCollection, Geometry } from "geojson";
	import { Tween, prefersReducedMotion } from "svelte/motion";
	import { cubicOut } from "svelte/easing";
	import worldUrl from "world-atlas/countries-110m.json?url";
	import type { Level } from "#lib/rcs/rcs.js";

	interface Country {
		key: string;
		iso2: string | null;
		name: string;
		shape: Feature<Geometry>;
	}

	interface Props {
		flat: boolean;
		selected: string | null;
		people: string[];
		isoByNumeric: Map<string, string>;
		levelOf: (iso2: string) => Level;
		nameOf: (iso2: string) => string;
		labels: Record<Level, string>;
		onselect: (iso2: string) => void;
	}

	let { flat, selected, people, isoByNumeric, levelOf, nameOf, labels, onselect }: Props = $props();

	const SIZE = 600;
	const FLAT = { width: 960, height: 500 };
	const KEY_STEP = 12;
	const LEVELS: Level[] = ["yes", "partial", "none", "unknown"];
	const uid = $props.id();
	const graticule = geoGraticule10();
	const sphere = { type: "Sphere" } as const;

	let countries = $state.raw<Country[]>([]);
	let status = $state<"loading" | "ready" | "error">("loading");
	let focused = $state(false);
	let drag: { x: number; y: number; from: [number, number]; target: string | null; moved: boolean } | null = null;

	const rotation = new Tween<[number, number]>([0, -20], { easing: cubicOut });

	const projection = $derived.by(() => {
		const [lambda, phi] = rotation.current;
		if (flat) {
			return geoNaturalEarth1().rotate([lambda, 0]).fitExtent([[8, 8], [FLAT.width - 8, FLAT.height - 8]], sphere);
		}
		return geoOrthographic().scale(SIZE / 2 - 6).translate([SIZE / 2, SIZE / 2]).rotate([lambda, phi]).clipAngle(90);
	});
	const path = $derived(geoPath(projection));
	const viewBox = $derived(flat ? `0 0 ${FLAT.width} ${FLAT.height}` : `0 0 ${SIZE} ${SIZE}`);
	const highlighted = $derived(countries.filter((c) => c.iso2 && people.includes(c.iso2)));
	const selectedShape = $derived(countries.find((c) => c.iso2 === selected));
	const centre = $derived(focused && status === "ready" ? countryAtCentre() : null);

	function toCountry(shape: Feature<Geometry>): Country {
		const name = (shape.properties as { name: string }).name;
		const numeric = shape.id as string | undefined;
		const iso2 = numeric ? isoByNumeric.get(numeric) ?? null : null;
		return { key: numeric ?? name, iso2, name, shape };
	}

	function loadWorld() {
		fetch(worldUrl)
			.then((response) => {
				if (!response.ok) throw new Error(`world shapes: HTTP ${response.status}`);
				return response.json();
			})
			.then((world: Topology<{ countries: GeometryCollection }>) => {
				const collection = feature(world, world.objects.countries) as FeatureCollection<Geometry>;
				countries = collection.features.map(toCountry);
				status = "ready";
				if (selected) rotateTo(selected, true);
			})
			.catch(() => (status = "error"));
	}

	function shortestLambda(target: number): number {
		const current = rotation.current[0];
		return current + ((((target - current) % 360) + 540) % 360) - 180;
	}

	function duration(ms: number): number {
		return prefersReducedMotion.current || document.hidden ? 0 : ms;
	}

	export function rotateTo(iso2: string, instant = false) {
		const country = countries.find((c) => c.iso2 === iso2);
		if (!country) return;
		const [lon, lat] = geoCentroid(mainland(country.shape));
		const next: [number, number] = [shortestLambda(-lon), Math.max(-60, Math.min(60, -lat))];
		rotation.set(next, { duration: instant ? 0 : duration(700) });
	}

	function mainland(shape: Feature<Geometry>): Feature<Geometry> {
		if (shape.geometry.type !== "MultiPolygon") return shape;
		const parts = shape.geometry.coordinates.map((coordinates) => ({ type: "Polygon" as const, coordinates }));
		const largest = parts.reduce((best, part) => (geoArea(part) > geoArea(best) ? part : best));
		return { ...shape, geometry: largest };
	}

	function countryAtCentre(): Country | null {
		const point = flat ? projection.invert?.([FLAT.width / 2, FLAT.height / 2]) : [-rotation.current[0], -rotation.current[1]];
		if (!point) return null;
		return countries.find((c) => c.iso2 && geoContains(c.shape, point as [number, number])) ?? null;
	}

	function onpointerdown(event: PointerEvent) {
		const svg = event.currentTarget as SVGSVGElement;
		const target = (event.target as Element).closest("[data-iso]")?.getAttribute("data-iso") ?? null;
		drag = { x: event.clientX, y: event.clientY, from: [...rotation.current], target, moved: false };
		svg.setPointerCapture(event.pointerId);
	}

	function onpointermove(event: PointerEvent) {
		if (!drag) return;
		const dx = event.clientX - drag.x;
		const dy = event.clientY - drag.y;
		if (Math.hypot(dx, dy) > 4) drag.moved = true;
		if (!drag.moved) return;
		const width = (event.currentTarget as SVGSVGElement).getBoundingClientRect().width;
		const k = (flat ? 360 : 180) / width;
		const phi = flat ? 0 : Math.max(-90, Math.min(90, drag.from[1] - dy * k));
		rotation.set([drag.from[0] + dx * k, phi], { duration: 0 });
	}

	function onpointerup() {
		if (drag && !drag.moved && drag.target) onselect(drag.target);
		drag = null;
	}

	function onkeydown(event: KeyboardEvent) {
		const [lambda, phi] = rotation.target;
		const moves: Record<string, [number, number]> = {
			ArrowLeft: [lambda + KEY_STEP, phi],
			ArrowRight: [lambda - KEY_STEP, phi],
			ArrowUp: [lambda, Math.max(-90, phi - KEY_STEP)],
			ArrowDown: [lambda, Math.min(90, phi + KEY_STEP)]
		};
		if (event.key in moves) {
			event.preventDefault();
			rotation.set(moves[event.key], { duration: duration(150) });
			return;
		}
		if ((event.key === "Enter" || event.key === " ") && centre?.iso2) {
			event.preventDefault();
			onselect(centre.iso2);
		}
	}

	function label(country: Country): string {
		if (!country.iso2) return `${country.name}: no data`;
		return nameOf(country.iso2);
	}
</script>

<figure class={["globe", { flat }]} aria-busy={status === "loading"}>
	<!-- svelte-ignore a11y_no_noninteractive_element_interactions, a11y_no_noninteractive_tabindex -->
	<svg
		class="world"
		{viewBox}
		role="application"
		aria-roledescription={flat ? "map" : "globe"}
		aria-label="World map of RCS support. Drag or use arrow keys to turn it. Press Enter to pick the country in the middle."
		aria-describedby="{uid}-centre"
		tabindex="0"
		{@attach loadWorld}
		{onpointerdown}
		{onpointermove}
		{onpointerup}
		onpointercancel={() => (drag = null)}
		{onkeydown}
		onfocus={() => (focused = true)}
		onblur={() => (focused = false)}
	>
		<defs>
			<pattern id="{uid}-partial" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
				<rect class="partial-bg" width="6" height="6" />
				<line class="partial-line" x1="0" y1="0" x2="0" y2="6" />
			</pattern>
			<pattern id="{uid}-unknown" width="5" height="5" patternUnits="userSpaceOnUse">
				<rect class="unknown-bg" width="5" height="5" />
				<circle class="unknown-dot" cx="2.5" cy="2.5" r="0.9" />
			</pattern>
		</defs>
		<path class="sphere" d={path(sphere)} />
		<path class="graticule" d={path(graticule)} />
		{#each countries as country (country.key)}
			{@const level = country.iso2 ? levelOf(country.iso2) : "unknown"}
			<path
				class="land {level}"
				style:--partial="url(#{uid}-partial)"
				style:--unknown="url(#{uid}-unknown)"
				d={path(country.shape)}
				data-iso={country.iso2}
			>
				<title>{label(country)}</title>
			</path>
		{/each}
		{#each highlighted as country (country.key)}
			<path class="person" d={path(country.shape)} />
		{/each}
		{#if selectedShape}
			<path class="selected" d={path(selectedShape.shape)} />
		{/if}
		{#if focused}
			<g class="crosshair" transform={flat ? `translate(${FLAT.width / 2} ${FLAT.height / 2})` : `translate(${SIZE / 2} ${SIZE / 2})`}>
				<circle r="7" />
				<line x1="-13" x2="-4" />
				<line x1="4" x2="13" />
			</g>
		{/if}
	</svg>
	<p id="{uid}-centre" class="centre" aria-live="polite">
		{#if status === "loading"}
			Loading the map.
		{:else if status === "error"}
			The map did not load. Use the country list instead.
		{:else if focused}
			Middle: {centre ? label(centre) : "ocean"}
		{/if}
	</p>
	<figcaption>
		<ul class="legend">
			{#each LEVELS as level (level)}
				<li>
					<svg class="swatch" viewBox="0 0 16 16" aria-hidden="true">
						<rect class="land {level}" style:--partial="url(#{uid}-partial)" style:--unknown="url(#{uid}-unknown)" width="16" height="16" rx="3" />
					</svg>
					{labels[level]}
				</li>
			{/each}
			<li>
				<svg class="swatch" viewBox="0 0 16 16" aria-hidden="true">
					<rect class="person" x="1.5" y="1.5" width="13" height="13" rx="3" />
				</svg>
				Your people
			</li>
		</ul>
	</figcaption>
</figure>

<style>
	.globe {
		--rcs-people: oklch(0.7 0.17 50);
		margin: 0;
		display: grid;
		gap: 0.5rem;
		justify-items: center;
	}

	.world {
		width: 100%;
		max-width: 36rem;
		height: auto;
		cursor: grab;
		touch-action: pan-y;
		user-select: none;
		border-radius: 50%;
		outline-offset: 4px;
	}

	.flat .world {
		max-width: none;
		border-radius: var(--radius);
	}

	.world:active {
		cursor: grabbing;
	}

	.world:focus-visible {
		outline: 2px solid hsl(var(--ring));
	}

	.sphere {
		fill: hsl(var(--card));
		stroke: hsl(var(--border));
		stroke-width: 1.5;
	}

	.graticule {
		fill: none;
		stroke: hsl(var(--border) / 0.7);
		stroke-width: 0.5;
	}

	.land {
		stroke: hsl(var(--card));
		stroke-width: 0.6;
		stroke-linejoin: round;
		transition: fill 150ms ease;
	}

	.land.yes {
		fill: hsl(var(--primary));
	}

	.land.partial {
		fill: var(--partial);
	}

	.land.none {
		fill: hsl(var(--muted-foreground) / 0.45);
	}

	.land.unknown {
		fill: var(--unknown);
	}

	.partial-bg {
		fill: hsl(var(--primary) / 0.25);
	}

	.partial-line {
		stroke: hsl(var(--primary));
		stroke-width: 2.5;
	}

	.unknown-bg {
		fill: hsl(var(--muted));
	}

	.unknown-dot {
		fill: hsl(var(--muted-foreground) / 0.7);
	}

	.person {
		fill: none;
		stroke: var(--rcs-people);
		stroke-width: 2.5;
		stroke-linejoin: round;
		pointer-events: none;
	}

	.selected {
		fill: none;
		stroke: hsl(var(--foreground));
		stroke-width: 2.5;
		stroke-linejoin: round;
		pointer-events: none;
	}

	.crosshair {
		fill: none;
		stroke: hsl(var(--foreground));
		stroke-width: 2;
		pointer-events: none;
	}

	.centre {
		min-height: 1.25rem;
		font-size: 0.875rem;
		color: hsl(var(--muted-foreground));
	}

	.legend {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: 0.375rem 1rem;
		font-size: 0.875rem;
		color: hsl(var(--muted-foreground));
	}

	.legend li {
		display: flex;
		align-items: center;
		gap: 0.375rem;
	}

	.swatch {
		width: 1rem;
		height: 1rem;
	}

	@media (prefers-reduced-motion: reduce) {
		.land {
			transition: none;
		}
	}
</style>
