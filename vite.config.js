import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from './src/node_modules/vite/dist/node';
import path from 'path';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		resolve: {
			alias: {
				$lib: path.resolve("./src/lib"),
			},
		},
	}
});
