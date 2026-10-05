// Saved restaurants, shops and sights. They appear on a day's map (toggle under the map)
// when they are within ~1.2 km of that day's route, or within 1 km of your location after you tap "My location".
// Add entries like:
// { name: "Ichiran Shinjuku", lat: 35.6938, lng: 139.7034, type: "food", leg: 1, note: "Solo ramen booths, open 24h", url: "https://maps.google.com/?q=Ichiran+Shinjuku" },
// type: "food" | "cafe" | "shop" | "sight"      leg: 1 (Tokyo), 2 (Osaka/Kyoto), 3 (Ueno) - optional
var PLACES = [
 {
  "name": "Sukiyaki Shabu-shabu Daibokujo",
  "lat": 34.6665,
  "lng": 135.5055,
  "type": "food",
  "note": "Black wagyu all-you-can-eat sukiyaki/shabu-shabu, Namba/Nipponbashi. Course ~¥4,980. Open 11:00-23:00.",
  "reel": "https://www.instagram.com/reel/DdbYiNVNP-Y/",
  "leg": 2
 },
 {
  "name": "Motohashi (watch dealer)",
  "lat": 35.644,
  "lng": 139.699,
  "type": "shop",
  "note": "Small neighbourhood watch shop in Nakameguro (Rolex, Patek, Seiko). Good stop on the Meguro river stroll.",
  "reel": "https://www.instagram.com/reel/DcTZnZeNB_B/"
 },
 {
  "name": "B.B Amemura flea market",
  "lat": 34.6724,
  "lng": 135.4989,
  "type": "shop",
  "note": "Vintage watch stalls in American Village, Osaka (Nishishinsaibashi).",
  "reel": "https://www.instagram.com/reel/DdBnaKJP2XX/",
  "leg": 2
 },
 {
  "name": "B.B Amemura flea market",
  "lat": 34.6724,
  "lng": 135.4989,
  "type": "shop",
  "note": "Second reel of the same vintage watch flea market in American Village.",
  "reel": "https://www.instagram.com/reel/DZpUKBvyal8/",
  "leg": 2
 },
 {
  "name": "Americamura (American Village)",
  "lat": 34.6717,
  "lng": 135.4985,
  "type": "shop",
  "note": "Osaka's best area for thrift shops, vintage clothes and street fashion.",
  "reel": "https://www.instagram.com/reel/Dc-vVNATzF8/",
  "leg": 2
 },
 {
  "name": "Osaka thrift shopping",
  "lat": 34.6717,
  "lng": 135.4985,
  "type": "shop",
  "note": "Osaka thrift stores with big flash sales. Same area as Americamura.",
  "reel": "https://www.instagram.com/reel/DVr0eQnk0iv/",
  "leg": 2
 },
 {
  "name": "BASEMENT coffee & sandwiches",
  "lat": 34.672,
  "lng": 135.4985,
  "type": "cafe",
  "note": "Lunch spot in Shinsaibashi BIGSTEP B2F, 3 min from Shinsaibashi Stn. 11:00-16:00, irregular holidays.",
  "reel": "https://www.instagram.com/reel/DdX_BV0yHEN/",
  "leg": 2
 },
 {
  "name": "Chermside Harajuku",
  "lat": 35.6715,
  "lng": 139.705,
  "type": "food",
  "note": "Steak sandwich everyone is talking about, Harajuku.",
  "reel": "https://www.instagram.com/reel/DcbJIeTp3p5/"
 },
 {
  "name": "Nikutarashi Umeda",
  "lat": 34.704,
  "lng": 135.5005,
  "type": "food",
  "note": "All-you-can-eat meat sushi + 150 izakaya dishes from ~¥2,500, Umeda.",
  "reel": "https://www.instagram.com/reel/DdTdII-uXik/",
  "leg": 2
 },
 {
  "name": "Yakiniku Marutomi Kyoto",
  "lat": 35.004,
  "lng": 135.77,
  "type": "food",
  "note": "Yakiniku in Kyoto, ~250 NIS for two. Book ahead (queues of 1.5h).",
  "reel": "https://www.instagram.com/reel/Dblj_lJILYg/",
  "leg": 2
 },
 {
  "name": "Soreyuke! Tori Yaro!",
  "lat": 34.709,
  "lng": 135.5015,
  "type": "food",
  "note": "Super cheap yakitori izakaya, Umeda/Chayamachi. Beer ¥299, skewers ¥99. 17:00-01:00.",
  "reel": "https://www.instagram.com/reel/Dc8DsOZTyhY/",
  "leg": 2
 },
 {
  "name": "Zauo Shibuya",
  "lat": 35.659,
  "lng": 139.699,
  "type": "food",
  "note": "Catch your own fish and have it cooked, Shibuya.",
  "reel": "https://www.instagram.com/reel/Da6CeXApv7d/"
 },
 {
  "name": "Kinpuku Sakaba",
  "lat": 35.6955,
  "lng": 139.703,
  "type": "food",
  "note": "Kabukicho izakaya, all-you-can-drink (sake and beer) ¥1,480. 5F Ricam Bldg.",
  "reel": "https://www.instagram.com/reel/DdBouj9S6NR/"
 },
 {
  "name": "Kinpuku Sakaba (second reel)",
  "lat": 35.6955,
  "lng": 139.703,
  "type": "food",
  "note": "Same Kabukicho spot: 2h all-you-can-drink ¥980, cheap yakitori.",
  "reel": "https://www.instagram.com/reel/DW80rzsyT3t/"
 },
 {
  "name": "Kitan Hibiki",
  "lat": 34.67,
  "lng": 135.501,
  "type": "food",
  "note": "Wagyu burger with great hospitality. Book before the trip.",
  "reel": "https://www.instagram.com/reel/DdU74BFSMYM/",
  "leg": 2
 },
 {
  "name": "Osaka: 5 must-eat spots (Kurogin, Tokito, Kitan Hibiki...)",
  "lat": 34.6665,
  "lng": 135.506,
  "type": "food",
  "note": "Tuna at Maguroya Kurogin, steak sandwich at Tokito, matcha at Matcha 587, melon ice cream at Kuromonmaru (Kuromon Market area).",
  "reel": "https://www.instagram.com/reel/DaFSecnsYQj/",
  "leg": 2
 },
 {
  "name": "Kichikichi Omurice",
  "lat": 35.0035,
  "lng": 135.769,
  "type": "food",
  "note": "Famous Kyoto omurice. Reel also lists Hikiniku to Come, Gokago, Gyoza Kazu, Beatle Momo.",
  "reel": "https://www.instagram.com/reel/DcZygTGPCmB/",
  "leg": 2
 },
 {
  "name": "Hikiniku to Come Kyoto",
  "lat": 35.005,
  "lng": 135.769,
  "type": "food",
  "note": "Wagyu minced-meat patties grilled in front of you, raw egg on the side. Reserve online.",
  "reel": "https://www.instagram.com/reel/DdJAoXwI362/",
  "leg": 2
 },
 {
  "name": "Hikiniku to Come Kyoto",
  "lat": 35.005,
  "lng": 135.769,
  "type": "food",
  "note": "Second reel: house-ground wagyu meatballs. Popular, reserve ahead.",
  "reel": "https://www.instagram.com/reel/Dcq6iaSxcgU/",
  "leg": 2
 },
 {
  "name": "Kanda butcher shop (yakiniku)",
  "lat": 35.6945,
  "lng": 139.7695,
  "type": "food",
  "note": "Cheap wagyu yakiniku, Kajicho, Kanda. Beer ¥190, kalbi ¥680. Fri 11:00-23:30, weekends from 16:00.",
  "reel": "https://www.instagram.com/reel/DVtRLqFCRA8/"
 },
 {
  "name": "FORNO Nishiazabu",
  "lat": 35.66,
  "lng": 139.722,
  "type": "food",
  "note": "Wood-fired Tottori wagyu, Nishiazabu near Roppongi. Mon-Sat 17:00-23:00. Pricey (¥10,000+).",
  "reel": "https://www.instagram.com/reel/DcLju5WFdUV/"
 },
 {
  "name": "Taishu Sakaba Muni",
  "lat": 35.0055,
  "lng": 135.771,
  "type": "food",
  "note": "Cheap standing-style izakaya on Kiyamachi, Kyoto. Craft beer ¥380. 17:00-23:00.",
  "reel": "https://www.instagram.com/reel/Dbaoywzjtbz/",
  "leg": 2
 },
 {
  "name": "Kokuryu Osaka",
  "lat": 34.6685,
  "lng": 135.501,
  "type": "food",
  "note": "Wagyu omakase near Dotonbori (20 dishes, ~¥19,800 dinner). Splurge.",
  "reel": "https://www.instagram.com/reel/DcgLYV7FIv9/",
  "leg": 2
 },
 {
  "name": "Gansan Sanjo",
  "lat": 35.009,
  "lng": 135.77,
  "type": "food",
  "note": "Wagyu course near Kawaramachi/Gion, Kyoto. ¥5,000+ pp, reserve on Tabelog. 17:00-23:00.",
  "reel": "https://www.instagram.com/reel/DbLOHsPDjnV/",
  "leg": 2
 },
 {
  "name": "Asahi Sky Room",
  "lat": 35.7108,
  "lng": 139.7966,
  "type": "sight",
  "note": "Free Asakusa view of Tokyo/Skytree, no minimum spend, ~$3 beers. Pairs with Senso-ji.",
  "reel": "https://www.instagram.com/reel/DbWGDmPO-zr/"
 },
 {
  "name": "Wagyu IDATEN",
  "lat": 34.666,
  "lng": 135.5,
  "type": "food",
  "note": "A5 wagyu layered beef boxes, 1 min from Namba Stn. 11:30-14:30, 17:00-21:30.",
  "reel": "https://www.instagram.com/reel/DZ1axohSJNt/",
  "leg": 2
 },
 {
  "name": "Kyoto Kanigin Kawaramachi",
  "lat": 35.0055,
  "lng": 135.7685,
  "type": "food",
  "note": "Crab restaurant, DECK by COAST 5F. 4-6 min from Kawaramachi Stn.",
  "reel": "https://www.instagram.com/reel/DcVHmvGSl-6/",
  "leg": 2
 },
 {
  "name": "Yoshitake (wagyu)",
  "lat": 34.681,
  "lng": 135.52,
  "type": "food",
  "note": "Wagyu sukiyaki, B1F Sanko Bldg, 1 min from Sakaisuji-Hommachi Stn.",
  "reel": "https://www.instagram.com/reel/DaKj_VPyjVF/",
  "leg": 2
 },
 {
  "name": "Yoshitake wagyu sukiyaki lunch",
  "lat": 34.681,
  "lng": 135.52,
  "type": "food",
  "note": "Second reel: lunch sukiyaki at the same restaurant.",
  "reel": "https://www.instagram.com/reel/DXvvIT4yO8E/",
  "leg": 2
 },
 {
  "name": "Yakiniku Rikimaru (Ohatsutenjin)",
  "lat": 34.7035,
  "lng": 135.5,
  "type": "food",
  "note": "All-you-can-eat wagyu yakiniku 90 min ¥5,478. Short walk from Umeda. Until 23:30.",
  "reel": "https://www.instagram.com/reel/DXjc796EfQI/",
  "leg": 2
 },
 {
  "name": "Coco Nemaru Ginza",
  "lat": 35.672,
  "lng": 139.765,
  "type": "food",
  "note": "Ginza wagyu in 450 g to ~1 kg cuts grilled in front of you, shareable.",
  "reel": "https://www.instagram.com/reel/DT2c7XPDbji/"
 },
 {
  "name": "Toyosu tuna auction tour",
  "lat": 35.645,
  "lng": 139.784,
  "type": "sight",
  "note": "World's biggest fish market. Arrive just before 5:00, taxi only (no public transport then). Tour via Airbnb/Klook.",
  "reel": "https://www.instagram.com/reel/DW3zMg6iLwe/"
 },
 {
  "name": "The Giant 3D Cat (Shinjuku)",
  "lat": 35.691,
  "lng": 139.702,
  "type": "sight",
  "note": "3D cat billboard at Shinjuku Stn east. Same reel: Godzilla Head, Kabukicho, Omoide Yokocho.",
  "reel": "https://www.instagram.com/reel/DY4vzXzohQk/"
 },
 {
  "name": "Godzilla Head",
  "lat": 35.6954,
  "lng": 139.7004,
  "type": "sight",
  "note": "Godzilla on the Hotel Gracery, Kabukicho. Near the Shinjuku hotel.",
  "reel": "https://www.instagram.com/reel/DY4vzXzohQk/"
 }
];
