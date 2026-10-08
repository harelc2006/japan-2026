"""Builds index.html (single-page trip site) from planning/leg*/ HTML files + data/*.
Run: python build_site.py   (index.html is generated: edit the sources instead)
Sources: planning/leg*/*.html (content), data/site.css, data/site.js (design + behaviour), data/places.js (saved places).
"""
import re
LEGS = [(1, 'planning/leg1-shinjuku/leg1-tokyo-shinjuku.html'), (2, 'planning/leg2-osaka/leg2-osaka-kyoto.html'),
        (3, 'planning/leg3-ueno/leg3-ueno.html')]
NEIGH = {1: ('Narita', 'Osaka'), 2: ('Shinjuku', 'Ueno'), 3: ('Osaka', 'Narita')}
# One colour per calendar day, from Tokyo Metro line colours.
# Keys are month*100+day (Oct 22 = 1022, Nov 1 = 1101).
LINE = {1022: '#e0800a', 1023: '#d4001a', 1024: '#0095c8', 1025: '#00946a', 1026: '#7f5fc7',
        1027: '#008f8b', 1028: '#8c5528', 1029: '#d63f86', 1030: '#0068b0', 1031: '#4f9e3f',
        1101: '#b6007a', 1102: '#c1a470', 1103: '#00a7db', 1104: '#9b7cb6'}
LABEL = {'info': 'Info', 'steps': 'Steps', 'todo': 'To book'}

STOPW = set('the a of and in at to optional temple shrine park street market garden gardens museum station'.split())
# Manual pin -> slot-title overrides where fuzzy matching is wrong: (leg, day, pin) -> text in slot title
PIN_SLOT = {(3, 5, 4): 'Collect bags', (1, 2, 5): 'Cat Street', (2, 3, 1): 'Osaka Water Bus'}


def _toks(t):
    t = re.sub(r'<[^>]+>', ' ', t).replace('&amp;', '&').lower()
    return set(w for w in re.findall(r'[a-z0-9]+', t) if w not in STOPW)


def number_slots(n, d, body, names):
    """Prefix each timeline slot with the number of the map pin(s) it matches."""
    slots = list(re.finditer(r'<div class="slot">.*?</div></div>', body, re.S))
    info = []
    for m in slots:
        b = re.search(r'<b>(.*?)</b>', m.group(0), re.S)
        title = b.group(1) if b else ''
        info.append((m, title, _toks(title), _toks(m.group(0)), 'class="tag move"' in m.group(0)))
    assign = {}
    for i, name in enumerate(names):
        pt = _toks(re.sub(r'\(.*?\)', '', name))
        if not pt:
            continue
        ov = PIN_SLOT.get((n, d, i + 1))
        best = None
        if ov:
            best = next((k for k, x in enumerate(info) if ov in x[1]), None)
        else:
            for tier in (2, 3):
                cand = []
                for k, x in enumerate(info):
                    sc = len(pt & (x[2] if tier == 2 else x[3])) / len(pt)
                    if sc >= (0.5 if tier == 2 else 0.7):
                        cand.append((-sc, x[4], k))
                if cand:
                    best = sorted(cand)[0][2]
                    break
        if best is not None:
            assign.setdefault(best, []).append(i + 1)
        else:
            print('  no slot for pin', n, d, i + 1, name)
    out, last = [], 0
    for k, (m, *_r) in enumerate(info):
        out.append(body[last:m.start()])
        txt = m.group(0)
        if k in assign:
            nums = assign[k]
            lab = str(nums[0]) if len(nums) == 1 else '%d-%d' % (nums[0], nums[-1]) if nums == list(range(nums[0], nums[-1] + 1)) else ','.join(map(str, nums))
            txt = txt.replace('<b>', '<b><span class="pn">%s</span>' % lab, 1)
        out.append(txt)
        last = m.end()
    out.append(body[last:])
    return ''.join(out)


# To-book items: only things that need or strongly benefit from a reservation/ticket (matched by text).
BOOK = re.compile(r'Shibuya Sky|teamLab|Narita Express|Shinkansen|Kaiyukan|Water Bus|Sagano|Dotonbori night cruise|'
                  r'Kitan Hibiki|Hikiniku to Come|Gansan Sanjo|Marutomi|Kichikichi|Kokuryu|Yoshitake|IDATEN|Menbaka|'
                  r'Skytree|Skyliner|Coco Nemaru|FORNO')
BOOK_CATS = [('Transport', r'Narita Express|Shinkansen|Skyliner'),
             ('Attractions and tickets', r'Shibuya Sky|teamLab|Kaiyukan|Water Bus|Sagano|cruise|Skytree'),
             ('Restaurants', r'.')]


