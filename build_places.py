"""Builds data/places.js from the curated list below (places seen on saved Instagram reels).
Run: python build_places.py && python build_site.py
Coordinates are approximate (neighbourhood level): verify the exact spot via the Google Maps link.
Fields: id = Instagram reel code, t = type, leg = 2 (Osaka/Kyoto) or omitted (Tokyo)."""
import json
P = [
 # id, name, lat, lng, type, leg, note
 ("DdbYiNVNP-Y","Sukiyaki Shabu-shabu Daibokujo",34.6665,135.5055,"food",2,"Black wagyu all-you-can-eat sukiyaki/shabu-shabu, Namba/Nipponbashi. Course ~¥4,980. Open 11:00-23:00."),
 ("DcTZnZeNB_B","Motohashi (watch dealer)",35.6440,139.6990,"shop",None,"Small neighbourhood watch shop in Nakameguro (Rolex, Patek, Seiko). Good stop on the Meguro river stroll."),
 ("DdBnaKJP2XX","B.B Amemura flea market",34.6724,135.4989,"shop",2,"Vintage watch stalls in American Village, Osaka (Nishishinsaibashi)."),
 ("DZpUKBvyal8","B.B Amemura flea market",34.6724,135.4989,"shop",2,"Second reel of the same vintage watch flea market in American Village."),
 ("Dc-vVNATzF8","Americamura (American Village)",34.6717,135.4985,"shop",2,"Osaka's best area for thrift shops, vintage clothes and street fashion."),
 ("DVr0eQnk0iv","Osaka thrift shopping",34.6717,135.4985,"shop",2,"Osaka thrift stores with big flash sales. Same area as Americamura."),
 ("DdX_BV0yHEN","BASEMENT coffee & sandwiches",34.6720,135.4985,"cafe",2,"Lunch spot in Shinsaibashi BIGSTEP B2F, 3 min from Shinsaibashi Stn. 11:00-16:00, irregular holidays."),
 ("DcbJIeTp3p5","Chermside Harajuku",35.6715,139.7050,"food",None,"Steak sandwich everyone is talking about, Harajuku."),
 ("DdTdII-uXik","Nikutarashi Umeda",34.7040,135.5005,"food",2,"All-you-can-eat meat sushi + 150 izakaya dishes from ~¥2,500, Umeda."),
 ("Dblj_lJILYg","Yakiniku Marutomi Kyoto",35.0040,135.7700,"food",2,"Yakiniku in Kyoto, ~250 NIS for two. Book ahead (queues of 1.5h)."),
 ("Dc8DsOZTyhY","Soreyuke! Tori Yaro!",34.7090,135.5015,"food",2,"Super cheap yakitori izakaya, Umeda/Chayamachi. Beer ¥299, skewers ¥99. 17:00-01:00."),
 ("Da6CeXApv7d","Zauo Shibuya",35.6590,139.6990,"food",None,"Catch your own fish and have it cooked, Shibuya."),
 ("DdBouj9S6NR","Kinpuku Sakaba",35.6955,139.7030,"food",None,"Kabukicho izakaya, all-you-can-drink (sake and beer) ¥1,480. 5F Ricam Bldg."),
 ("DW80rzsyT3t","Kinpuku Sakaba (second reel)",35.6955,139.7030,"food",None,"Same Kabukicho spot: 2h all-you-can-drink ¥980, cheap yakitori."),
 ("DdU74BFSMYM","Kitan Hibiki",34.6700,135.5010,"food",2,"Wagyu burger with great hospitality. Book before the trip."),
 ("DaFSecnsYQj","Osaka: 5 must-eat spots (Kurogin, Tokito, Kitan Hibiki...)",34.6665,135.5060,"food",2,"Tuna at Maguroya Kurogin, steak sandwich at Tokito, matcha at Matcha 587, melon ice cream at Kuromonmaru (Kuromon Market area)."),
 ("DcZygTGPCmB","Kichikichi Omurice",35.0035,135.7690,"food",2,"Famous Kyoto omurice. Reel also lists Hikiniku to Come, Gokago, Gyoza Kazu, Beatle Momo."),
 ("DdJAoXwI362","Hikiniku to Come Kyoto",35.0050,135.7690,"food",2,"Wagyu minced-meat patties grilled in front of you, raw egg on the side. Reserve online."),
 ("Dcq6iaSxcgU","Hikiniku to Come Kyoto",35.0050,135.7690,"food",2,"Second reel: house-ground wagyu meatballs. Popular, reserve ahead."),
 ("VtRLqFCRA8".replace("VtRLqFCRA8","DVtRLqFCRA8"),"Kanda butcher shop (yakiniku)",35.6945,139.7695,"food",None,"Cheap wagyu yakiniku, Kajicho, Kanda. Beer ¥190, kalbi ¥680. Fri 11:00-23:30, weekends from 16:00."),
 ("DcLju5WFdUV","FORNO Nishiazabu",35.6600,139.7220,"food",None,"Wood-fired Tottori wagyu, Nishiazabu near Roppongi. Mon-Sat 17:00-23:00. Pricey (¥10,000+)."),
 ("Dbaoywzjtbz","Taishu Sakaba Muni",35.0055,135.7710,"food",2,"Cheap standing-style izakaya on Kiyamachi, Kyoto. Craft beer ¥380. 17:00-23:00."),
 ("DcgLYV7FIv9","Kokuryu Osaka",34.6685,135.5010,"food",2,"Wagyu omakase near Dotonbori (20 dishes, ~¥19,800 dinner). Splurge."),
 ("DbLOHsPDjnV","Gansan Sanjo",35.0090,135.7700,"food",2,"Wagyu course near Kawaramachi/Gion, Kyoto. ¥5,000+ pp, reserve on Tabelog. 17:00-23:00."),
 ("DbWGDmPO-zr","Asahi Sky Room",35.7108,139.7966,"sight",None,"Free Asakusa view of Tokyo/Skytree, no minimum spend, ~$3 beers. Pairs with Senso-ji."),
 ("DZ1axohSJNt","Wagyu IDATEN",34.6660,135.5000,"food",2,"A5 wagyu layered beef boxes, 1 min from Namba Stn. 11:30-14:30, 17:00-21:30."),
 ("DcVHmvGSl-6","Kyoto Kanigin Kawaramachi",35.0055,135.7685,"food",2,"Crab restaurant, DECK by COAST 5F. 4-6 min from Kawaramachi Stn."),
 ("DaKj_VPyjVF","Yoshitake (wagyu)",34.6810,135.5200,"food",2,"Wagyu sukiyaki, B1F Sanko Bldg, 1 min from Sakaisuji-Hommachi Stn."),
 ("DXvvIT4yO8E","Yoshitake wagyu sukiyaki lunch",34.6810,135.5200,"food",2,"Second reel: lunch sukiyaki at the same restaurant."),
 ("DXjc796EfQI","Yakiniku Rikimaru (Ohatsutenjin)",34.7035,135.5000,"food",2,"All-you-can-eat wagyu yakiniku 90 min ¥5,478. Short walk from Umeda. Until 23:30."),
 ("DT2c7XPDbji","Coco Nemaru Ginza",35.6720,139.7650,"food",None,"Ginza wagyu in 450 g to ~1 kg cuts grilled in front of you, shareable."),
 ("DW3zMg6iLwe","Toyosu tuna auction tour",35.6450,139.7840,"sight",None,"World's biggest fish market. Arrive just before 5:00, taxi only (no public transport then). Tour via Airbnb/Klook."),
 ("DY4vzXzohQk","The Giant 3D Cat (Shinjuku)",35.6910,139.7020,"sight",None,"3D cat billboard at Shinjuku Stn east. Same reel: Godzilla Head, Kabukicho, Omoide Yokocho."),
 ("DY4vzXzohQk","Godzilla Head",35.6954,139.7004,"sight",None,"Godzilla on the Hotel Gracery, Kabukicho. Near the Shinjuku hotel."),

 (None,"Uobei Shibuya Dogenzaka",35.6590,139.6985,"food",None,"Conveyor-belt sushi ordered on a touchscreen, fast belt, very cheap. From the Hoang Pham guide. Walk-in."),
 (None,"Ichiran Ramen (Shibuya)",35.6598,139.7005,"food",None,"Solo-booth tonkotsu ramen, tick your own order sheet. From the guide. Open late."),
 (None,"The French Toast Factory Akihabara",35.6985,139.7730,"food",None,"Thick French toast brunch near Akihabara. From the guide. Go at opening."),
 (None,"Butaichi Hokkaido Banya Ikebukuro",35.7295,139.7110,"food",None,"Hokkaido butadon pork bowls, Ikebukuro. From the guide."),
 (None,"Gyukatsu Kyoto Katsugyu (Shijo Kawaramachi)",35.0035,135.7690,"food",2,"Beef cutlet cooked on your own hot stone. From the guide. Queue at dinner."),
 (None,"Menbaka Fire Ramen",35.0140,135.7480,"food",2,"Ramen served with a flaming oil show, Kyoto. From the guide. Book a slot."),
 (None,"551 Horai Honten (Namba)",34.6660,135.5018,"food",2,"Famous Osaka pork buns, takeaway. From the guide. Also at Kyoto Station."),
 (None,"Matsusaka M Sennichimae",34.6660,135.5040,"food",2,"Matsusaka wagyu yakiniku, Namba. From the guide."),
 (None,"Udon Tamatama (Namba)",34.6655,135.5030,"food",2,"Udon shop near Namba. From the guide."),
 (None,"Rikuro's Namba Cheesecake",34.6665,135.5010,"food",2,"Jiggly warm Japanese cheesecake, Namba. From the guide."),
]
out = []
for i, n, la, ln, t, leg, note in P:
    d = {"name": n, "lat": la, "lng": ln, "type": t, "note": note, "reel": "https://www.instagram.com/reel/%s/" % i}
    if not i: del d["reel"]
    if leg: d["leg"] = leg
    out.append(d)
hdr = open('data/places.js', encoding='utf-8').read().split('var PLACES')[0]
open('data/places.js', 'w', encoding='utf-8').write(hdr + 'var PLACES = ' + json.dumps(out, ensure_ascii=False, indent=1) + ';\n')
print(len(out), 'places')
