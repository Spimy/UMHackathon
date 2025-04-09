<script lang="ts">
	import { page } from '$app/state';

	interface NavItem {
		label: string;
		href: string;
		icon: string;
	}

	interface Props {
		brandingIconUrl: string;
	}

	let { brandingIconUrl }: Props = $props();

	// Array of navigation items
	const navItems: NavItem[] = [
		{ label: 'Overview', href: '/overview', icon: '/icons/overview.svg' },
		{ label: 'Chat', href: '/chat', icon: '/icons/chat.svg' },
		{ label: 'Inventory', href: '/inventory', icon: '/icons/inventory.svg' },
		{ label: 'Alerts', href: '/alerts', icon: '/icons/alerts.svg' },
		{ label: 'Account', href: '/account', icon: '/icons/user.svg' }
	];
</script>

<header class="bg-primary text-tertiary px-3 py-6">
	<!-- Navbar -->
	<nav class="flex h-full flex-col items-center space-y-8">
		<!-- Branding -->
		<a href="/overview" class="flex flex-col items-center space-y-2">
			<img src={brandingIconUrl} alt="Brand Logo" class="h-16 w-16 object-contain" />
			<span class="text-mdsemi drop-shadow-lg">Burger Factory</span>
		</a>

		<!-- Navigation Items -->
		<ul class="flex flex-col space-y-6">
			{#each navItems as { label, href, icon }}
				<li class="flex flex-col items-center">
					<a
						{href}
						class="{page.url.pathname.includes(href)
							? 'bg-highlight'
							: ''} hover:bg-highlight flex w-full flex-col items-center rounded-lg p-4 text-center transition duration-300 ease-in-out"
					>
						<img src={icon} alt="{label} Icon" />
						<span class="text-mdsemi">{label}</span>
					</a>
				</li>
			{/each}
		</ul>

		<!-- Log Out Button -->
		<a
			href="/auth/signout"
			class="text-mdsemi mt-auto w-full cursor-pointer rounded-lg bg-red-800 py-3 text-center text-white transition duration-300 hover:bg-red-700"
		>
			Sign Out
		</a>
	</nav>
</header>