def group_todo(body):
    """Split the checklist: booking items (grouped) stay; the rest go to a 'Walk-in and tips' list."""
    lis = re.findall(r'<li>(.*?)</li>', body, re.S)
    groups = {c[0]: [] for c in BOOK_CATS}
    other = []
    for li in lis:
        txt = re.sub(r'<[^>]+>', '', li).split(':')[0]
        if not BOOK.search(txt):
            other.append(li)
            continue
        for title, pat in BOOK_CATS:
            if re.search(pat, txt):
                groups[title].append(li)
                break
    h2 = '<h2>To book</h2>'
    main = h2 + ''.join('<h3 class="todo-h">%s</h3><ul>%s</ul>' % (t, ''.join('<li>%s</li>' % x for x in groups[t]))
                        for t, _ in BOOK_CATS if groups[t])
    rest = '<h2>Walk-in and tips</h2><ul class="plain">%s</ul>' % ''.join('<li>%s</li>' % x for x in other)
    return main, rest


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
        m = re.search(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun), (Oct|Nov) (\d+)', html)
        body = re.sub(r'^<div class="card"[^>]*>', '', html)
        body = body[:body.rindex('</div>')]
        body = re.sub(r'id="map(\d)"', lambda x: 'id="l%d-map%s"' % (n, x.group(1)), body)
        attrs = ''
        if m and cid.startswith('day'):
            d = int(m.group(3))
            k = (10 if m.group(2) == 'Oct' else 11) * 100 + d
            daydates[int(cid[3:])] = k
            dn = int(cid[3:])
            sb = re.search(r'(?<![\w])%d: \[(.*?)\n    \]' % dn, stops, re.S)
            if sb:
                body = number_slots(n, dn, body, re.findall(r'\["([^"]+)"', sb.group(1)))
            body = re.sub(r'<div class="badge">.*?</div>', '<div class="badge">%d</div>' % d, body, count=1)
            attrs = ' data-date="2026-%02d-%02d" style="--c:%s"' % (k // 100, d, LINE[k])
            dayc.append('<button data-p="%s" style="--c:%s"><b>%d</b><i>%s</i></button>' % (pid, LINE[k], d, m.group(1)))
        else:
            if cid == 'todo':
                body, walk = group_todo(body)
                panels.append('<article class="panel" id="l%d-walkin"><div class="card">%s</div></article>' % (n, walk))
                rest.append('<button class="txt" data-p="l%d-walkin">Walk-in</button>' % n)
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
<li><b>Oct 21</b> Fly TLV 19:45, land Narita Oct 22 13:20<small>El Al LY91 &middot; booking XKJ3AB &middot; seats 46D Harel, 46C Menashe</small></li>
<li><b>Oct 22&ndash;26</b> Shinjuku, Tokyo<small>Shinjuku Washington Hotel Annex &middot; Agoda 683387539</small><a href="tel:+81333433111">Call hotel</a></li>
<li><b>Oct 26&ndash;31</b> Osaka &amp; Kyoto<small>Hotel Geometiq Osaka Umeda &middot; Booking.com 6269959712 &middot; paid</small><a href="tel:+81663111551">Call hotel</a></li>
<li><b>Oct 31&ndash;Nov 4</b> Ueno, Tokyo<small>APA Hotel Keisei Ueno-Ekimae &middot; Agoda 685720259 &middot; plan in Ueno tab</small><a href="tel:+81358466811">Call hotel</a></li>
<li><b>Nov 4</b> Fly Tokyo 23:00, land TLV Nov 5 06:30<small>Arkia IZ882 &middot; order 13513638 &middot; 1 bag + 1 trolley each. Ueno check-out is 10:00, so store bags.</small></li>
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

CSS = open('data/site.css', encoding='utf-8').read()
JS = open('data/site.js', encoding='utf-8').read()
PLACES = open('data/places.js', encoding='utf-8').read()
html = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#000000"><title>Japan 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;500;700;900&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<link rel="stylesheet" href="data/vendor/leaflet.css">
<style>''' + CSS + '''</style></head><body>
''' + OVERVIEW + '\n' + '\n'.join(secs) + '''
<nav class="tabbar" id="tabbar">
<button data-leg="0"><span class="ic">&#9679;</span>Overview</button>
<button data-leg="1"><span class="ic">新</span>Tokyo</button>
<button data-leg="2"><span class="ic">阪</span>Osaka</button>
<button data-leg="3"><span class="ic">野</span>Ueno</button>
<button id="heBtn" class="he"><span class="ic">א</span><span class="t">עברית</span></button>
<div id="gte"></div>
</nav>
<script src="data/vendor/leaflet.js"></script>
<script>
''' + PLACES + '\nvar LEGS = {};\n' + '\n'.join(datas) + '\n' + JS + '</script></body></html>'
open('index.html', 'w', encoding='utf-8').write(html)
