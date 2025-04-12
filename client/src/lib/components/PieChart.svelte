<script lang="ts">
	import type { ApexOptions } from 'apexcharts';
	import { onMount } from 'svelte';
	import type { PlotPointsResponse } from '../../routes/chat/[id]/+page.svelte';

	interface Props {
		res: PlotPointsResponse;
	}

	let chart: HTMLDivElement | null = $state(null);
	let { res }: Props = $props();

	onMount(() => {
		import('apexcharts').then((ApexCharts) => {
			const options: ApexOptions = {
				chart: {
					type: 'pie',
					foreColor: '#000000',
					height: '100%'
				},
				series: res.data_points[res.time].map((point) => point[res.data_point]),
				labels: res.data_points[res.time].map((point) => point.item_name),
				dataLabels: {
					enabled: false
				},
				tooltip: {
					x: {
						show: true
					}
				}
			};
			new ApexCharts.default(chart, options).render();
		});
	});
</script>

<div bind:this={chart}></div>
