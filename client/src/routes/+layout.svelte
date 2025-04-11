<script lang="ts">
	import { page } from '$app/state';
	import Navbar from '$lib/components/Navbar.svelte';
	import '../app.css';

	let { children, data } = $props();
</script>

<div class="grid h-screen grid-cols-[auto_1fr]">
	{#if page.data.session}
		<Navbar
			merchantName={data.user?.merchant.merchant_name || 'Merchant'}
			brandingIconUrl={data.session?.user?.image ||
				`https://ui-avatars.com/api/?name=${data.user?.merchant.merchant_name}`}
		/>
	{/if}

	<div class="overflow-y-auto">
		{@render children()}
	</div>
</div>
