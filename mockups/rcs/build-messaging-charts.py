# /// script
# requires-python = '>=3.14'
# ///
import json
from collections import Counter
from html import escape
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / 'research' / 'rcs'
OUT = Path(__file__).resolve().parent

BY_COUNTRY = json.loads((RESEARCH / 'messaging-by-country.json').read_text())
GLOBAL = json.loads((RESEARCH / 'messaging-global.json').read_text())
ADOPTION = json.loads((RESEARCH / 'adoption.json').read_text())

GWI_UNIT = 'percent of internet users aged 16+ reporting use in the past month'
REGIONS = ['Europe', 'Asia', 'North America', 'South America', 'Africa', 'Oceania']
COLORED_APPS = {'WhatsApp': 's1', 'Facebook Messenger': 's2', 'Telegram': 's3'}


def num(value: float) -> str:
	text = f'{value:,.6f}'.rstrip('0').rstrip('.')
	assert float(text.replace(',', '')) == value, (value, text)
	return text


def big(value: float) -> str:
	for scale, word in ((1e12, 'trillion'), (1e9, 'billion'), (1e6, 'million')):
		if value >= scale:
			text = f'{value / scale:.6f}'.rstrip('0').rstrip('.')
			assert round(float(text) * scale) == value, (value, text)
			return f'{text} {word}'
	return num(value)


def qualified(metric: dict) -> str:
	prefix = {'more_than': 'more than ', 'approximately': 'about ', 'nearly': 'nearly '}
	return prefix.get(metric.get('qualifier'), '') + big(metric['value'])


def host(url: str | None) -> str:
	if url is None:
		return 'none found'
	return urlparse(url).netloc.removeprefix('www.')


def a(url: str | None, label: str) -> str:
	if url is None:
		return '—'
	return f'<a href="{escape(url)}">{escape(label)}</a>'


def attr(text: str) -> str:
	return escape(text, quote=True)


CSS = """
:root {
	color-scheme: light dark;
	--page: #f9f9f7;
	--surface: #fcfcfb;
	--ink: #0b0b0b;
	--ink-2: #52514e;
	--muted: #6f6d68;
	--grid: #e1e0d9;
	--axis: #c3c2b7;
	--ring: rgba(11, 11, 11, 0.1);
	--s1: #1baf7a;
	--s2: #2a78d6;
	--s3: #eb6834;
	--other: #d9d7cf;
	--on-fill: #0b0b0b;
	--on-other: #0b0b0b;
}
@media (prefers-color-scheme: dark) {
	:root {
		--page: #0d0d0d;
		--surface: #1a1a19;
		--ink: #ffffff;
		--ink-2: #c3c2b7;
		--muted: #a3a199;
		--grid: #2c2c2a;
		--axis: #383835;
		--ring: rgba(255, 255, 255, 0.1);
		--s1: #199e70;
		--s2: #3987e5;
		--s3: #d95926;
		--other: #4a4945;
		--on-fill: #0b0b0b;
		--on-other: #ffffff;
	}
}
* { box-sizing: border-box; }
body {
	margin: 0;
	background: var(--page);
	color: var(--ink);
	font: 15px/1.5 system-ui, -apple-system, 'Segoe UI', sans-serif;
}
main {
	max-width: 68rem;
	margin: 0 auto;
	padding: 1.5rem 1rem 4rem;
}
h1 {
	font-size: clamp(1.5rem, 1.1rem + 2vw, 2.25rem);
	line-height: 1.15;
	letter-spacing: -0.02em;
	margin: 0 0 0.5rem;
	max-width: 30ch;
}
h2 {
	font-size: 0.8rem;
	letter-spacing: 0.05em;
	text-transform: uppercase;
	color: var(--ink-2);
	margin: 2rem 0 0.75rem;
}
h2 span { text-transform: none; letter-spacing: 0; font-weight: 400; color: var(--muted); }
.caption { color: var(--ink-2); max-width: 65ch; margin: 0 0 1rem; }
.legend {
	display: flex;
	flex-wrap: wrap;
	gap: 0.5rem 1rem;
	margin: 1rem 0;
	padding: 0;
	list-style: none;
	font-size: 0.85rem;
	color: var(--ink-2);
}
.legend li { display: flex; align-items: center; gap: 0.4rem; }
.swatch { width: 1.1rem; height: 0.8rem; flex: none; }
.chart { background: var(--surface); border-radius: 12px; box-shadow: 0 0 0 1px var(--ring); padding: 1rem; }
.chart > h2:first-child, .chart > section:first-child h2 { margin-top: 0; }
@media (max-width: 40rem) { .chart { padding: 0.75rem 0.5rem; } }
footer { margin-top: 2rem; font-size: 0.85rem; color: var(--ink-2); max-width: 75ch; }
footer h3 { font-size: 0.85rem; margin: 1.25rem 0 0.25rem; color: var(--ink); }
footer ul { margin: 0; padding-left: 1.1rem; }
a { color: inherit; text-underline-offset: 2px; overflow-wrap: anywhere; }
[data-tip] { cursor: default; }
[data-tip]:focus-visible { outline: 2px solid var(--ink); outline-offset: 2px; }
#tip {
	position: fixed;
	z-index: 10;
	max-width: min(22rem, calc(100vw - 1rem));
	padding: 0.5rem 0.65rem;
	border-radius: 8px;
	background: var(--ink);
	color: var(--page);
	font-size: 0.8rem;
	line-height: 1.4;
	white-space: pre-line;
	pointer-events: none;
}
details { margin-top: 1.5rem; }
summary { cursor: pointer; font-weight: 600; }
.table-wrap { overflow-x: auto; }
table { border-collapse: collapse; font-size: 0.8rem; margin-top: 0.75rem; min-width: 40rem; }
th, td { text-align: left; padding: 0.3rem 0.6rem 0.3rem 0; border-bottom: 1px solid var(--grid); vertical-align: top; }
td.n { font-variant-numeric: tabular-nums; }
"""

