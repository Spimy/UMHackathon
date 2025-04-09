import formsPlugin from '@tailwindcss/forms';
import typographyPlugin from '@tailwindcss/typography';
import { Config } from 'tailwindcss';

export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				primary: '#00B14F',
				secondary: '#000000',
				tertiary: '#FEFEFE',
				highlight: '#18481A'
			},
			fontFamily: {
				sans: ['Inter', 'sans-serif']
			},
			fontSize: {
				sm: [
					'0.75rem', // 12px
					{
						lineHeight: '1.125rem', // 18px
						fontWeight: '400'
					}
				],
				md: [
					'1.25rem', // 20px
					{
						lineHeight: 'normal',
						fontWeight: '400'
					}
				],
				mdsemi: [
					'1.25rem', // 20px
					{
						lineHeight: 'normal',
						fontWeight: '600'
					}
				],
				lgsemi: [
					'1.5rem', // 24px
					{
						lineHeight: 'normal',
						fontWeight: '600'
					}
				],
				xlsemi: [
					'1.875rem', // 30px
					{
						lineHeight: 'normal',
						fontWeight: '600'
					}
				],
				xxlsemi: [
					'2.75rem', // 44px
					{
						lineHeight: 'normal',
						fontWeight: '600'
					}
				],
				base: [
					'1rem', // 16px
					{
						lineHeight: 'normal',
						fontWeight: '600'
					}
				]
			}
		}
	},
	plugins: [formsPlugin, typographyPlugin]
} satisfies Config;
