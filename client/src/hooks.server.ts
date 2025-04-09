import { GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET } from '$env/static/private';
import Google from '@auth/core/providers/google';
import { SvelteKitAuth } from '@auth/sveltekit';
import { redirect, type Handle } from '@sveltejs/kit';
import { sequence } from '@sveltejs/kit/hooks';

export const { handle: auth } = SvelteKitAuth({
	providers: [Google({ clientId: GOOGLE_CLIENT_ID, clientSecret: GOOGLE_CLIENT_SECRET })]
});

export const secure: Handle = async ({ event, resolve }) => {
	// Check if the user is signed in
	const session = await event.locals.auth();

	// If the user is not signed in and is not on the root page, redirect to the root page
	if (!session && event.url.pathname !== '/') {
		throw redirect(302, '/');
	}

	// Proceed with the request
	return resolve(event);
};

export const handle = sequence(auth, secure);
