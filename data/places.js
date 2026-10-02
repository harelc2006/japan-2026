// Saved restaurants, shops and sights. They appear on a day's map (toggle under the map)
// when they are within ~1.2 km of that day's route, or within 1 km of your location after you tap "My location".
// Add entries like:
// { name: "Ichiran Shinjuku", lat: 35.6938, lng: 139.7034, type: "food", leg: 1, note: "Solo ramen booths, open 24h", url: "https://maps.google.com/?q=Ichiran+Shinjuku" },
// type: "food" | "cafe" | "shop" | "sight"      leg: 1 (Tokyo), 2 (Osaka/Kyoto), 3 (Ueno) - optional
var PLACES = [];
