/*
  Road to 1:35 — service worker
  Copyright (c) 2026 Antonio. All rights reserved. Proprietary; see LICENSE.
*/
const CACHE = 'road135-v2';
const ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icons/icon-180.png',
  './icons/icon-192.png',
  './icons/icon-512.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

/* Network-first for the page itself (so updates arrive), cache fallback offline.
   Cache-first for static assets (icons, manifest). */
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  // activities.json must always be fresh: network first, cached copy only
  // as an offline fallback, and never poisons the static cache.
  if (new URL(e.request.url).pathname.endsWith('/activities.json')) {
    e.respondWith(
      fetch(e.request)
        .then((r) => {
          const copy = r.clone();
          caches.open(CACHE).then((c) => c.put('./activities.json', copy));
          return r;
        })
        .catch(() => caches.match('./activities.json'))
    );
    return;
  }
  const isNav = e.request.mode === 'navigate' || e.request.destination === 'document';
  if (isNav) {
    e.respondWith(
      fetch(e.request)
        .then((r) => {
          const copy = r.clone();
          caches.open(CACHE).then((c) => c.put('./index.html', copy));
          return r;
        })
        .catch(() => caches.match('./index.html'))
    );
  } else {
    e.respondWith(
      caches.match(e.request).then((hit) => hit || fetch(e.request).then((r) => {
        const copy = r.clone();
        caches.open(CACHE).then((c) => c.put(e.request, copy));
        return r;
      }))
    );
  }
});
