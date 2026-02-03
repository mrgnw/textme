<script>
	let { href = null, onclick = null, icon: Icon, label, highlighted = false, disabled = false } = $props();
</script>

{#if href}
	<a
		{href}
		target="_blank"
		class="action-button"
		class:highlighted
		class:disabled
		onclick={(e) => disabled && e.preventDefault()}
	>
		<span class="icon-wrapper">
			<Icon class="w-7 h-7 sm:w-8 sm:h-8" />
		</span>
		<span class="label">{label}</span>
	</a>
{:else}
	<button
		{onclick}
		class="action-button"
		class:highlighted
		{disabled}
	>
		<span class="icon-wrapper">
			<Icon class="w-7 h-7 sm:w-8 sm:h-8" />
		</span>
		<span class="label">{label}</span>
	</button>
{/if}

<style>
	.action-button {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.25rem;
		padding: 0.5rem;
		border-radius: 0.75rem;
		transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
		text-decoration: none;
		color: inherit;
		background: transparent;
		border: none;
		cursor: pointer;
		min-width: 4rem;
	}

	.action-button:hover:not(.disabled) {
		transform: scale(1.1);
	}

	.action-button:active:not(.disabled) {
		transform: scale(0.95);
	}

	.action-button.disabled {
		opacity: 0.3;
		cursor: not-allowed;
	}

	.icon-wrapper {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.highlighted .icon-wrapper::before {
		content: '';
		position: absolute;
		inset: -8px;
		background: radial-gradient(circle, rgba(0,136,204,0.35) 0%, transparent 70%);
		border-radius: 50%;
		animation: pulse 2s ease-in-out infinite;
	}

	.highlighted {
		color: #0088cc;
	}

	@keyframes pulse {
		0%, 100% {
			opacity: 0.6;
			transform: scale(1);
		}
		50% {
			opacity: 1;
			transform: scale(1.15);
		}
	}

	.label {
		font-size: 0.7rem;
		font-weight: 500;
		opacity: 0.8;
	}

	@media (min-width: 640px) {
		.label {
			font-size: 0.75rem;
		}
	}
</style>