JS = """
const tip = document.getElementById('tip');
function place(el) {
	tip.textContent = el.dataset.tip;
	tip.hidden = false;
	const r = el.getBoundingClientRect();
	const t = tip.getBoundingClientRect();
	const left = Math.min(Math.max(8, r.left + r.width / 2 - t.width / 2), innerWidth - t.width - 8);
	const top = r.top - t.height - 8 > 8 ? r.top - t.height - 8 : r.bottom + 8;
	tip.style.left = left + 'px';
	tip.style.top = top + 'px';
}
function hide() { tip.hidden = true; }
document.addEventListener('pointerover', (e) => {
	const el = e.target.closest('[data-tip]');
	el ? place(el) : hide();
});
document.addEventListener('focusin', (e) => {
	const el = e.target.closest('[data-tip]');
	el ? place(el) : hide();
});
document.addEventListener('scroll', hide, { passive: true });
"""

PATTERNS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
	<defs>
		<pattern id="hatch-s1" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="2.5" height="6" style="fill:var(--s1)"/></pattern>
		<pattern id="hatch-s2" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="2.5" height="6" style="fill:var(--s2)"/></pattern>
		<pattern id="hatch-s3" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="2.5" height="6" style="fill:var(--s3)"/></pattern>
		<pattern id="hatch-other" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="2.5" height="6" style="fill:var(--other)"/></pattern>
	</defs>
</svg>"""


def page(title: str, body: str, data: object, css: str) -> str:
	payload = json.dumps(data, ensure_ascii=False, indent='\t').replace('</', '<\\/')
	return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<style>{CSS}{css}</style>
</head>
<body>
{PATTERNS}
<main>
{body}
</main>
<div id="tip" role="tooltip" hidden></div>
<script type="application/json" id="data">
{payload}
</script>
<script>{JS}</script>
</body>
</html>
"""


def swatch(fill: str, stroke: str = 'none', dash: str = '') -> str:
	return (
		f'<svg class="swatch" viewBox="0 0 18 13" aria-hidden="true"><rect x="1" y="1" width="16" height="11" rx="3" '
		f'fill="{fill}" stroke="{stroke}" stroke-width="1.5" {dash}/></svg>'
	)


def source_list(urls: list[str]) -> str:
	counts = Counter(u for u in urls if u)
	items = ''.join(f'<li>{a(u, host(u) + urlparse(u).path)} · {n}</li>' for u, n in counts.most_common())
	return f'<ul>{items}</ul>'


def publisher_list(urls: list[str]) -> str:
	first = {}
	for u in urls:
		if u:
			first.setdefault(host(u), u)
	counts = Counter(host(u) for u in urls if u)
	items = ''.join(
		f'<li>{a(first[h], h)} · {n} market{"s" if n != 1 else ""}</li>' for h, n in counts.most_common()
	)
	return f'<ul>{items}</ul>'


