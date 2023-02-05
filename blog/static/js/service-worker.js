// const initCache = () =>{
// 	caches.open(cachesName).then(cache => {
// 		cache.addAll(filesToCache);
// 	}), event => {
// 		console.log(event);
// 	};
// };


// self.addEventListener("install", event => {
// 	console.log('Cache opened');
// 	event.waitUntile(initCache());
// });

// self.addEventListener("activate", event => {
// 	event.waitUntile(
// 		caches.keys().then(keyList =>{
// 			return Promise.all(keyList.map((key) => {
// 				if (key !== cachesName) {
// 					return caches.delete(key)
// 				}
// 			}))
// 		})
// 	);
// });

self.addEventListener('install', event => {
    caches.open(cacheName)
      .then(function(cache) {
        console.log('Cache opened');
        return cache.addAll(filesToCache);
      })
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        if (response) {
          return response;
        } 
        return fetch(event.request);
      })
  );
});

self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.filter(function(cacheName) {
          return cacheName.startsWith('my-site-') && cacheName !== cacheName;
        }).map(function(cacheName) {
          return caches.delete(cacheName);
        })
      );
    })
  );
});
