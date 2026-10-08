var TILES = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}";
var $ = function (s, r) { return (r || document).querySelector(s); };
var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
var store = {
  get: function (k) { try { return localStorage.getItem("jp26:" + k); } catch (e) { return null; } },
  set: function (k, v) { try { v ? localStorage.setItem("jp26:" + k, "1") : localStorage.removeItem("jp26:" + k); } catch (e) {} }
};
var ICONS = { food: "🍜", cafe: "☕", shop: "🛍", sight: "⛩" };
var maps = {}, user = null;

function city(x) { return x[3] || "Tokyo"; }
function gm(name, c) { return "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(name + " " + c); }
function pinIcon(color, text) {
  return L.divIcon({ className: "", html: '<div class="pin" style="--c:' + color + '"><span>' + text + '</span></div>', iconSize: [30, 30], iconAnchor: [15, 34], popupAnchor: [0, -32] });
}
function km(a, b) {
  var R = 6371, r = Math.PI / 180, dLat = (b[0] - a[0]) * r, dLng = (b[1] - a[1]) * r;
  var h = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(a[0] * r) * Math.cos(b[0] * r) * Math.sin(dLng / 2) * Math.sin(dLng / 2);
  return 2 * R * Math.asin(Math.sqrt(h));
}

/* ---- Maps: one per day, created when the day is first opened ---- */
var llState = 0, llQ = [];
function withLeaflet(fn) {
  if (window.L) return fn();
  llQ.push(fn);
  if (llState) return;
  llState = 1;
  var l = document.createElement("link"); l.rel = "stylesheet"; l.href = "data/vendor/leaflet.css"; document.head.appendChild(l);
  var s = document.createElement("script"); s.src = "data/vendor/leaflet.js";
  s.onload = function () { var q = llQ; llQ = []; q.forEach(function (f) { f(); }); };
  s.onerror = function () { llState = 0; };
  document.head.appendChild(s);
}
function buildMap(n, d) { withLeaflet(function () { buildMap0(n, d); }); }
function buildMap0(n, d) {
  var key = n + "-" + d, el = document.getElementById("l" + n + "-map" + d);
  if (!el || maps[key]) return;
  var leg = LEGS[n], hotel = leg.hotel, color = leg.colors[d], list = leg.stops[d];
  var map = L.map(el), pts = [[hotel[1], hotel[2]]];
  maps[key] = map;
  L.tileLayer(TILES, { maxZoom: 19, attribution: "Tiles &copy; Esri" }).addTo(map);
  L.marker(pts[0], { icon: pinIcon("#17233a", "H"), zIndexOffset: 1000 })
    .bindPopup("<b>" + hotel[0] + "</b><br>Hotel<br><a href='" + gm(hotel[0], city(hotel)) + "' target='_blank' rel='noopener'>Open in Google Maps</a>").addTo(map);
  list.forEach(function (s, i) {
    pts.push([s[1], s[2]]);
    L.marker([s[1], s[2]], { icon: pinIcon(color, i + 1) })
      .bindPopup("<b>" + s[0] + "</b><br>Stop " + (i + 1) + "<br><a href='" + gm(s[0], city(s)) + "' target='_blank' rel='noopener'>Open in Google Maps</a>").addTo(map);
  });
  L.polyline(pts, { color: color, weight: 4, opacity: 0.6, dashArray: "6 8" }).addTo(map);
  map.fitBounds(pts, { padding: [30, 30] });

  var tools = document.createElement("div");
  tools.className = "maptools";
  var loc = document.createElement("button");
  loc.textContent = "My location";
  tools.appendChild(loc);
  el.parentNode.insertBefore(tools, el.nextSibling);

  var layer = L.layerGroup(), box = null, centers = pts.slice();
  function renderPlaces() {
    layer.clearLayers();
    var shown = 0;
    (window.PLACES || []).forEach(function (p) {
      if (p.leg && p.leg !== n) return;
      var near = centers.some(function (c, i) { return km(c, [p.lat, p.lng]) <= (i >= pts.length ? 1.5 : 2.5); });
      if (!near) return;
      shown++;
      L.marker([p.lat, p.lng], { icon: L.divIcon({ className: "", html: '<div class="pl">' + (ICONS[p.type] || "📍") + "</div>", iconSize: [26, 26], iconAnchor: [13, 13] }) })
        .bindPopup("<b>" + p.name + "</b>" + (p.note ? "<br>" + p.note : "") + (p.reel ? "<br><a href='" + p.reel + "' target='_blank' rel='noopener'>▶ Watch the reel</a>" : "") + "<br><a href='" + (p.url || gm(p.name, city(hotel))) + "' target='_blank' rel='noopener'>Open in Google Maps</a>").addTo(layer);
    });
    if (shown && !box) {
      box = document.createElement("label");
      box.innerHTML = '<input type="checkbox" checked> Saved places';
      tools.appendChild(box);
      $("input", box).onchange = function () { this.checked ? map.addLayer(layer) : map.removeLayer(layer); };
      map.addLayer(layer);
    }
  }
  renderPlaces();
  loc.onclick = function () {
    if (!navigator.geolocation) { loc.textContent = "Location not available"; return; }
    loc.textContent = "Locating...";
    navigator.geolocation.getCurrentPosition(function (pos) {
      user = [pos.coords.latitude, pos.coords.longitude];
      L.circleMarker(user, { radius: 8, color: "#fff", weight: 3, fillColor: "#0068b0", fillOpacity: 1 }).addTo(map);
      centers = pts.concat([user]);
      renderPlaces();
      map.fitBounds(pts.concat([user]), { padding: [30, 30] });
      loc.textContent = "My location";
    }, function () { loc.textContent = "Location blocked. Allow it in browser settings."; }, { enableHighAccuracy: true, timeout: 10000 });
  };
}

/* Route buttons (Google Maps transit directions, built from stops) */
Object.keys(LEGS).forEach(function (n) {
  var leg = LEGS[n];
  $$("#leg" + n + " a.route").forEach(function (a) {
    var list = leg.stops[a.dataset.day];
    var names = list.map(function (s) { return s[0].replace(" (optional)", "") + " " + city(s); });
    var dest = names[names.length - 1], way = names.slice(0, -1);
    a.href = "https://www.google.com/maps/dir/?api=1&travelmode=transit&origin=" + encodeURIComponent(leg.hotel[0] + " " + city(leg.hotel)) +
      "&destination=" + encodeURIComponent(dest) + (way.length ? "&waypoints=" + encodeURIComponent(way.join("|")) : "");
  });
});

/* ---- Tick-off: stops and checklist items, saved on the phone ---- */
$$(".panel").forEach(function (p) {
  $$(".slot", p).forEach(function (s, i) {
    var k = p.id + "-s" + i, t = $(".time", s);
    if (!t) return;
    var b = document.createElement("button");
    b.className = "time"; b.type = "button"; b.innerHTML = t.innerHTML; b.title = "Tap to tick off";
    s.replaceChild(b, t);
    if (store.get(k)) s.classList.add("done");
    b.onclick = function () { s.classList.toggle("done"); store.set(k, s.classList.contains("done")); };
  });
  var uls = p.id.slice(-4) === "todo" ? $$("ul", p) : [];
  if (uls.length) {
    uls.forEach(function (u) { u.className = "checks"; });
    $$("li", p).forEach(function (li, i) {
      var k = p.id + "-c" + i, box = document.createElement("input");
      box.type = "checkbox"; box.checked = !!store.get(k);
      li.innerHTML = "<span>" + li.innerHTML + "</span>"; li.insertBefore(box, li.firstChild);
      li.classList.toggle("done", box.checked);
      li.onclick = function (e) { if (e.target !== box) box.checked = !box.checked; li.classList.toggle("done", box.checked); store.set(k, box.checked); };
    });
  }
});

/* ---- Navigation: legs on the bottom bar, panels on the chips ---- */
function showPanel(n, id) {
  var sec = document.getElementById("leg" + n);
  $$(".panel", sec).forEach(function (p) { p.classList.toggle("on", p.id === id); });
  $$(".chips button", sec).forEach(function (b) {
    var on = b.dataset.p === id;
    b.classList.toggle("on", on);
    if (on) b.scrollIntoView({ inline: "center", block: "nearest" });
  });
  var m = /-day(\d)$/.exec(id);
  if (m && LEGS[n]) buildMap(n, m[1]);
  if (m && maps[n + "-" + m[1]]) maps[n + "-" + m[1]].invalidateSize();
  history.replaceState(null, "", "#" + id);
  window.scrollTo(0, 0);
}
function showLeg(n, panel) {
  $$(".leg").forEach(function (s) { s.classList.toggle("on", s.id === "leg" + n); });
  $$("#tabbar button").forEach(function (b) { b.classList.toggle("on", b.dataset.leg === String(n)); });
  if (n === 0) { history.replaceState(null, "", "#leg0"); window.scrollTo(0, 0); return; }
  var sec = document.getElementById("leg" + n);
  var cur = $(".panel.on", sec);
  showPanel(n, panel || (cur && cur.id) || "l" + n + "-info");
}
$$("#tabbar button").forEach(function (b) { b.onclick = function () { showLeg(+b.dataset.leg); }; });
$$(".chips button").forEach(function (b) {
  b.onclick = function () { showPanel(+b.closest(".leg").id.slice(3), b.dataset.p); };
});

/* ---- Today card on the overview ---- */
(function () {
  var now = new Date(), iso = now.getFullYear() + "-" + ("0" + (now.getMonth() + 1)).slice(-2) + "-" + ("0" + now.getDate()).slice(-2);
  var hits = $$('.panel[data-date="' + iso + '"]'), host = $("#today"), todayPanel = null;
  var start = new Date(2026, 9, 21), left = Math.ceil((start - new Date(now.getFullYear(), now.getMonth(), now.getDate())) / 864e5);
  if (hits.length) {
    todayPanel = hits[hits.length - 1];
    var title = $("h2", todayPanel).textContent, color = getComputedStyle(todayPanel).getPropertyValue("--c");
    host.innerHTML = '<div class="card today-card" style="--c:' + color + '"><h2>Today</h2><div class="date">' + title + '</div><button type="button">Open today</button></div>';
    $("button", host).onclick = function () { showLeg(+todayPanel.id.charAt(1), todayPanel.id); };
  } else if (left > 0) {
    host.innerHTML = '<div class="card today-card"><h2>' + left + (left === 1 ? " day" : " days") + ' to go</h2><div class="date">Flight LY91 leaves Ben Gurion Oct 21 at 19:45.</div></div>';
  }
  var h = location.hash.slice(1), m = /^l(\d)-/.exec(h);
  if (m && document.getElementById(h)) showLeg(+m[1], h);
  else if (/^leg[1-3]$/.test(h)) showLeg(+h.charAt(3));
  else if (todayPanel) showLeg(+todayPanel.id.charAt(1), todayPanel.id);
  else showLeg(0);
})();

/* Hebrew via Google Translate (cookie googtrans). Button in the tab bar toggles it. */
(function () {
  var he = /googtrans=\/en\/iw/.test(document.cookie);
  var btn = document.getElementById("heBtn");
  function setCookie(v) {
    var c = "googtrans=" + v + "; path=/";
    document.cookie = c;
    document.cookie = c + "; domain=" + location.hostname;
  }
  btn.classList.toggle("on", he);
  btn.querySelector("span.t").textContent = he ? "English" : "עברית";
  btn.querySelector("span.ic").textContent = he ? "EN" : "א";
  btn.onclick = function () {
    if (he) { setCookie("/en/en"); document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/"; }
    else setCookie("/en/iw");
    location.reload();
  };
  if (he) {
    document.documentElement.dir = "rtl";
    var HD = { Sun: "א׳", Mon: "ב׳", Tue: "ג׳", Wed: "ד׳", Thu: "ה׳", Fri: "ו׳", Sat: "ש׳" };
    var HF = { Sun: "יום ראשון", Mon: "יום שני", Tue: "יום שלישי", Wed: "יום רביעי", Thu: "יום חמישי", Fri: "יום שישי", Sat: "שבת" };
    var MO = { Oct: "באוקטובר", Nov: "בנובמבר" };
    $$(".chips button i").forEach(function (e) { if (HD[e.textContent]) { e.textContent = HD[e.textContent]; e.setAttribute("translate", "no"); } });
    var w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT), n, list = [];
    while ((n = w.nextNode())) if (/(Sun|Mon|Tue|Wed|Thu|Fri|Sat), (Oct|Nov) \d+/.test(n.nodeValue)) list.push(n);
    list.forEach(function (n) {
      n.nodeValue = n.nodeValue.replace(/(Sun|Mon|Tue|Wed|Thu|Fri|Sat), (Oct|Nov) (\d+)/g, function (m, d, mo, x) { return HF[d] + ", " + x + " " + MO[mo]; });
    });
    window.googleTranslateElementInit = function () {
      new google.translate.TranslateElement({ pageLanguage: "en", includedLanguages: "iw", autoDisplay: false }, "gte");
    };
    var s = document.createElement("script");
    s.src = "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
    document.body.appendChild(s);
  }
})();

if ("serviceWorker" in navigator) {
  var hadSW = !!navigator.serviceWorker.controller;
  navigator.serviceWorker.addEventListener("controllerchange", function () {
    if (!hadSW) { hadSW = true; return; }
    if (document.getElementById("updbar")) return;
    var b = document.createElement("button");
    b.id = "updbar";
    b.textContent = "New version available. Tap to reload";
    b.style.cssText = "position:fixed;left:12px;right:12px;bottom:76px;z-index:9999;padding:12px;border:0;border-radius:10px;background:#222;color:#fff;font:600 15px sans-serif;box-shadow:0 2px 10px rgba(0,0,0,.4)";
    b.onclick = function () { location.reload(); };
    document.body.appendChild(b);
  });
  window.addEventListener("load", function () { navigator.serviceWorker.register("sw.js").catch(function () {}); });
}

/* strict clock times: first HH:MM only, zero-padded */
$$(".time").forEach(function (t) {
  var m = t.textContent.match(/(\d{1,2}):(\d{2})/);
  if (m) t.innerHTML = '<span class="tm">' + (m[1].length < 2 ? "0" : "") + m[1] + ":" + m[2] + '</span>';
});
