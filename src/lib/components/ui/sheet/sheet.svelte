<script lang="ts">
	import { Dialog } from "bits-ui";
	import { fade, fly } from "svelte/transition";
	import X from "@lucide/svelte/icons/x";
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
		<Dialog.Overlay forceMount class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm">
			{#snippet child({ props, open })}
				{#if open}
					<div {...props} transition:fade={{ duration: 150 }}></div>
				{/if}
			{/snippet}
		</Dialog.Overlay>
		<Dialog.Content forceMount class="fixed inset-x-0 bottom-0 z-50 flex max-h-[85vh] flex-col rounded-t-2xl bg-background">
			{#snippet child({ props, open })}
				{#if open}
					<div {...props} transition:fly={{ y: 240, duration: 250 }}>
						<div class="flex items-center justify-between border-b px-4 py-3">
							{#if title}
								<Dialog.Title class="text-lg font-semibold">{title}</Dialog.Title>
							{:else}
								<div></div>
							{/if}
							<Dialog.Close class="rounded-full p-1 transition-colors hover:bg-muted">
								<X class="h-5 w-5" />
							</Dialog.Close>
						</div>
						<div class="flex-1 overflow-y-auto">
							{@render children?.()}
						</div>
					</div>
				{/if}
			{/snippet}
		</Dialog.Content>
	</Dialog.Portal>
</Dialog.Root>
