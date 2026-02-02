<script lang="ts">
	import { Dialog } from "bits-ui";
	import { cn } from "$lib/utils.js";
	import { X } from "lucide-svelte";
	import type { Snippet } from "svelte";

	interface Props {
		open?: boolean;
		onOpenChange?: (open: boolean) => void;
		title?: string;
		trigger?: Snippet;
		children?: Snippet;
	}

	let {
		open = $bindable(false),
		onOpenChange,
		title,
		trigger,
		children
	}: Props = $props();
</script>

<Dialog.Root bind:open {onOpenChange}>
	{#if trigger}
		<Dialog.Trigger>
			{@render trigger()}
		</Dialog.Trigger>
	{/if}

	<Dialog.Portal>
		<Dialog.Overlay
			class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
		/>
		<Dialog.Content
			class="fixed inset-x-0 bottom-0 z-50 flex max-h-[85vh] flex-col rounded-t-2xl bg-background"
		>
			<div class="flex items-center justify-between border-b px-4 py-3">
				{#if title}
					<Dialog.Title class="text-lg font-semibold">{title}</Dialog.Title>
				{:else}
					<div></div>
				{/if}
				<Dialog.Close
					class="rounded-full p-1 hover:bg-muted transition-colors"
				>
					<X class="h-5 w-5" />
				</Dialog.Close>
			</div>
			<div class="flex-1 overflow-y-auto">
				{@render children?.()}
			</div>
		</Dialog.Content>
	</Dialog.Portal>
</Dialog.Root>