# ---------- 1. app patchwork ----------

PATCHWORK_CSS = """
.region-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(6.25rem, 1fr)); gap: 4px; }
.tile { position: relative; min-height: 5.25rem; padding: 0.45rem 0.5rem; border-radius: 8px; overflow: hidden; }
.tile > svg.bg { position: absolute; inset: 0; width: 100%; height: 100%; }
.tile > * { position: relative; }
.tile .country { display: block; font-size: 0.75rem; line-height: 1.2; }
.tile .app { display: block; font-weight: 700; font-size: 0.85rem; line-height: 1.2; margin-top: 0.15rem; }
.tile .share { display: block; font-size: 0.8rem; font-variant-numeric: tabular-nums; margin-top: 0.1rem; }
.tile .flag { display: block; font-size: 0.7rem; margin-top: 0.1rem; }
.tile.fill { color: var(--on-fill); }
.tile.fill.other { color: var(--on-other); }
.tile.hatch span, .tile.unknown span { width: fit-content; background: var(--surface); padding: 0 3px; border-radius: 3px; }
.tile.hatch { border: 2px solid var(--c); background: var(--surface); }
.tile.unknown { color: var(--ink-2); border: 1.5px dashed var(--muted); }
.stat { display: flex; flex-wrap: wrap; gap: 0.25rem 1.5rem; margin: 0 0 1rem; padding: 0; list-style: none; }
.stat b { font-size: 1.5rem; display: block; line-height: 1.1; }
.stat li { color: var(--ink-2); font-size: 0.85rem; }
"""


def tile_mark(fill_var: str, hatched: bool) -> str:
	fill = f'url(#hatch-{fill_var})' if hatched else f'var(--{fill_var})'
	return f'<svg class="bg" aria-hidden="true"><rect width="100%" height="100%" style="fill:{fill}"/></svg>'


def restriction_text(country: dict) -> str:
	apps = sorted({r['app'] for r in country['restrictions']})
	return ', '.join(apps)


def restricted_label(country: dict) -> str:
	apps = {r['app'] for r in country['restrictions']}
	return escape(next(iter(apps))) if len(apps) == 1 else f'{len(apps)} apps'


def build_tile(c: dict) -> tuple[str, dict]:
	app = c['dominant_app']
	share = c['dominant_app_share']
	share_value = share['value'] if share else None
	off_basis = share_value is not None and share['unit'] != GWI_UNIT
	row = {
		'iso': c['country_iso'],
		'country': c['country_name'],
		'region': c['continent'],
		'leading_app': app,
		'leading_app_confidence': c['dominant_app_confidence'],
		'basis': c['dominant_app_basis'],
		'source_url': c['dominant_app_source_url'],
		'date': c['dominant_app_date'],
		'share': share_value,
		'share_unit': share['unit'] if share_value is not None else None,
		'share_confidence': share['confidence'] if share_value is not None else None,
		'share_source_url': share['source_url'] if share_value is not None else None,
		'restricted_apps': restriction_text(c) or None,
	}
	tip = [f'{c["country_name"]}: {app or "no reliable ranking"}']
	if share_value is not None:
		tip.append(f'{num(share_value)}% — {share["unit"]} ({share["date"]}, {share["confidence"]})')
	else:
		tip.append('Share: not available')
	tip.append(f'Basis: {c["dominant_app_basis"]}')
	tip.append(f'Confidence: {c["dominant_app_confidence"] or "none"}')
	if row['restricted_apps']:
		tip.append(f'Restrictions recorded for: {row["restricted_apps"]}')
	tip.append(f'Source: {host(c["dominant_app_source_url"])}')
	label = ' '.join(tip[:2])
	if app is None:
		return (
			f'<div class="tile unknown" tabindex="0" data-tip="{attr(chr(10).join(tip))}" aria-label="{attr(label)}">'
			f'<span class="country">{escape(c["country_name"])}</span><span class="app">No reliable ranking</span></div>',
			row,
		)
	fill_var = COLORED_APPS.get(app, 'other')
	hatched = c['dominant_app_confidence'] != 'measured'
	classes = ['tile', 'hatch' if hatched else 'fill']
	if fill_var == 'other':
		classes.append('other')
	share_html = ''
	if share_value is not None:
		mark = '*' if off_basis else ''
		share_html = f'<span class="share">{num(share_value)}%{mark}</span>'
	flag = f'<span class="flag">⊘ {restricted_label(c)} restricted</span>' if row['restricted_apps'] else ''
	short_app = 'Messenger' if app == 'Facebook Messenger' else app
	html = (
		f'<div class="{" ".join(classes)}" style="--c:var(--{fill_var})" tabindex="0" data-tip="{attr(chr(10).join(tip))}" aria-label="{attr(label)}">'
		f'{tile_mark(fill_var, hatched)}'
		f'<span class="country">{escape(c["country_name"])}</span>'
		f'<span class="app">{escape(short_app)}</span>{share_html}{flag}</div>'
	)
	return html, row


