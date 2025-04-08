<script>
	import { page } from '$app/state';
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
<p>
	{#if page.data.session}
		<span>
			<small>Signed in as</small><br />
			<strong>{page.data.session.user?.name ?? 'User'}</strong>
		</span>
		<a class="bg-blue cursor-pointer rounded bg-blue-400 px-2 py-1" href="/auth/signout">Sign out</a
		>
	{:else}
		<span>You are not signed in</span>
		<a class="bg-blue cursor-pointer rounded bg-blue-400 px-2 py-1" href="/auth/signin">
			Sign In with Google
		</a>
	{/if}
</p>
