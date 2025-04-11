import { PUBLIC_API_URL } from '$env/static/public';
import { error } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

interface Merchant {
	merchant_name: string;
	join_date: string;
	city_id: number;
	merchant_id: string;
}

interface User {
	id: number;
	user_email: string;
	merchant_id: string;
	merchant: Merchant;
}

export const load: LayoutServerLoad = async ({ locals, fetch }) => {
	const session = await locals.auth();

	const user: User | null = await fetch(
		`${PUBLIC_API_URL}/user/?email=${session?.user?.email}`
	).then((res) => {
		if (res.status === 200) {
			return res.json();
		}
		return null;
	});

	if (session && !user) {
		error(401, 'Unauthorized');
	}

	return { session, user };
};
