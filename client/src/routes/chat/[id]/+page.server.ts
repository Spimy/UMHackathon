import { PUBLIC_API_URL } from '$env/static/public';
import { error, type Actions } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export interface Message {
	id?: number;
	chat_id?: number;
	text: string;
	is_sent: boolean;
	image?: string;
	timestamp?: string;
}

export interface ChatResponse {
	id: number;
	name: string;
	user_email: string;
	created_at: string;
}

export const load: PageServerLoad = async ({ params, locals, fetch }) => {
	const session = (await locals.auth())!;

	const chatId = Number(params.id);
	if (isNaN(chatId)) return error(404, 'Chat not found');

	const chats: ChatResponse[] = await fetch(`${PUBLIC_API_URL}/chat/${session.user?.email}`).then(
		(res) => res.json()
	);

	const messages: Message[] = await fetch(`${PUBLIC_API_URL}/chat/${chatId}/messages`).then((res) =>
		res.json()
	);

	return { chats, chatId, messages };
};

export const actions = {
	createChat: async ({ locals, fetch }) => {
		const session = (await locals.auth())!;

		await fetch(`${PUBLIC_API_URL}/chat`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ name: 'New Chat', user_email: session.user?.email })
		}).then((res) => res.json());
	}
} satisfies Actions;