def app_order(countries: list[dict]) -> dict:
	counts = Counter(c['dominant_app'] for c in countries if c['dominant_app'])
	return {app: i for i, (app, _) in enumerate(counts.most_common())}


def build_patchwork() -> str:
	countries = BY_COUNTRY['countries']
	assert len(countries) == 74
	assert {c['continent'] for c in countries} == set(REGIONS)
	rank = app_order(countries)
	leading = [c['dominant_app'] for c in countries if c['dominant_app']]
	app_counts = Counter(leading)
	distinct = len(app_counts)
	with_share = sum(
		1 for c in countries if c['dominant_app_share'] and c['dominant_app_share']['value'] is not None
	)
	rows = []
	sections = []
	for region in REGIONS:
		members = [c for c in countries if c['continent'] == region]
		members.sort(key=lambda c: (rank.get(c['dominant_app'], 99), c['country_name']))
		tiles = []
		for c in members:
			html, row = build_tile(c)
			tiles.append(html)
			rows.append(row)
		region_apps = len({c['dominant_app'] for c in members if c['dominant_app']})
		sections.append(
			f'<h2>{region} <span>· {len(members)} markets · {region_apps} leading '
			f'app{"s" if region_apps != 1 else ""}</span></h2>'
			f'<div class="region-grid">{"".join(tiles)}</div>'
		)
	others = sorted((app for app in app_counts if app not in COLORED_APPS), key=lambda x: (-app_counts[x], x))
	legend = f"""<ul class="legend">
	<li>{swatch('var(--s1)')}WhatsApp · {app_counts['WhatsApp']}</li>
	<li>{swatch('var(--s2)')}Facebook Messenger · {app_counts['Facebook Messenger']}</li>
	<li>{swatch('var(--s3)')}Telegram · {app_counts['Telegram']}</li>
	<li>{swatch('var(--other)')}Other app, named on tile · {sum(app_counts[x] for x in others)}</li>
	<li>{swatch('url(#hatch-s1)', 'var(--s1)')}Hatched = ranking is an estimate</li>
	<li>{swatch('none', 'var(--muted)', 'stroke-dasharray="3 2"')}Dashed = no reliable ranking</li>
</ul>"""
	table_rows = ''.join(
		f'<tr><td>{escape(r["country"])}</td><td>{escape(r["region"])}</td><td>{escape(r["leading_app"] or "—")}</td>'
		f'<td>{escape(r["leading_app_confidence"] or "—")}</td>'
		f'<td class="n">{num(r["share"]) + "%" if r["share"] is not None else "—"}</td>'
		f'<td>{escape(r["share_unit"] or "—")}</td><td>{escape(r["date"])}</td>'
		f'<td>{a(r["source_url"], host(r["source_url"]))}</td></tr>'
		for r in rows
	)
	body = f"""<h1>{distinct} apps lead in {len(leading)} of {len(countries)} researched markets</h1>
<p class="caption">Leading messaging app in each market, grouped by region. WhatsApp leads in {app_counts['WhatsApp']} of {len(countries)}, but Messenger, Telegram, LINE, Viber, KakaoTalk, WeChat, Zalo, MAX and Snapchat each lead somewhere. The percentage is the leading app’s share where a figure exists ({with_share} of {len(countries)} markets).</p>
<ul class="stat">
	<li><b>{distinct}</b>different leading apps</li>
	<li><b>{app_counts['WhatsApp']} / {len(countries)}</b>markets led by WhatsApp</li>
	<li><b>{len(countries) - with_share}</b>markets without a share figure</li>
</ul>
{legend}
<div class="chart">{''.join(sections)}</div>
<details>
	<summary>Table view, all {len(countries)} markets</summary>
	<div class="table-wrap"><table>
		<thead><tr><th>Country</th><th>Region</th><th>Leading app</th><th>Confidence</th><th>Share</th><th>Share unit</th><th>Date</th><th>Source</th></tr></thead>
		<tbody>{table_rows}</tbody>
	</table></div>
</details>
<footer>
	<h3>How to read the percentages</h3>
	<p>Unmarked figures: percent of internet users aged 16+ who used the app in the past month (GWI survey, Q2 2026, via DataReportal Digital 2027). Figures marked * use a different base: Australia (adults messaging in the past seven days, 2025), United Kingdom (adults 18+ visiting in the month, 2025), South Korea (surveyed messenger users, 2025), Taiwan (most-used messenger, 2025), Ukraine (Gradus respondents, 2026), Kuwait and Qatar (estimated business-messaging reach, Infobip). Hover or focus a tile for the exact unit.</p>
	<h3>Data gaps</h3>
	<p>{len(countries) - with_share} markets lack a share figure, including one without a reliable ranking. Hatched tiles rest on Android-only app rankings or published rankings with unspecified methods. Iran has no reliable current ranking. App audiences overlap, so shares do not add up, and default SMS/RCS texting is excluded from these rankings. ⊘ marks markets with recorded blocks or calling restrictions (dated observations, not a full list).</p>
	<h3>Sources (leading-app ranking, markets per publisher)</h3>
	{publisher_list([r['source_url'] for r in rows])}
	<p>Each market’s exact report link is in the table view.</p>
	<p>Data: research/rcs/messaging-by-country.json, research cutoff {BY_COUNTRY['as_of']}.</p>
</footer>"""
	return page('Leading messaging app by market', body, rows, PATCHWORK_CSS)


