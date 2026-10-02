"""Builds index.html (single-page trip site) from planning/leg*/ HTML files + data/*.
Run: python build_site.py   (index.html is generated: edit the sources instead)
Sources: planning/leg*/*.html (content), data/site.css, data/site.js (design + behaviour), data/places.js (saved places).
"""
import re
LEGS = [(1, 'planning/leg1-shinjuku/leg1-tokyo-shinjuku.html'), (2, 'planning/leg2-osaka/leg2-osaka-kyoto.html')]
# Leg 3 has no source file yet: add (3, 'planning/leg3-ueno/leg3-ueno.html') above and delete LEG3 below.
NEIGH = {1: ('Narita', 'Osaka'), 2: ('Shinjuku', 'Ueno'), 3: ('Osaka', 'Narita')}
# One colour per calendar day, from Tokyo Metro line colours.
LINE = {22: '#e0800a', 23: '#d4001a', 24: '#0095c8', 25: '#00946a', 26: '#7f5fc7',
        27: '#008f8b', 28: '#8c5528', 29: '#d63f86', 30: '#0068b0', 31: '#4f9e3f'}
LABEL = {'info': 'Info', 'steps': 'Steps', 'todo': 'To book'}


def conv(n, path):
    s = open(path, encoding='utf-8').read()
    kanji = re.search(r'class="kanji">(.*?)<', s).group(1)
    title = re.search(r'<h1>(.*?)</h1>', s).group(1)
    sub = re.search(r'<header>.*?<p>(.*?)</p>', s, re.S).group(1)
    main = re.search(r'<main>(.*?)</main>', s, re.S).group(1)
    js = re.findall(r'<script>(.*?)</script>', s, re.S)[-1]
    days = re.search(r'var days = (\{.*?\n  \});', js, re.S).group(1)
    hotel = re.search(r'var hotel = (\[.*?\]);', js).group(1)
    stops = re.search(r'var stops = (\{.*?\n  \});', js, re.S).group(1)
    cards = re.findall(r'(<div class="card" id="([^"]+)"[^>]*>.*?\n</div>)\n', main, re.S)
    info, dayc, rest, panels, daydates = [], [], [], [], {}
    for html, cid in cards:
        pid = 'l%d-%s' % (n, cid)
        m = re.search(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun), Oct (\d+)', html)
        body = re.sub(r'^<div class="card"[^>]*>', '', html)
        body = body[:body.rindex('</div>')]
        body = re.sub(r'id="map(\d)"', lambda x: 'id="l%d-map%s"' % (n, x.group(1)), body)
        attrs = ''
        if m and cid.startswith('day'):
            d = int(m.group(2))
            daydates[int(cid[3:])] = d
            body = re.sub(r'<div class="badge">.*?</div>', '<div class="badge">%d</div>' % d, body, count=1)
            attrs = ' data-date="2026-10-%02d" style="--c:%s"' % (d, LINE[d])
            dayc.append('<button data-p="%s" style="--c:%s"><b>%d</b><i>%s</i></button>' % (pid, LINE[d], d, m.group(1)))
        else:
            (info if cid == 'info' else rest).append('<button class="txt" data-p="%s">%s</button>' % (pid, LABEL.get(cid, cid)))
        panels.append('<article class="panel" id="%s"%s><div class="card">%s</div></article>' % (pid, attrs, body))
    prev, nxt = NEIGH[n]
    plate = ('<header class="plate"><div class="kanji">%s</div><div class="pl-main"><h1>%s</h1><p>%s</p></div>'
             '<div class="pl-nb"><span>&lsaquo; %s</span><span>%s &rsaquo;</span></div></header>') % (kanji, title, sub, prev, nxt)
    sec = '<section class="leg" id="leg%d">%s<nav class="chips">%s</nav><main>%s</main></section>' % (
        n, plate, ''.join(info + dayc + rest), ''.join(panels))
    colors = ','.join('%d:"%s"' % (d, LINE[dt]) for d, dt in daydates.items())
    data = 'LEGS[%d] = { days: %s, hotel: %s, stops: %s, colors: {%s} };' % (n, days, hotel, stops, colors)
    return sec, data


secs, datas = [], []
for n, p in LEGS:
    a, b = conv(n, p)
    secs.append(a)
    datas.append(b)

