// self.addEventListener('install', event => {
//     caches.open(cacheName)
//       .then(function(cache) {
//         console.log('Cache opened');
//         return cache.addAll(filesToCache);
//       })
//     // console.log('install');
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
//   // console.log('fetch');
// });

// self.addEventListener('activate', event => {
//   event.waitUntil(
//     caches.keys().then(function(cacheNames) {
//       return Promise.all(
//         cacheNames.filter(function(cacheName) {
//           return cacheName.startsWith('my-site-') && cacheName !== cacheName;
//         }).map(function(cacheName) {
//           return caches.delete(cacheName);
//         })
//       );
//     })
//   );
//   // console.log('activ');
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
var cacheName = 'Cache-v1';
var filesToCache = [
	"/static/css/styles.css",
	"/static/js/index.js"
];

self.addEventListener('install', event => {
    caches.open(cacheName)
      .then(function(cache) {
        console.log('Cache opened');
        return cache.addAll(filesToCache);
      })
});

self.addEventListener('activate', event => {
	console.log('2')
});

self.addEventListener('fetch', event => {
	console.log('3')
});