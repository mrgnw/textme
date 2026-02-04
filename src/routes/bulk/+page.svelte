<script>
	import { TextareaAutosize } from "runed";
	import { parseBulkText } from "$lib/bulkParse";
	import BulkRow from "$components/BulkRow.svelte";
	import { scale } from "svelte/transition";

	let textareaEl = $state(
		/** @type {HTMLTextAreaElement | undefined} */ (undefined),
	);
	let input = $state("");

	new TextareaAutosize({
		element: () => textareaEl,
		input: () => input,
	});

	let contacts = $derived(parseBulkText(input));

	const placeholder = `Maria 34612345678
Luis 34698765432
Ana B 34656781234

Friends:
Carlos 34634567890
Elena 34678901234`;
</script>

<div class="max-w-2xl mx-auto p-6 sm:p-8 lg:p-10 my-8">
	<div class="text-center mb-8">
		<h1 class="text-3xl sm:text-4xl lg:text-5xl mb-4">Bulk contacts</h1>
		<p class="text-xl sm:text-2xl lg:text-3xl text-muted-foreground">
			Paste a list of names and phone numbers
		</p>
	</div>

	<textarea
		bind:this={textareaEl}
		bind:value={input}
		{placeholder}
		class="bulk-textarea"
		rows="3"
	></textarea>

	{#if contacts.length > 0}
		<div class="results" transition:scale={{ duration: 200, start: 0.97 }}>
			<p class="text-sm text-muted-foreground mb-2">
				{contacts.length} contact{contacts.length === 1 ? "" : "s"} found
			</p>
			{#each contacts as contact (contact.raw)}
				<BulkRow phone={contact.phone} name={contact.name} />
			{/each}
		</div>
	{/if}
</div>

<style>
	.bulk-textarea {
		width: 100%;
		resize: none;
		overflow: hidden;
		border: 1px solid hsl(var(--border));
		border-radius: 0.75rem;
		padding: 0.75rem 1rem;
		font-family: monospace;
		font-size: 0.9rem;
		line-height: 1.6;
		background: hsl(var(--background));
		color: hsl(var(--foreground));
		transition: border-color 0.2s ease;
	}

	.bulk-textarea:focus {
		outline: none;
		border-color: hsl(var(--coral));
	}

	.bulk-textarea::placeholder {
		color: hsl(var(--muted-foreground));
		opacity: 0.6;
	}

	.results {
		margin-top: 1.5rem;
	}
</style>
