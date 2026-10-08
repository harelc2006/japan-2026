var C = "jp26-d9775c5c", PRE = ["./", "data/vendor/leaflet.js", "data/vendor/leaflet.css", "data/vendor/images/marker-icon.png", "data/vendor/images/marker-shadow.png", "data/vendor/images/layers.png"];
self.addEventListener("install", function (e) { e.waitUntil(caches.open(C).then(function (c) { return c.addAll(PRE); }).then(function () { return self.skipWaiting(); })); });
self.addEventListener("activate", function (e) { e.waitUntil(caches.keys().then(function (ks) { return Promise.all(ks.filter(function (k) { return k !== C && k !== "jp26-rt"; }).map(function (k) { return caches.delete(k); })); }).then(function () { return self.clients.claim(); })); });
self.addEventListener("fetch", function (e) {
  var r = e.request; if (r.method !== "GET") return;
  var same = new URL(r.url).origin === location.origin;
  e.respondWith(caches.match(r, { ignoreSearch: true }).then(function (hit) {
    if (hit && same) return hit;
    return fetch(r).then(function (res) {
      if (res && (res.ok || res.type === "opaque")) { var cp = res.clone(); caches.open("jp26-rt").then(function (c) { c.put(r, cp); }); }
      return res;
    }).catch(function () { return hit || caches.match("./"); });
  }));
});
