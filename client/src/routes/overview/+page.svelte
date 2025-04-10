<script lang="ts">
	import StatCard, { colours, type Colour } from '$lib/components/StatCard.svelte';
	import { type ApexOptions } from 'apexcharts';
	import { onMount } from 'svelte';

	const numFormat = (value: number) => {
		return Intl.NumberFormat('en-US', {
			notation: 'compact',
			maximumFractionDigits: 1
		}).format(value);
	};

	const merchartChartOptions: ApexOptions = {
		chart: {
			type: 'bar',
			foreColor: '#fefefe'
		},
		plotOptions: {
			bar: {
				distributed: true
			}
		},
		series: [
			{
				name: 'Merchant',
				data: [18000, 30000, 20000, 32000, 12000, 24000]
			}
		],
		xaxis: {
			categories: ['Bliss', 'Factory', 'Barn', 'Joint', 'Bar', 'Other']
		},
		yaxis: {
			labels: {
				formatter: numFormat
			}
		},
		dataLabels: {
			enabled: false
		},
		legend: {
			show: false
		},
		tooltip: {
			theme: 'dark'
		},
		colors: ['#9F9FF8', '#FEFEFE', '#96E2D6', '#92BFFF', '#AEC7ED', '#000000']
	};

	const trafficChartOptions: ApexOptions = {
		chart: {
			type: 'donut',
			foreColor: '#fefefe'
		},
		plotOptions: {
			bar: {
				distributed: true
			}
		},
		series: [52.1, 22.8, 13.9, 11.2],
		labels: ['Subang Jaya', 'Old Klang', 'Bukit Jalil', 'Other'],
		dataLabels: {
			enabled: false
		},
		legend: {
			show: true
		},
		tooltip: {
			theme: 'dark',
			y: {
				formatter: (v) => `${v}%`
			}
		},
		colors: ['#000000', '#92BFFF', '#96E2D6', '#AEC7ED']
	};

	const marketingChartOptions: ApexOptions = {
		chart: {
			type: 'bar',
			foreColor: '#fefefe',
			height: '100%'
		},
		plotOptions: {
			bar: {
				distributed: true
			}
		},
		series: [
			{
				name: 'Month',
				data: [18000, 30000, 20000, 32000, 12000, 24000, 18000, 30000, 20000, 32000, 12000, 24000]
			}
		],
		xaxis: {
			categories: [
				'Jan',
				'Feb',
				'Mar',
				'Apr',
				'May',
				'Jun',
				'Jul',
				'Aug',
				'Sep',
				'Oct',
				'Nov',
				'Dec'
			]
		},
		yaxis: {
			labels: {
				formatter: numFormat
			}
		},
		dataLabels: {
			enabled: false
		},
		legend: {
			show: false
		},
		tooltip: {
			theme: 'dark'
		},
		colors: ['#9F9FF8', '#FEFEFE', '#96E2D6', '#92BFFF', '#AEC7ED', '#000000']
	};

	let merchantChart: HTMLDivElement | null = $state(null);
	let trafficChart: HTMLDivElement | null = $state(null);
	let marketingChart: HTMLDivElement | null = $state(null);

	onMount(() => {
		import('apexcharts').then((ApexCharts) => {
			new ApexCharts.default(merchantChart, merchartChartOptions).render();
			new ApexCharts.default(trafficChart, trafficChartOptions).render();
			new ApexCharts.default(marketingChart, marketingChartOptions).render();
		});
	});

	interface Stat {
		title: string;
		value: string;
		percentage: string;
	}

	interface TopSale {
		name: string;
		value: number;
	}

	let stats: Stat[] = $state([
		{ title: 'Orders', value: '7,548', percentage: '+11.01%' },
		{ title: 'Merchant Views', value: '15,678', percentage: '-0.03%' },
		{ title: 'New Customers', value: '648', percentage: '+15.03%' },
		{ title: 'Active Customers', value: '1,430', percentage: '+6.08%' }
	]);

	let totalSales = $state('RM235,741.31');
	let topSales: TopSale[] = $state([
		{ name: 'BBQ Cheese', value: 550 },
		{ name: 'Double Veg', value: 300 },
		{ name: 'Will Tender', value: 450 },
		{ name: 'Jusger', value: 200 },
		{ name: "Alex's Fries", value: 400 },
		{ name: 'JB Burger', value: 100 },
		{ name: 'Berry Milkshake', value: 300 },
		{ name: 'Factory Soda', value: 550 }
	]);

	// Calculate the maximum sales value
	const maxSales = Math.max(...topSales.map((item) => item.value));

	let currentColour = 0;
	const getColour = (): Colour => {
		const colour = colours[currentColour];
		currentColour = (currentColour + 1) % colours.length;
		return colour;
	};