# ---------- 2. global app reach ----------

REACH_CSS = """
.rows { display: grid; gap: 0.6rem; }
.row { display: grid; grid-template-columns: minmax(7.5rem, 11rem) 1fr; gap: 0.25rem 0.75rem; align-items: center; }
.row .name { font-weight: 600; font-size: 0.9rem; }
.row .value { font-size: 0.8rem; color: var(--ink-2); grid-column: 2; }
.row .value b { color: var(--ink); font-variant-numeric: tabular-nums; }
.row svg { display: block; width: 100%; height: 18px; overflow: visible; }
.nocount { font-size: 0.8rem; color: var(--ink-2); border: 1.5px dashed var(--muted); border-radius: 6px; padding: 0.1rem 0.5rem; width: fit-content; }
.axis { display: grid; grid-template-columns: minmax(7.5rem, 11rem) 1fr; gap: 0 0.75rem; font-size: 0.7rem; color: var(--muted); }
.axis svg { width: 100%; height: 16px; overflow: visible; }
.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr)); gap: 0.75rem; }
.card { background: var(--surface); box-shadow: 0 0 0 1px var(--ring); border-radius: 10px; padding: 0.75rem; font-size: 0.85rem; }
.card b { display: block; font-size: 1.15rem; }
.card .unit { color: var(--ink); }
.card .meta { color: var(--muted); font-size: 0.75rem; }
.card .conf { display: flex; align-items: center; gap: 0.35rem; color: var(--ink-2); font-size: 0.75rem; margin-top: 0.25rem; }
@media (max-width: 40rem) {
	.row, .axis { grid-template-columns: 1fr; }
	.row .value { grid-column: 1; }
	.axis span { display: none; }
}
"""


def conf_mark(conf: str | None) -> tuple[str, str]:
	if conf == 'measured':
		return 'fill:var(--s2)', 'measured'
	if conf == 'vendor-claim':
		return 'fill:color-mix(in oklab, var(--s2) 35%, var(--surface));stroke:var(--s2)', 'vendor claim'
	assert conf == 'estimate', conf
	return 'fill:url(#hatch-s2);stroke:var(--s2)', 'estimate'


