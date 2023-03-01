var cacheName = 'Cache-v2';
var filesToCache = [
	"/static/css/styles.css",
	"/static/js/index.js"
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(cacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
			console.log(Promise.all(cacheNames
												.filter(cacheName => (cacheName.startsWith("Cache-")))
												.filter(cacheName => (cacheName !== cacheName))
									));
            return Promise.all(
				
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("Cache-v")))
                    .filter(cacheName => (cacheName !== cacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('offline');
            })
    )
});

// self.addEventListener('install', event => {
//     caches.open(cacheName)
//       .then(function(cache) {
//         console.log('Cache opened');
//         return cache.addAll(filesToCache);
//       })
//     console.log('install');
// });

// self.addEventListener('fetch', event => {
//   event.respondWith(
//     caches.match(event.request)
//       .then(function(response) {
//         if (response) {
//           return response;
//         } 
//         return fetch(event.request);
//       })
//   );
//   console.log('fetch');
// });

// self.addEventListener('activate', event => {
//   event.waitUntil(
//     caches.keys().then(function(cacheNames) {
//       return Promise.all(
//         cacheNames.filter(function(cacheName) {
// 			console.log(cacheName.startsWith('Cache-') && cacheName !== cacheName);
// 			return cacheName.startsWith('Cache-') && cacheName !== cacheName;
//         }).map(function(cacheName) {
// 			console.log(cacheName);
//           	return caches.delete(cacheName);
//         })
//       );
//     })
//   );
// });

// self.addEventListener('load', () => {
//     if ('serviceWorker' in navigator) {
//       try {
//         registration = navigator.serviceWorker.register('index.js')
//         console.log('Service Worker registered: ', registration);
//       } catch (e){
//         console.error('Service Worker registration failed: ', e);
//       }
//     }
// });


// self.addEventListener('install', event => {
//     caches.open(cacheName)
//       .then(function(cache) {
//         console.log('Cache opened');
//         return cache.addAll(filesToCache);
//       })
// });

// self.addEventListener('activate', event => {
//     caches.open(cacheName)
//         .then(function(cache) {
//           console.log('Cache opened');
//           return cache.addAll(filesToCache);
//         })
// });

// self.addEventListener('fetch', event => {
// 	console.log('3')
// });