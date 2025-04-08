import { sveltekit } from '@sveltejs/kit/vite';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	server: {
		watch: {
			usePolling: true,
			ignored: ['**/node_modules/**']
		},
		host: '0.0.0.0',
		port: 5173,
		strictPort: true
	}
});