def build_reach() -> str:
	apps = GLOBAL['apps']
	counted = sorted((x for x in apps if x['mau']['value'] is not None), key=lambda x: -x['mau']['value'])
	missing = [x for x in apps if x['mau']['value'] is None]
	top = counted[0]['mau']['value']
	assert counted[0]['app'] == 'WhatsApp' and top == 3_000_000_000
	ticks = [0, 1e9, 2e9, 3e9]
	grid = ''.join(
		f'<line x1="{t / top * 100}%" x2="{t / top * 100}%" y1="-4" y2="22" stroke="var(--grid)"/>'
		for t in ticks
	)
	axis = ''.join(
		f'<text x="{t / top * 100}%" y="12" text-anchor="{"start" if t == 0 else "end" if t == top else "middle"}" '
		f'fill="var(--muted)">{"0" if t == 0 else big(t)}</text>'
		for t in ticks
	)
	rows = []
	for x in counted:
		m = x['mau']
		style, conf = conf_mark(m['confidence'])
		width = m['value'] / top * 100
		tip = f'{x["app"]}: {qualified(m)} {m["unit"]}\nDate: {m["date"]} · {conf}\n{m["note"]}\nSource: {host(m["source_url"])}'
		rows.append(
			f'<div class="row" tabindex="0" data-tip="{attr(tip)}">'
			f'<span class="name">{escape(x["app"])}</span>'
			f'<svg aria-hidden="true">{grid}<rect x="0" y="1" width="max(4px, {width}%)" height="16" rx="4" '
			f'style="{style};width:max(4px, {width}%)" stroke-width="1.5"/></svg>'
			f'<span class="value"><b>{qualified(m)}</b> {escape(m["unit"])} · {escape(m["date"])} · {conf}</span></div>'
		)
	for x in missing:
		m = x['mau']
		tip = f'{x["app"]}: no current verified monthly count\n{m["note"]}\nChecked: {host(m["source_url"])}'
		cls = 'row rcs' if x['app'] == 'RCS' else 'row'
		rows.append(
			f'<div class="{cls}" tabindex="0" data-tip="{attr(tip)}">'
			f'<span class="name">{escape(x["app"])}</span>'
			f'<span class="nocount">No current verified count — not zero</span></div>'
		)
	cards = []
	for x in apps:
		for r in x['related_metrics']:
			_, conf = conf_mark(r['confidence'])
			style, _ = conf_mark(r['confidence'])
			cards.append(
				f'<div class="card"><b>{qualified(r)}</b><span class="unit">{escape(r["unit"])}</span>'
				f'<div class="meta">{escape(x["app"])} · {escape(r["date"])} · {a(r["source_url"], host(r["source_url"]))}</div>'
				f'<div class="conf"><svg class="swatch" viewBox="0 0 18 13" aria-hidden="true"><rect x="1" y="1" width="16" '
				f'height="11" rx="3" style="{style}" stroke-width="1.5"/></svg>{conf}</div>'
				f'<div class="meta">{escape(r["note"])}</div></div>'
			)
	sources = [x['mau']['source_url'] for x in apps]
	legend = f"""<ul class="legend">
	<li>{swatch('color-mix(in oklab, var(--s2) 35%, var(--surface))', 'var(--s2)')}Vendor claim (company disclosure)</li>
	<li>{swatch('url(#hatch-s2)', 'var(--s2)')}Estimate</li>
	<li>{swatch('none', 'var(--muted)', 'stroke-dasharray="3 2"')}No current verified count</li>
</ul>"""
	data = [
		{'app': x['app'], 'monthly': x['mau'], 'other_measures_not_comparable': x['related_metrics']}
		for x in apps
	]
	whatsapp = counted[0]['mau']
	body = f"""<h1>WhatsApp reports {qualified(whatsapp)} monthly users. RCS has no verified monthly count at all.</h1>
<p class="caption">Latest company-reported monthly active users or accounts per messaging app. iMessage, Google Messages, RCS, Viber, Instagram DMs and SMS publish no current monthly user count, so they are shown as unknown, not as zero. Most bars count all activity in the app, not only messaging.</p>
{legend}
<div class="chart">
	<div class="axis"><span></span><svg aria-hidden="true">{axis}</svg></div>
	<div class="rows">{''.join(rows)}</div>
</div>
<h2>Other numbers people quote <span>· different measures, not monthly users, not on the axis above</span></h2>
<p class="caption">Forecasts, registrations, device counts, enabled subsets and message volumes. Each answers a different question, so none of them can stand in for a monthly user count.</p>
<div class="cards">{''.join(cards)}</div>
<footer>
	<h3>Data gaps</h3>
	<p>Units differ: WeChat and QQ report accounts, not people; Snapchat and KakaoTalk report quarter averages; “more than” figures are milestone floors. Signal’s figure is a media estimate with an undisclosed method. Apple does not publish iMessage users, Rakuten publishes only Viber registrations, Meta reports Instagram as a whole, and no source counts RCS users across all clients and carriers. The GSMA 3.8 billion RCS figure is a forecast for the end of 2026 with an unspecified activity window.</p>
	<h3>Sources (monthly counts and the pages checked for missing counts)</h3>
	{source_list(sources)}
	<p>Data: research/rcs/messaging-global.json, research cutoff {GLOBAL['as_of']}.</p>
</footer>"""
	return page('Global monthly users per messaging app', body, data, REACH_CSS)


