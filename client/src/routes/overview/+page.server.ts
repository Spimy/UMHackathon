import { PUBLIC_API_URL } from '$env/static/public';
import type { PageServerLoad } from './$types';

export type Merchant = {
	id: string;
	name: string;
};

export type ReviewData = {
	review_summary: string;
	average_rating: number;
};

export const load: PageServerLoad = async ({ fetch }) => {
	const competitor1_id = '2e8a5';
	const competitor2_id = '5c1f8';

	const merchantData1 = await fetch(`${PUBLIC_API_URL}/merchants/${competitor1_id}`).then((res) =>
		res.json()
	);
	const merchantData2 = await fetch(`${PUBLIC_API_URL}/merchants/${competitor2_id}`).then((res) =>
		res.json()
	);

	const merchants: Merchant[] = [
		{
			id: competitor1_id,
			name: merchantData1.merchant_name
		},
		{
			id: competitor2_id,
			name: merchantData2.merchant_name
		}
	];

	return { merchants };
};