</script>

<main class="m-5 grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-5">
	<div
		class="grid grid-cols-1 gap-4 sm:col-span-2 sm:grid-cols-2 md:col-span-full md:grid-cols-2 lg:col-span-4 lg:grid-cols-4"
	>
		{#each stats as stat}
			<StatCard
				title={stat.title}
				value={stat.value}
				percentage={stat.percentage}
				colour={getColour()}
			/>
		{/each}
	</div>

	<div class="bg-primary col-span-full row-span-3 rounded-xl p-4 text-white shadow lg:col-span-1">
		<h2 class="text-lgsemi">Top Sales of the Day</h2>
		<ul class="flex h-full flex-col justify-evenly space-y-3 py-4">
			{#each topSales as item}
				<li class="flex items-center gap-3">
					<span class="text-md w-1/2">{item.name}</span>
					<div class="flex w-1/2 items-center space-x-1">
						<!-- Create the bars -->
						{#each Array(Math.min(3, Math.round((item.value / maxSales) * 3))) as _}
							<span class="block h-2 w-8 rounded-full bg-white"></span>
						{/each}
					</div>
				</li>
			{/each}
		</ul>
	</div>

	<!-- Total Sales -->
	<div
		class="bg-bento-dark relative col-span-full row-span-1 rounded-xl text-white shadow lg:col-span-4"
	>
		<!-- Dropdown -->
		<div class="absolute right-4 top-4">
			<div class="relative">
				<select
					class="bg-bento-dark focus:ring-highlight cursor-pointer rounded-md border-none py-1 pl-2 pr-6 text-base text-white focus:outline-none focus:ring-2"
				>
					<option value="this-week">This week</option>
					<option value="last-week">This month</option>
					<option value="this-month">This year</option>
				</select>
			</div>
		</div>

		<!-- Content -->
		<div class="p-6">
			<h2 class="text-mdsemi">Total Sales</h2>
			<h3 class="text-xlsemi">
				{#each totalSales.split('.') as part, index}
					{#if index === 0}
						{part}
					{:else}
						<span class="text-base">{'.'}{part}</span>
					{/if}
				{/each}
			</h3>
		</div>

		<div class="mt-auto">
			<img src="/icons/wave-large.svg" alt="Wave Pattern" class="h-auto w-full" />
		</div>
	</div>

	<!-- Merchants -->
	<div
		class="bg-primary col-span-full row-span-1 grid rounded-xl p-4 text-white shadow md:col-span-2"
	>
		<h2 class="text-lgsemi mb-5">Top Performing Merchants</h2>
		<div class="col-span-full" bind:this={merchantChart}></div>
	</div>

	<!-- Traffic -->
	<div
		class="bg-primary col-span-full row-span-1 grid rounded-xl p-4 text-white shadow md:col-span-2"
	>
		<h2 class="text-lgsemi mb-5">Traffic by Location</h2>
		<div class="col-span-full" bind:this={trafficChart}></div>
	</div>

	<!-- Marketing -->
	<div class="bg-primary col-span-full row-span-1 max-h-96 rounded-xl p-4 text-white shadow">
		<h2 class="text-lgsemi mb-5">Marketing and SEO</h2>
		<div class="col-span-full" bind:this={marketingChart}></div>
	</div>
</main>

<style>
	:global(.apexcharts-toolbar svg) {
		fill: #fefefe !important;
	}
	:global(.apexcharts-menu) {
		background: #252828 !important;
		border-color: #18481a !important;
	}

	:global(.apexcharts-menu-item:hover) {
		background: #18481a !important;
	}
</style>
