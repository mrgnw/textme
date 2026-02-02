<script lang="ts">
	import { Check } from "lucide-svelte";

	interface Props {
		flag: string;
		name: string;
		dialCode: string;
		selected?: boolean;
		showCheck?: boolean;
	}

	let { flag, name, dialCode, selected = false, showCheck = true }: Props = $props();
</script>

<div class="flex items-center gap-3 w-full">
	<span class="text-xl">{flag}</span>
	<span class="flex-1 truncate">{name}</span>
	<span class="text-muted-foreground text-sm">+{dialCode}</span>
	{#if showCheck && selected}
		<Check class="h-4 w-4 text-primary" />
	{/if}
</div>
