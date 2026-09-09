<script lang="ts">
	import XIcon from "@lucide/svelte/icons/x";
	import { Button } from "$lib/components/ui/button";
	import { parse } from "svelte-tel-input/utils";
	import { forget, recent } from "$lib/recent.svelte";

	interface Props {
		onpick: (e164: string) => void;
	}

	let { onpick }: Props = $props();
</script>

{#if recent.current.length > 0}
	<div class="space-y-3 pt-6">
		<p class="text-center text-xs font-semibold uppercase tracking-wider text-muted-foreground">Recent</p>
		<div class="flex flex-wrap justify-center gap-2">
			{#each recent.current as r (r.e164)}
				<span class="inline-flex h-9 items-center gap-1.5 rounded-full border bg-card pl-3 pr-1 text-sm tabular-nums">
					<button type="button" class="hover:underline underline-offset-4" onclick={() => onpick(r.e164)}>
						{parse(r.e164).formatInternational ?? r.e164}
					</button>
					{#if r.name}<span class="text-muted-foreground">{r.name}</span>{/if}
					<Button variant="ghost" size="icon" class="h-7 w-7 rounded-full text-muted-foreground" aria-label="Remove {r.e164}" onclick={() => forget(r.e164)}>
						<XIcon class="size-3.5" />
					</Button>
				</span>
			{/each}
		</div>
	</div>
{/if}
