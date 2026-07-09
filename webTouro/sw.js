const CACHE_NAME = '12fogar-guide-cache-v1';
const ASSETS = [
  './',
  './index.html',
  './style.css',
  './app.js',
  './manifest.json',
  './assets/logo.jpg',
  './assets/maps-street.jpg',
  './assets/maps-details.jpg',
  './assets/maps-peru.jpg',
  './assets/mailbox-box.jpg'
];

// Install Event - Pre-cache all essential offline assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[Service Worker] Caching App Shell Assets');
        return cache.addAll(ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate Event - Clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            console.log('[Service Worker] Removing old cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event - Stale-while-revalidate strategy for seamless offline access
self.addEventListener('fetch', event => {
  // Only handle GET requests and standard HTTP schemes (ignore browser extensions, etc.)
  if (event.request.method !== 'GET') return;
  
  const isLocalRequest = event.request.url.startsWith(self.location.origin);

  if (!isLocalRequest) {
    // If it's an external resource (like weather api or google fonts), try network, and fallback to cache if available
    if (event.request.url.includes('api.open-meteo.com') || event.request.url.includes('fonts.googleapis.com') || event.request.url.includes('fonts.gstatic.com')) {
      event.respondWith(
        fetch(event.request)
          .catch(() => caches.match(event.request))
      );
    }
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(cachedResponse => {
        if (cachedResponse) {
          // Serve from cache, but fetch from network in background to update cache silently
          fetch(event.request)
            .then(networkResponse => {
              if (networkResponse.status === 200) {
                caches.open(CACHE_NAME).then(cache => cache.put(event.request, networkResponse));
              }
            }).catch(() => {/* Ignore network update errors offline */});
          
          return cachedResponse;
        }

        return fetch(event.request).then(networkResponse => {
          // Cache new requests dynamically
          if (networkResponse.status === 200) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, responseClone));
          }
          return networkResponse;
        });
      })
  );
});
