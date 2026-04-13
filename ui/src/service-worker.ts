/// <reference types="@sveltejs/kit/types/ambient" />
/// <reference lib="webworker" />

import { build, files, version } from '$service-worker';

declare const self: ServiceWorkerGlobalScope;

const CACHE_NAME = `fqf-cache-${version}`;

// Static assets to pre-cache: the built app shell + any static files
const ASSETS = [...build, ...files];

// ── Install: pre-cache static shell ──────────────────────────────────────────
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches
            .open(CACHE_NAME)
            .then((cache) => cache.addAll(ASSETS))
            .then(() => self.skipWaiting())
    );
});

// ── Activate: delete old caches ───────────────────────────────────────────────
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches
            .keys()
            .then((keys) =>
                Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
            )
            .then(() => self.clients.claim())
    );
});

// ── Fetch: cache-first for static assets, network-first for API ───────────────
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Only handle same-origin requests
    if (url.origin !== self.location.origin) return;

    if (url.pathname.startsWith('/api/')) {
        // Network-first for API: try live response, fall back to cached (GET only)
        event.respondWith(
            fetch(request)
                .then((resp) => {
                    if (resp.ok && request.method === 'GET') {
                        const clone = resp.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
                    }
                    return resp;
                })
                .catch(() => caches.match(request).then((cached) => cached ?? Response.error()))
        );
    } else {
        // Cache-first for static assets
        event.respondWith(
            caches.match(request).then((cached) => {
                if (cached) return cached;
                return fetch(request).then((resp) => {
                    if (resp.ok) {
                        const clone = resp.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
                    }
                    return resp;
                });
            })
        );
    }
});
