import formsPlugin from '@tailwindcss/forms';
import typographyPlugin from '@tailwindcss/typography';
import { Config } from 'tailwindcss';

export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				primary: '#3B9663',
				secondary: '#000000',
				tertiary: '#FEFEFE',
				highlight: '#18481A',
				bentoPurple: '#9F9FF8',
				bentoDark: '#252828',
				bentoLightBlue: '#92BFFF'
			},
			fontFamily: {
				sans: ['Inter', 'sans-serif']
			},
			keyframes: {
				pulse: {
					'0%, 40%, 100%': {
						opacity: '0.3',
						transform: 'scale(0.85)'
					},
					'20%': {
						opacity: '1',
						transform: 'scale(1)'
					}
				}
			},
			animation: {
				'dot-pulse': 'pulse 1.5s infinite'
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
