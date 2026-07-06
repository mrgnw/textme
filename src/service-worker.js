/// <reference types="@sveltejs/kit" />
/// <reference no-default-lib="true"/>
/// <reference lib="esnext" />
/// <reference lib="webworker" />

import { build, files, version } from '$service-worker';

// Gives `self` the correct service-worker types.
const sw = /** @type {ServiceWorkerGlobalScope} */ (/** @type {unknown} */ (globalThis.self));

const CACHE = `textme-${version}`;
const ASSETS = [...build, ...files];

sw.addEventListener('install', (event) => {
	event.waitUntil(
		caches
			.open(CACHE)
			.then((cache) => cache.addAll([...ASSETS, '/']))
			.then(() => sw.skipWaiting())
	);
});

sw.addEventListener('activate', (event) => {
	event.waitUntil(
		caches
			.keys()
			.then((keys) => Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key))))
			.then(() => sw.clients.claim())
	);
});

sw.addEventListener('fetch', (event) => {
	if (event.request.method !== 'GET') return;
	const url = new URL(event.request.url);
	if (url.origin !== sw.location.origin) return;
	if (url.pathname.startsWith('/api/')) return;
	event.respondWith(respond(event.request, url));
});

/**
 * Cache-first for immutable build/static assets, network-first for everything
 * else, with the cached `/` shell as the offline navigation fallback.
 * @param {Request} request
 * @param {URL} url
 */
async function respond(request, url) {
	const cache = await caches.open(CACHE);

	if (ASSETS.includes(url.pathname)) {
		const cached = await cache.match(url.pathname);
		if (cached) return cached;
	}

	try {
		const response = await fetch(request);
		// Non-Response means offline; treat it as a failure so the cache can answer.
		if (!(response instanceof Response)) throw new Error('offline');
		if (request.mode === 'navigate' && url.pathname === '/' && response.ok) {
			cache.put('/', response.clone());
		}
		return response;
	} catch (error) {
		// ponytail: any offline navigation gets the '/' shell; per-slug offline pages if anyone asks
		if (request.mode === 'navigate') {
			const shell = await cache.match('/');
			if (shell) return shell;
		}
		const cached = await cache.match(request);
		if (cached) return cached;
		throw error;
	}
}