# ---------- 3. iOS / Android split ----------

SPLIT_CSS = """
.rows { display: grid; gap: 0.35rem; }
.row { display: grid; grid-template-columns: minmax(9rem, 12rem) 1fr minmax(11rem, 16rem); gap: 0.15rem 0.75rem; align-items: center; font-size: 0.85rem; padding: 0.15rem 0; }
.row .name { font-weight: 600; }
.row svg { display: block; width: 100%; height: 14px; }
.row .rcs { font-size: 0.8rem; color: var(--ink-2); }
.row .nums { display: block; font-weight: 400; font-size: 0.75rem; color: var(--ink-2); font-variant-numeric: tabular-nums; }
.row .nums b { color: var(--ink); font-weight: 600; }
.group { margin-top: 0.5rem; }
.group + .group { margin-top: 1.5rem; }
.group p { margin: -0.4rem 0 0.75rem; font-size: 0.85rem; color: var(--ink-2); max-width: 65ch; }
.icon { font-weight: 700; color: var(--ink); }
.stat { display: flex; flex-wrap: wrap; gap: 0.25rem 1.5rem; margin: 0 0 1rem; padding: 0; list-style: none; }
.stat b { font-size: 1.5rem; display: block; line-height: 1.1; }
.stat li { color: var(--ink-2); font-size: 0.85rem; }
@media (max-width: 40rem) {
	.row { grid-template-columns: 1fr; }
}
"""

ANDROID_STATUS = {
	'confirmed': 'Android RCS confirmed',
	'documented_historically': 'Android RCS documented in the past',
	'announced_historically': 'Android RCS announced in the past',
	'unverified': 'Android RCS unverified',
	'carrier_ecosystem': 'Android RCS via carrier ecosystem',
}


def split_row(c: dict, market: dict | None) -> tuple[str, dict]:
	ios = c['ios_share']['value']
	android = c['android_share']['value']
	row = {
		'iso': c['country_iso'],
		'country': c['country_name'],
		'ios_share': ios,
		'android_share': android,
		'os_unit': c['ios_share']['unit'],
		'os_date': c['ios_share']['date'],
		'os_source_url': c['ios_share']['source_url'],
		'iphone_rcs_carriers_listed': market['iphone']['value'] if market else None,
		'iphone_rcs_status': market['iphone']['status'] if market else None,
		'iphone_rcs_source_url': market['iphone']['source_url'] if market else None,
		'android_rcs_status': market['android_status'] if market else None,
	}
	bar = (
		f'<svg aria-hidden="true"><rect x="0" width="{ios}%" height="14" rx="4" style="fill:var(--s2)"/>'
		f'<rect x="{100 - android}%" width="{android}%" height="14" rx="4" style="fill:var(--s1)"/></svg>'
	)
	tip = [
		f'{c["country_name"]}: iOS {num(ios)}%, Android {num(android)}%',
		f'{c["ios_share"]["unit"]}, {c["ios_share"]["date"]} (StatCounter)',
	]
	rcs = ''
	if market:
		iphone = market['iphone']
		if iphone['status'] == 'listed':
			carriers = ', '.join(iphone['carriers'])
			rcs = f'<span class="icon">✓</span> iPhone RCS: {num(iphone["value"])} carrier{"s" if iphone["value"] != 1 else ""} listed'
			tip.append(f'Apple lists iPhone RCS for: {carriers}')
		else:
			rcs = '<span class="icon">–</span> iPhone RCS: no carrier listed'
			tip.append('Apple’s carrier directory lists no iPhone RCS carrier here')
		status = ANDROID_STATUS[market['android_status']]
		rcs += f'<br>{status}'
		tip.append(status)
		tip.append(
			f'Apple directory: {host(iphone["source_url"])}{urlparse(iphone["source_url"]).path} ({iphone["date"]})'
		)
		rcs = f'<span class="rcs">{rcs}</span>'
	html = (
		f'<div class="row" tabindex="0" data-tip="{attr(chr(10).join(tip))}">'
		f'<span class="name">{escape(c["country_name"])}'
		f'<span class="nums"><b>iOS {num(ios)}%</b> · Android {num(android)}%</span></span>{bar}{rcs}</div>'
	)
	return html, row


