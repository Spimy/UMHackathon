<script module lang="ts">
	export const colours = ['primary', 'bento-purple', 'bento-dark', 'bento-light-blue'] as const;
	export type Colour = (typeof colours)[number];
</script>

<script lang="ts">
	interface Props {
		title: string;
		value: string;
		percentage: string;
		colour: Colour;
	}

	let { title, value, percentage, colour }: Props = $props();

	// Determine if the percentage is positive or negative
	const isPositive = percentage.startsWith('+');
</script>

<div class="bg-{colour} text-tertiary flex flex-col space-y-2 rounded-lg shadow-md">
	<div class="grid gap-2 p-4 pb-0">
		<!-- Title -->
		<h2 class="text-mdsemi">{title}</h2>

		<!-- Value and Percentage -->
		<div class="flex items-end justify-between">
			<h3 class="text-xlsemi">{value}</h3>
			<p class="flex space-x-1 text-sm">
				<span>{percentage}</span>
				{#if isPositive}
					<img src="/icons/upward.svg" alt="Upward Trend" class="h-4 w-4" />
				{:else}
					<img src="/icons/downward.svg" alt="Downward Trend" class="h-4 w-4" />
				{/if}
			</p>
		</div>
	</div>

	<!-- Wave Pattern -->
	<div class="relative mt-2 h-6 w-full">
		<img src="/icons/wave.svg" alt="Wave Pattern" class="absolute inset-0 h-full w-full" />
	</div>
</div>