OVERVIEW = '''<section class="leg" id="leg0">
<header class="plate"><div class="kanji">日本</div><div class="pl-main"><h1>Japan 2026</h1><p>Harel &amp; Menashe &middot; Oct 21 &ndash; Nov 5</p></div></header>
<main>
<article class="panel on" id="ov"><div id="today"></div>
<div class="card"><h2>Route</h2><ol class="route-list">
<li><b>Oct 21</b> Fly TLV 19:45, land Narita Oct 22 13:20<small>El Al LY91</small></li>
<li><b>Oct 22&ndash;26</b> Shinjuku, Tokyo<small>Shinjuku Washington Hotel Annex</small><a href="tel:+81333433111">Call hotel</a></li>
<li><b>Oct 26&ndash;31</b> Osaka &amp; Kyoto<small>Hotel Geometiq Osaka Umeda &middot; paid</small><a href="tel:+81663111551">Call hotel</a></li>
<li><b>Oct 31&ndash;Nov 4</b> Ueno, Tokyo<small>APA Hotel Keisei Ueno-Ekimae &middot; plan coming</small><a href="tel:+81358466811">Call hotel</a></li>
<li><b>Nov 4</b> Fly Tokyo 23:00, land TLV Nov 5 06:30<small>Arkia IZ882 &middot; 1 bag + 1 trolley each. Ueno check-out is 10:00, so store bags.</small></li>
</ol></div>
<div class="card"><h2>Deadlines</h2><ul class="plain">
<li><b>~Oct 10</b> Shibuya Sky tickets open (for Oct 24)</li>
<li><b>Oct 20</b> Shinjuku hotel charged. Last free cancellation for Osaka (23:59 JST)</li>
<li><b>Oct 29</b> Ueno hotel charged</li></ul></div>
<div class="card"><h2>Using this guide</h2><ul class="plain">
<li>Pick a leg from the bar at the bottom, then a day from the chips at the top.</li>
<li>Tap a time to tick that stop off. Ticks are saved on this phone.</li>
<li>Under each map, "My location" shows where you are.</li></ul></div>
</article></main></section>'''

LEG3 = '''<section class="leg" id="leg3">
<header class="plate"><div class="kanji">上野</div><div class="pl-main"><h1>Ueno, Tokyo</h1><p>Sat Oct 31 &ndash; Wed Nov 4 &middot; 4 nights &middot; APA Hotel Keisei Ueno-Ekimae</p></div><div class="pl-nb"><span>&lsaquo; Osaka</span><span>Narita &rsaquo;</span></div></header>
<nav class="chips"><button class="txt" data-p="l3-info">Info</button></nav>
<main><article class="panel" id="l3-info" style="--c:#4f9e3f"><div class="card"><h2>Plan coming soon</h2><div class="date">This leg is not planned yet.</div>
<table>
<tr><td>Hotel</td><td>APA Hotel Keisei Ueno-Ekimae<br>Ueno, Taito-ku 2-14-26, Tokyo 110-0005<br><a href="tel:+81358466811">+81 3 5846 6811</a></td></tr>
<tr><td>Check-in / out</td><td>From 15:00 (Oct 31) / before 10:00 (Nov 4)</td></tr>
<tr><td>Booking</td><td>Charged Oct 29. Free cancellation until Oct 31 00:00.</td></tr>
<tr><td>Flight home</td><td>Arkia IZ882 leaves Nov 4 at 23:00, check-in around 20:00. Decide where bags go after check-out.</td></tr>
</table></div></article></main></section>'''

CSS = open('data/site.css', encoding='utf-8').read()
JS = open('data/site.js', encoding='utf-8').read()
PLACES = open('data/places.js', encoding='utf-8').read()
html = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#000000"><title>Japan 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>''' + CSS + '''</style></head><body>
''' + OVERVIEW + '\n' + '\n'.join(secs) + '\n' + LEG3 + '''
<nav class="tabbar" id="tabbar">
<button data-leg="0"><span class="ic">&#9679;</span>Overview</button>
<button data-leg="1"><span class="ic">新</span>Tokyo</button>
<button data-leg="2"><span class="ic">阪</span>Osaka</button>
<button data-leg="3" class="soon"><span class="ic">野</span>Ueno</button>
</nav>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
''' + PLACES + '\nvar LEGS = {};\n' + '\n'.join(datas) + '\n' + JS + '</script></body></html>'
open('index.html', 'w', encoding='utf-8').write(html)