def build_split() -> str:
	countries = BY_COUNTRY['countries']
	markets = {m['country_code']: m for m in ADOPTION['markets']}
	assert all(c['ios_share'] and c['android_share'] for c in countries)
	assert set(markets) <= {c['country_iso'] for c in countries}, set(markets) - {
		c['country_iso'] for c in countries
	}
	listed, unlisted, unresearched = [], [], []
	for c in sorted(countries, key=lambda c: -c['ios_share']['value']):
		m = markets.get(c['country_iso'])
		if m is None:
			unresearched.append((c, m))
		elif m['iphone']['status'] == 'listed' and m['iphone']['value'] > 0:
			listed.append((c, m))
		else:
			assert m['iphone']['status'] == 'none_listed' and m['iphone']['value'] == 0, m
			unlisted.append((c, m))
	rows = []

	def group(title: str, note: str, members: list) -> str:
		html = []
		for c, m in members:
			h, r = split_row(c, m)
			html.append(h)
			rows.append(r)
		cls = 'group'
		return f'<section class="{cls}"><h2>{title} <span>· {len(members)} markets</span></h2><p>{note}</p><div class="rows">{"".join(html)}</div></section>'

	iphone_majority = [c['country_name'] for c, _ in unresearched + unlisted if c['ios_share']['value'] > 50]
	body = f"""<h1>Apple lists iPhone RCS carriers in {len(listed)} of {len(countries)} markets in this dataset. Most have not been researched.</h1>
<p class="caption">Each bar shows the iOS and Android shares of mobile web page views. Every iPhone–Android conversation needs RCS on both ends. Apple’s carrier directory confirms iPhone RCS on named carriers in {len(listed)} markets, lists none in {len(unlisted)}, and the other {len(unresearched)} markets have not been checked.</p>
<ul class="stat">
	<li><b>{len(listed)}</b>markets with iPhone RCS carriers listed</li>
	<li><b>{len(unlisted)}</b>researched, no iPhone RCS carrier listed</li>
	<li><b>{len(unresearched)}</b>not yet researched</li>
</ul>
<ul class="legend">
	<li>{swatch('var(--s2)')}iOS share</li>
	<li>{swatch('var(--s1)')}Android share</li>
	<li>Gap between bars = other operating systems</li>
</ul>
<div class="chart">
{group('iPhone RCS carriers listed', 'Apple lists at least one local carrier with iPhone RCS. RCS still needs both people to have it enabled, and carrier support and eligibility can vary.', listed)}
{group('Researched, no iPhone RCS carrier listed', 'Apple’s directory lists no local carrier with iPhone RCS. This directory is not a complete availability test.', unlisted)}
{group('Not researched for RCS', 'No carrier or device check exists in this dataset. Unknown, not unavailable.', unresearched)}
</div>
<footer>
	<h3>Data gaps</h3>
	<p>Operating-system shares are StatCounter mobile web page views for October 2026, not device counts or people; other systems and rounding make up the remainder. iPhone RCS status comes from Apple’s carrier directory on {ADOPTION['as_of']}: a listed carrier supports it, but a traveler on another carrier or roaming may not get it (no roaming inference is made). The United States count covers selected national carriers only. Android status labels describe documented Google Messages or carrier RCS, not activation rates. {len(unresearched)} markets have no RCS research, including iPhone-majority markets such as {', '.join(iphone_majority[:6])}.</p>
	<h3>Sources</h3>
	<ul>
		<li>{a('https://gs.statcounter.com/os-market-share/mobile', 'StatCounter mobile OS market share')}, October 2026, CC BY-SA 3.0 ({len(countries)} country pages, linked in the table data)</li>
		{''.join(f'<li>{a(u, "Apple carrier support · " + urlparse(u).path)} · {n} markets</li>' for u, n in Counter(m['iphone']['source_url'] for m in markets.values()).most_common())}
	</ul>
	<p>Data: research/rcs/messaging-by-country.json and research/rcs/adoption.json, research cutoff {ADOPTION['as_of']}.</p>
</footer>"""
	return page('iOS vs Android share and RCS availability by market', body, rows, SPLIT_CSS)


if __name__ == '__main__':
	(OUT / 'app-patchwork.html').write_text(build_patchwork())
	(OUT / 'global-app-reach.html').write_text(build_reach())
	(OUT / 'ios-android-split.html').write_text(build_split())
	print('wrote 3 charts to', OUT)
