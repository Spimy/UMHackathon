import { PUBLIC_API_URL } from '$env/static/public';
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { ChatResponse } from './[id]/+page.server';

export const load: PageServerLoad = async ({ locals, fetch }) => {
	const session = (await locals.auth())!;

	const chat: ChatResponse = await fetch(`${PUBLIC_API_URL}/chat`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ name: 'New Chat', user_email: session.user?.email })
	}).then((res) => res.json());

	redirect(303, `/chat/${chat.id}`);
};
