console.log('Service worker loaded');

const CACHE_NAME = 'Cache-v1';
const urlsToCache = [
	"/static/css/styles.css",
	"/static/js/index.js"
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Cache opened');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('activate', function(event) {
    event.waitUntil(
      caches.keys().then(function(cacheNames) {
        return Promise.all(
          cacheNames.map(function(cache) {
            if (cache !== CACHE_NAME) {
              console.log('Deleting old cache:', cache);
              return caches.delete(cache);
            }
          })
        );
      })
    );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        if (response) {
          console.log('Serving from cache');
          return response;
        }
        console.log('Not found in cache. Fetching from network');
        return fetch(event.request);
      }
    )
  );
});
