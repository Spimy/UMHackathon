import { PUBLIC_API_URL } from '$env/static/public';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch }) => {
	const competitor1_id = '2e8a5';
	const competitor2_id = '5c1f8';

	const merchantData1 = await fetch(`${PUBLIC_API_URL}/merchants/${competitor1_id}`).then((res) =>
		res.json()
	);
	const merchantData2 = await fetch(`${PUBLIC_API_URL}/merchants/${competitor2_id}`).then((res) =>
		res.json()
	);

	const reviewData1 = await fetch(
		`${PUBLIC_API_URL}/ollama/summarize_reviews/${competitor1_id}`
	).then((res) => res.json());
	const reviewData2 = await fetch(
		`${PUBLIC_API_URL}/ollama/summarize_reviews/${competitor2_id}`
	).then((res) => res.json());

	const merchant1ReviewSummary = reviewData1.review_summary;
	const merchant1Rating = String(Math.round(reviewData1.average_rating));
	const merchant2ReviewSummary = reviewData2.review_summary;
	const merchant2Rating = String(Math.round(reviewData2.average_rating));

	const merchants = [
		{
			id: competitor1_id,
			name: merchantData1.merchant_name,
			review_summary: merchant1ReviewSummary,
			rating: merchant1Rating
		},
		{
			id: competitor2_id,
			name: merchantData2.merchant_name,
			review_summary: merchant2ReviewSummary,
			rating: merchant2Rating
		}
	];

	return { merchants };
};
