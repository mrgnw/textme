import adapter from '@sveltejs/adapter-cloudflare';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { defineConfig } from 'vite';
import { sveltekit } from '@sveltejs/kit/vite';
import Icons from 'unplugin-icons/vite';

export default defineConfig({
  plugins: [
    sveltekit({
      preprocess: vitePreprocess(),
      adapter: adapter({ platformProxy: { persist: false } }),
      compilerOptions: { experimental: { async: true } },
      experimental: { remoteFunctions: true }
    }),
    Icons({ compiler: 'svelte' })
  ]
})
