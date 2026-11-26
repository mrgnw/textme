import json
from html import escape
from pathlib import Path

HERE = Path(__file__).parent
DATA = json.loads((HERE / '../../research/rcs/adoption.json').read_text())
AS_OF = DATA['as_of']

CSS = """
:root {
	color-scheme: light dark;
	--surface: #f7f6f3;
	--surface-2: #ecebe6;
	--ink: #1c1917;
	--ink-2: #57534e;
	--rule: #dcdad3;
	--bar: #2a78d6;
	--bar-soft: #86b6ef;
	--live: #0ca30c;
	--partial: #fab219;
	--gap: #8a857c;
}
@media (prefers-color-scheme: dark) {
	:root {
		--surface: #1a1a19;
		--surface-2: #262624;
		--ink: #f5f5f4;
		--ink-2: #c3c2b7;
		--rule: #3a3a37;
		--bar: #3987e5;
		--bar-soft: #184f95;
		--gap: #8f8b82;
	}
}
* { box-sizing: border-box; }
body {
	margin: 0;
	background: var(--surface);
	color: var(--ink);
	font: 16px/1.6 system-ui, -apple-system, 'Segoe UI', sans-serif;
}
main { max-width: 760px; margin: 0 auto; padding: 32px 20px 64px; }
h1, h2, .year {
	font-family: 'Iowan Old Style', 'Palatino Linotype', Palatino, Charter, Georgia, serif;
	letter-spacing: -0.02em;
	line-height: 1.1;
}
h1 { font-size: clamp(30px, 7vw, 48px); margin: 8px 0 16px; text-wrap: balance; }
h2 { font-size: 24px; margin: 48px 0 12px; }
.eyebrow { font-size: 13px; letter-spacing: 0.05em; text-transform: uppercase; color: var(--ink-2); margin: 0; }
.caption { color: var(--ink-2); max-width: 62ch; margin: 0 0 24px; }
.muted { color: var(--ink-2); }
small, .small { font-size: 13px; line-height: 1.45; }
a { color: inherit; text-underline-offset: 2px; }
.legend { display: flex; flex-wrap: wrap; gap: 8px 20px; font-size: 13px; color: var(--ink-2); margin: 0 0 24px; padding: 0; list-style: none; }
.legend li { display: flex; align-items: center; gap: 6px; }
.gaps { margin-top: 48px; padding: 16px 20px; border: 1px dashed var(--gap); border-radius: 10px; }
.gaps h2 { margin-top: 0; font-size: 20px; }
.gaps ul, .sources ul { padding-left: 18px; margin: 0; }
.sources li { font-size: 13px; line-height: 1.45; margin: 4px 0; overflow-wrap: anywhere; }
details { margin-top: 32px; }
summary { cursor: pointer; font-weight: 600; min-height: 44px; display: flex; align-items: center; }
.table-wrap { overflow-x: auto; }
table.data { border-collapse: collapse; font-size: 13px; width: 100%; }
table.data th, table.data td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--rule); vertical-align: top; }
table.data td.num { font-variant-numeric: tabular-nums; white-space: nowrap; }
svg { display: block; overflow: visible; }
"""

PATTERNS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
	<defs>
		<pattern id="hatch-bar" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
			<rect width="5" height="5" style="fill:var(--surface)"/>
			<line x1="0" y1="0" x2="0" y2="5" style="stroke:var(--bar)" stroke-width="2.4"/>
		</pattern>
		<pattern id="hatch-ink" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
			<line x1="0" y1="0" x2="0" y2="4" style="stroke:var(--ink-2)" stroke-width="1.6"/>
		</pattern>
		<pattern id="hatch-live" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
			<rect width="4" height="4" style="fill:var(--surface)"/>
			<line x1="0" y1="0" x2="0" y2="4" style="stroke:var(--live)" stroke-width="2"/>
		</pattern>
		<pattern id="hatch-partial" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
			<rect width="4" height="4" style="fill:var(--surface)"/>
			<line x1="0" y1="0" x2="0" y2="4" style="stroke:var(--partial)" stroke-width="2"/>
		</pattern>
	</defs>
</svg>"""

PUBLISHERS = {
	'blog.google': 'Google',
	'support.google.com': 'Google',
	'play.google.com': 'Google Play',
	'www.youtube.com': 'Google (video)',
	'www.apple.com': 'Apple',
	'support.apple.com': 'Apple',
	'www.gsma.com': 'GSMA',
	'prod-cms.gsmaintelligence.com': 'GSMA Intelligence',
	'www.gsmaservices.com': 'GSMA Industry Services',
	'www.juniperresearch.com': 'Juniper Research',
	'omdia.tech.informa.com': 'Omdia',
	'www.mobilesquared.co.uk': 'Mobilesquared',
	'www.vodafone.com': 'Vodafone',
	'newsroom.kddi.com': 'KDDI',
	'www.lguplus.com': 'LG U+',
	'www.samsung.com': 'Samsung',
	'www.docomo.ne.jp': 'NTT DOCOMO',
	'www.telstra.com.au': 'Telstra',
	'www.att.com': 'AT&T',
	'www.mavenir.com': 'Mavenir',
	'www.airtel.in': 'Bharti Airtel',
	'vivo.com.br': 'Vivo',
	'www.telcel.com': 'Telcel',
	'www.telkomsel.com': 'Telkomsel',
	'www.idx.co.id': 'Indosat (IDX filing)',
	'www.accc.gov.au': 'ACCC',
	'www.kmcc.go.kr': 'Korea Media and Communications Commission',
	'www.broadnet.me': 'BroadNet',
	'www.digitalchina.gov.cn': 'Digital China portal',
	'www.webex.com': 'Webex / Mobilesquared',
	'www.mobiletime.com.br': 'Mobile Time',
}
INFOBIP = 'https://www.gsma.com/futurenetworks/wp-content/uploads/2020/03/RCS-Whitepaper-Infobip_Feb20.pdf'

CONFIDENCE_LABEL = {'measured': 'Measured', 'vendor-claim': 'Vendor claim', 'estimate': 'Estimate'}
QUALIFIER = {'gt': 'More than ', 'gte': 'At least ', 'approx': 'About ', None: ''}


def publisher(url: str) -> str:
	if url == INFOBIP:
		return 'Infobip via GSMA'
	host = url.split('/')[2]
	assert host in PUBLISHERS, host
	return PUBLISHERS[host]


def big_number(value: int) -> str:
	for size, word in ((1_000_000_000, 'billion'), (1_000_000, 'million')):
		if value >= size:
			text = f'{value / size:.3f}'.rstrip('0').rstrip('.')
			assert round(float(text) * size) == value, value
			return f'{text} {word}'
	return f'{value:,}'


def month(date: str) -> str:
	names = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
	parts = date.split('-')
	if len(parts) == 1:
		return parts[0]
	text = f'{names[int(parts[1]) - 1]} {parts[0]}'
	return f'{int(parts[2])} {text}' if len(parts) == 3 else text


def confidence_swatch(confidence: str, size: int = 14) -> str:
	fills = {
		'measured': 'style="fill:var(--bar)"',
		'vendor-claim': 'fill="url(#hatch-bar)" style="stroke:var(--bar)" stroke-width="1.5"',
		'estimate': 'style="fill:none;stroke:var(--bar)" stroke-width="1.5" stroke-dasharray="3 2"',
	}
	inner = size - 2
	return (
		f'<svg width="{size}" height="{size}" aria-hidden="true">'
		f'<rect x="1" y="1" width="{inner}" height="{inner}" rx="3" {fills[confidence]}/></svg>'
	)


def confidence_legend() -> str:
	items = ''.join(f'<li>{confidence_swatch(key)}{label}</li>' for key, label in CONFIDENCE_LABEL.items())
	return f'<ul class="legend" aria-label="Confidence key">{items}</ul>'


def short_url(url: str) -> str:
	text = url.split('://', 1)[1].removeprefix('www.').split('?')[0].rstrip('/')
	return text if len(text) <= 64 else text[:63] + '…'


def sources_block(urls: list[str]) -> str:
	unique = list(dict.fromkeys(urls))
	items = ''.join(
		f'<li><a href="{escape(url)}">{escape(publisher(url))}</a> <span class="muted">{escape(short_url(url))}</span></li>'
		for url in unique
	)
	return f'<section class="sources"><h2>Sources</h2><ul>{items}</ul></section>'


def gaps_block(items: list[str]) -> str:
	body = ''.join(f'<li>{item}</li>' for item in items)
	return f'<section class="gaps"><h2>What this data cannot tell you</h2><ul>{body}</ul></section>'


def page(title: str, css: str, body: str, data: object) -> str:
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
<script type="application/json" id="chart-data">
{payload}
</script>
</body>
</html>
"""


def write(name: str, html: str) -> None:
	(HERE / name).write_text(html)
	print(f'wrote {name}')


# ---------- 1. adoption timeline ----------

FIGURE_LABEL = {
	'rcs_monthly_users': 'Monthly RCS users',
	'rcs_addressable_connections': 'Connections able to receive RCS',
	'rcs_capable_subscribers': 'RCS-capable subscribers',
	'rcs_people_with_access': 'People with RCS',
	'google_messages_monthly_active_users_with_rcs_enabled': 'Google Messages monthly users with RCS on',
	'rcs_active_users_juniper_2023_study': 'Active RCS users',
	'rcs_business_installed_base_omdia': 'People reachable by RCS business messages',
	'rcs_users_mobilesquared_2024_study': 'RCS users, incl. modeled iPhone uplift',
	'rcs_capable_devices': 'RCS-capable devices',
	'rcs_active_users_gsma_industry_services': 'Active RCS users, year-end projection',
}

EVENT_TITLE = {
	('2019-11-14', 'US'): 'Google starts broad RCS rollout in the US',
	('2020-11-19', 'Worldwide'): 'Google Messages RCS goes global on Android',
	('2021-06-15', 'Worldwide'): 'End-to-end encryption for one-to-one Google Messages chats',
	('2023-02', 'Europe'): 'Vodafone makes Google Messages the Android default',
	('2023-08-08', 'Worldwide'): 'RCS on by default in Google Messages; encrypted group chats',
	('2024-09-16', 'Worldwide'): 'iPhone gets RCS with iOS 18, where carriers support it',
	('2024-10', 'Worldwide'): 'iOS 18.1 adds RCS business messages',
	('2025-03-14', 'Worldwide'): 'Universal Profile 3.0 adds cross-platform encryption spec',
	('2025-04-01', 'JP'): 'KDDI (au, UQ, povo) turns on iPhone RCS in Japan',
	('2025-07-25', 'Worldwide'): 'Universal Profile 3.1: audio messages, onboarding',
	('2025-09', 'KR'): 'Korea’s three carriers add iPhone RCS with iOS 26',
	('2026-03-26', 'Worldwide'): 'Universal Profile 4.0: richer text, media, path to video',
	('2026-05-11', 'Worldwide'): 'Encrypted iPhone–Android RCS begins in beta',
	('2026-07-06', 'US'): 'Samsung Messages retired in the US (Android 12+)',
	('2026-07-21', 'Worldwide'): 'Universal Profile 4.1 refines encryption interop',
	('2026-08-24', 'JP'): 'NTT DOCOMO runs its own RCS; iPhone path needs iOS 27',
	('2026-09', 'Worldwide'): 'iOS 27 adds Tapbacks and inline replies over RCS',
	('2026-11-16', 'AU'): 'Telstra starts carrier RCS rollout in Australia',
}
KEY_EVENTS = {('2020-11-19', 'Worldwide'), ('2024-09-16', 'Worldwide'), ('2026-05-11', 'Worldwide')}
SKIPPED_EVENT_KINDS = {'model_publication', 'forecast_publication', 'usage_disclosure', 'traffic_disclosure'}

TIMELINE_CSS = """
.year { font-size: 40px; margin: 40px 0 8px; color: var(--ink); }
.rows { list-style: none; margin: 0; padding: 0; }
.row { display: grid; grid-template-columns: 76px 1fr; gap: 12px; padding: 8px 0; border-top: 1px solid var(--rule); }
.row .when { font-size: 13px; color: var(--ink-2); font-variant-numeric: tabular-nums; padding-top: 2px; }
.event .what { display: flex; gap: 8px; align-items: baseline; }
.event .what svg { flex: none; transform: translateY(2px); }
.event.key .what { font-weight: 650; }
.tag { font-size: 12px; color: var(--ink-2); border: 1px solid var(--rule); border-radius: 99px; padding: 0 8px; white-space: nowrap; }
.figure .value { font-weight: 650; font-variant-numeric: tabular-nums; }
.figure .label { color: var(--ink-2); font-size: 14px; }
.figure svg { margin: 6px 0 2px; }
.figure.missing .value { font-weight: 600; }
.figure .meta { font-size: 12px; color: var(--ink-2); }
.overview { width: 100%; max-width: 600px; height: auto; margin: 0 0 32px; font-size: 11px; fill: var(--ink-2); font-variant-numeric: tabular-nums; }
.overview .strong { fill: var(--ink); font-weight: 600; }
@media (min-width: 640px) { .row { grid-template-columns: 104px 1fr; } }
"""


def event_marker(key: bool) -> str:
	r = 6 if key else 4.5
	return (
		f'<svg width="14" height="14" aria-hidden="true"><circle cx="7" cy="7" r="{r}" '
		'fill="url(#hatch-ink)" style="stroke:var(--ink-2)" stroke-width="1.5"/></svg>'
	)


def bar_svg(value: int, scale_max: int, confidence: str, title: str) -> str:
	width = value / scale_max * 100
	fills = {
		'measured': 'style="fill:var(--bar)"',
		'vendor-claim': 'fill="url(#hatch-bar)" style="stroke:var(--bar)" stroke-width="1.5"',
		'estimate': 'style="fill:none;stroke:var(--bar)" stroke-width="2" stroke-dasharray="4 3"',
	}
	return (
		f'<svg width="100%" height="16" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
		'<rect x="0" y="1" width="100%" height="14" rx="3" style="fill:var(--surface-2)"/>'
		f'<rect x="0.75" y="1.75" width="{width:.3f}%" height="12.5" rx="3" {fills[confidence]}/></svg>'
	)


def timeline_figure_row(row: dict, scale_max: int) -> str:
	label = FIGURE_LABEL[row['metric']]
	value = f'{QUALIFIER[row["qualifier"]]}{big_number(row["value"])}'
	source = publisher(row['source_url'])
	kind = {'forecast': 'Forecast', 'model': 'Model', 'observation': 'Reported'}[row['kind']]
	confidence = CONFIDENCE_LABEL[row['confidence']]
	title = f'{value} {row["unit"]}: {label}. {kind}, {confidence.lower()}, {source}, {month(row["date"])}. {row["note"]}'
	return f"""<li class="row figure">
	<span class="when">{month(row['date'])}</span>
	<div>
		<span class="value">{value}</span> <span class="label">{escape(label)}</span>
		{bar_svg(row['value'], scale_max, row['confidence'], title)}
		<span class="meta">{kind} · {confidence} · <a href="{escape(row['source_url'])}">{escape(source)}</a></span>
	</div>
</li>"""


def timeline_event_row(row: dict) -> str:
	key = (row['date'], row['geography'])
	title = EVENT_TITLE[key]
	geo = 'Global' if row['geography'] == 'Worldwide' else row['geography']
	klass = 'row event key' if key in KEY_EVENTS else 'row event'
	return f"""<li class="{klass}" title="{escape(row['note'])}">
	<span class="when">{month(row['date'])}</span>
	<div class="what">{event_marker(key in KEY_EVENTS)}<span>{escape(title)} <span class="tag">{geo}</span> <a class="small muted" href="{escape(row['source_url'])}">{escape(publisher(row['source_url']))}</a></span></div>
</li>"""


def launches_row(launches: dict, countries: dict) -> str:
	assert launches['date'] == countries['date'] and launches['source_url'] == countries['source_url']
	text = f'{launches["value"]} operator launches in {countries["value"]} countries'
	return f"""<li class="row event" title="{escape(launches['note'])}">
	<span class="when">{month(launches['date'])}</span>
	<div class="what">{event_marker(False)}<span>{text} <span class="tag">Global</span> <a class="small muted" href="{escape(launches['source_url'])}">{escape(publisher(launches['source_url']))}</a></span></div>
</li>"""


def year_position(date: str) -> float:
	parts = date.split('-')
	if len(parts) == 1:
		return int(parts[0]) + 0.5
	return int(parts[0]) + (int(parts[1]) - 0.5) / 12


def overview_svg(figures: list[dict], iphone_date: str, scale_max: int) -> str:
	width, height = 400, 230
	left, right, top, bottom = 34, 12, 14, 24
	x0, x1 = 2019, 2027
	assert scale_max <= 6_000_000_000

	def x(pos: float) -> float:
		return left + (pos - x0) / (x1 - x0) * (width - left - right)

	def y(value: float) -> float:
		return top + (1 - value / 6_000_000_000) * (height - top - bottom)

	parts = []
	for b in range(0, 7, 2):
		parts.append(
			f'<line x1="{left}" x2="{width - right}" y1="{y(b * 1e9):.1f}" y2="{y(b * 1e9):.1f}" style="stroke:var(--rule)" stroke-width="1"/>'
			f'<text x="{left - 6}" y="{y(b * 1e9) + 3.5:.1f}" text-anchor="end">{b}B</text>'
		)
	for year in range(x0, x1):
		parts.append(f'<text x="{x(year + 0.5):.1f}" y="{height - 6}" text-anchor="middle">{year}</text>')
	ix = x(year_position(iphone_date))
	parts.append(
		f'<line x1="{ix:.1f}" x2="{ix:.1f}" y1="{top}" y2="{height - bottom}" style="stroke:var(--ink-2)" stroke-width="1"/>'
		f'<text x="{ix + 4:.1f}" y="{height - bottom - 6}" class="strong">iPhone joins</text>'
	)
	marks = {
		'vendor-claim': 'fill="url(#hatch-bar)" style="stroke:var(--bar)" stroke-width="1.5"',
		'estimate': 'style="fill:var(--surface);stroke:var(--bar)" stroke-width="1.5" stroke-dasharray="3 2"',
		'measured': 'style="fill:var(--bar);stroke:var(--surface)" stroke-width="2"',
	}
	seen: dict[tuple, int] = {}
	for r in figures:
		spot = (year_position(r['date']), r['value'])
		nudge = seen.get(spot, 0)
		seen[spot] = nudge + 1
		cx, cy = x(spot[0]) + nudge * 7, y(r['value'])
		title = (
			f'{QUALIFIER[r["qualifier"]]}{big_number(r["value"])} {FIGURE_LABEL[r["metric"]].lower()} '
			f'({month(r["date"])}, {CONFIDENCE_LABEL[r["confidence"]].lower()}, {publisher(r["source_url"])})'
		)
		parts.append(
			f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" {marks[r["confidence"]]}><title>{escape(title)}</title></circle>'
		)
	billion = next(
		r for r in figures if r['metric'] == 'google_messages_monthly_active_users_with_rcs_enabled'
	)
	top_row = max(figures, key=lambda r: r['value'])
	labels = [
		(figures[0], 'start', 8, -8, f'{big_number(figures[0]["value"])} users'),
		(billion, 'end', -6, -20, f'>{big_number(billion["value"])} Google Messages'),
		(top_row, 'end', -9, 4, f'{big_number(top_row["value"])} capable devices'),
	]
	for r, anchor, dx, dy, text in labels:
		parts.append(
			f'<text x="{x(year_position(r["date"])) + dx:.1f}" y="{y(r["value"]) + dy:.1f}" '
			f'text-anchor="{anchor}" class="strong">{escape(text)}</text>'
		)
	return (
		f'<svg class="overview" viewBox="0 0 {width} {height}" role="img" '
		'aria-label="Dot plot of published RCS user and capability figures from 2019 to 2026, rising from '
		'300 million to 6 billion. Points are not connected because definitions differ.">'
		f'{"".join(parts)}</svg>'
	)


def build_timeline() -> None:
	figures = [r for r in DATA['global_adoption'] if r['value'] is not None]
	missing = [r for r in DATA['global_adoption'] if r['value'] is None]
	events = [r for r in DATA['timeline'] if r['kind'] not in SKIPPED_EVENT_KINDS]
	coverage = [r for r in DATA['carrier_coverage'] if r['value'] is not None]
	launch_pairs = [
		(r, next(c for c in coverage if c['date'] == r['date'] and c['metric'].startswith('markets_')))
		for r in coverage
		if r['metric'] == 'reported_rcs_operator_launches'
	]
	scale_max = max(r['value'] for r in figures)

	entries = []
	for r in figures:
		entries.append((r['date'], 1, timeline_figure_row(r, scale_max)))
	for r in events:
		entries.append((r['date'], 0, timeline_event_row(r)))
	for launches, countries in launch_pairs:
		entries.append((launches['date'], 0, launches_row(launches, countries)))
	entries.sort(key=lambda e: (e[0][:4], e[0].ljust(10, '~'), e[1]))

	years = []
	for year in sorted({e[0][:4] for e in entries}):
		rows = '\n'.join(e[2] for e in entries if e[0][:4] == year)
		years.append(f'<h2 class="year">{year}</h2>\n<ol class="rows">\n{rows}\n</ol>')

	billion_mark = next(
		r for r in figures if r['metric'] == 'google_messages_monthly_active_users_with_rcs_enabled'
	)
	iphone = next(r for r in events if r['date'] == '2024-09-16')
	headline = (
		f'{QUALIFIER[billion_mark["qualifier"]]}{big_number(billion_mark["value"])} monthly Google Messages users '
		f'had RCS on by {billion_mark["date"][:4]}. Then the iPhone joined in {iphone["date"][:4]}.'
	)

	table_rows = ''.join(
		f'<tr><td class="num">{r["date"]}</td><td>{escape(FIGURE_LABEL[r["metric"]])}</td>'
		f'<td class="num">{QUALIFIER[r["qualifier"]]}{r["value"]:,}</td><td>{r["unit"]}</td>'
		f'<td>{r["kind"]}</td><td>{r["confidence"]}</td><td><a href="{escape(r["source_url"])}">{escape(publisher(r["source_url"]))}</a></td></tr>'
		for r in figures
	)
	missing_rows = ''.join(
		f'<tr><td class="num">{r["date"]}</td><td>{escape(r["metric"])}</td><td class="num">unknown</td>'
		f'<td>{r["unit"]}</td><td>missing</td><td>—</td><td><a href="{escape(r["source_url"])}">{escape(publisher(r["source_url"]))}</a></td></tr>'
		for r in missing
	)
	gap_row = f"""<li class="row figure missing">
	<span class="when">{month(AS_OF)}</span>
	<div>
		<span class="value">Unknown</span> <span class="label">Current worldwide monthly RCS users, all apps</span>
		<svg width="100%" height="16" role="img" aria-label="No verified current total"><title>No public, deduplicated 2025–2026 count with a defined monthly activity window was verified.</title><rect x="0.75" y="1.75" width="99%" height="12.5" rx="3" style="fill:none;stroke:var(--gap)" stroke-width="1" stroke-dasharray="2 4"/></svg>
		<span class="meta">No verified count exists in the dataset</span>
	</div>
</li>"""
	years[-1] = years[-1].replace('\n</ol>', f'\n{gap_row}\n</ol>')

	urls = [r['source_url'] for r in figures + events + coverage]
	body = f"""<p class="eyebrow">RCS adoption, 2019 to {month(AS_OF)}</p>
<h1>{escape(headline)}</h1>
<p class="caption">Each dot and bar is one published figure, drawn to the same scale (full width = {
		big_number(scale_max)
	}, the largest figure). The figures count different things — users, capable devices, connections — so they are not joined into one line. Forecasts and models are estimates.</p>
{confidence_legend()}
{overview_svg(sorted(figures, key=lambda r: r['date']), iphone['date'], scale_max)}
<ul class="legend"><li>{
		event_marker(False)
	}Milestone (vendor announcement)</li><li><span class="tag">Global</span> Where it applies</li></ul>
{''.join(years)}
{
		gaps_block(
			[
				'There is no current, deduplicated count of people who actually use RCS each month. The dataset records this as unknown.',
				'Google’s 2023 figures each use a different definition (monthly users, people with access, monthly Google Messages users with RCS on). They are shown as separate points, not a trend.',
				'The 2026 figures of 3.8 billion are projections, and one counts capable subscribers rather than active users.',
				'The last operator census in the data is from June 2020. Current operator and country counts are unknown.',
			]
		)
	}
{sources_block(urls)}
<details><summary>Data table</summary><div class="table-wrap"><table class="data">
<thead><tr><th>Date</th><th>Figure</th><th>Value</th><th>Unit</th><th>Kind</th><th>Confidence</th><th>Source</th></tr></thead>
<tbody>{table_rows}{missing_rows}</tbody></table></div></details>
<p class="small muted">Data as of {
		AS_OF
	}. Business-messaging traffic and market-level counts are left out of this chart.</p>"""
	write(
		'adoption-timeline.html',
		page(
			'RCS adoption timeline',
			TIMELINE_CSS,
			body,
			{
				'as_of': AS_OF,
				'global_adoption': DATA['global_adoption'],
				'timeline': events,
				'carrier_coverage': coverage,
			},
		),
	)


# ---------- 2. country coverage ----------

ANDROID_STATUS = {
	'confirmed': ('live', 'Documented'),
	'documented_historically': ('partial', 'Historical only'),
	'announced_historically': ('partial', 'Announced only'),
	'carrier_ecosystem': ('partial', 'Domestic system'),
	'unverified': ('unknown', 'Unverified'),
}
STATUS_LABEL = {
	'live': 'Live',
	'partial': 'Partial or dated',
	'none': 'None listed',
	'unknown': 'Unverified',
}
SCORE = {'live': 2, 'partial': 1, 'none': 0, 'unknown': 0}
GROUPS = (
	('both', 'RCS documented on both iPhone and Android'),
	('one', 'Documented on one platform only'),
	('neither', 'Not currently documented on either'),
)

COUNTRY_CSS = """
table.matrix { border-collapse: collapse; width: 100%; font-size: 14px; }
.matrix th, .matrix td { text-align: left; padding: 8px 6px; border-bottom: 1px solid var(--rule); vertical-align: top; }
.matrix thead th { font-size: 12px; letter-spacing: 0.05em; text-transform: uppercase; color: var(--ink-2); font-weight: 600; vertical-align: bottom; }
.matrix thead th span { display: block; text-transform: none; letter-spacing: 0; font-weight: 400; }
.matrix tbody th[colspan] { padding-top: 24px; font-family: 'Iowan Old Style', 'Palatino Linotype', Palatino, Charter, Georgia, serif; font-size: 19px; font-weight: 600; letter-spacing: -0.01em; border-bottom: 1px solid var(--ink-2); }
.matrix tbody th[colspan] .count { font-family: system-ui, sans-serif; font-size: 13px; font-weight: 400; color: var(--ink-2); }
.matrix .market { font-weight: 600; }
.matrix .market small { display: block; font-weight: 400; color: var(--ink-2); }
.cell { display: flex; gap: 6px; align-items: flex-start; }
.cell svg { flex: none; margin-top: 2px; }
.cell small { display: block; color: var(--ink-2); }
.matrix td { width: 25%; }
@media (max-width: 480px) { .matrix .market small { display: none; } .matrix { font-size: 13px; } .matrix th, .matrix td { padding: 8px 3px; } .cell { flex-direction: column; gap: 2px; } }
"""


def status_glyph(status: str, confidence: str, label: str) -> str:
	solid = confidence == 'measured'
	ring = 'style="fill:none;stroke:var(--ink-2)" stroke-width="1.5"'
	if status == 'live':
		fill = (
			'style="fill:var(--live)"'
			if solid
			else 'fill="url(#hatch-live)" style="stroke:var(--live)" stroke-width="2"'
		)
		shape = f'<circle cx="9" cy="9" r="7" {fill}/>'
	elif status == 'partial':
		fill = 'style="fill:var(--partial)"' if solid else 'fill="url(#hatch-partial)"'
		shape = f'<path d="M9 2 A7 7 0 0 0 9 16 Z" {fill}/><circle cx="9" cy="9" r="7" {ring}/>'
	elif status == 'none':
		shape = '<circle cx="9" cy="9" r="6.5" style="fill:none;stroke:var(--gap)" stroke-width="1.5"/>'
	else:
		assert status == 'unknown', status
		shape = (
			'<circle cx="9" cy="9" r="6.5" style="fill:none;stroke:var(--gap)" stroke-width="1.5" stroke-dasharray="2 2"/>'
			'<text x="9" y="12.5" text-anchor="middle" font-size="10" font-weight="700" style="fill:var(--ink-2)">?</text>'
		)
	return f'<svg width="18" height="18" role="img" aria-label="{escape(label)}">{shape}</svg>'


def market_cells(m: dict) -> dict:
	iphone = m['iphone']
	assert iphone['confidence'] == 'measured'
	listed = iphone['status'] == 'listed'
	assert listed == (iphone['value'] > 0)
	n = iphone['value']
	enc = len(iphone['encryption_beta_carriers'])
	if m['country_code'] == 'US':
		iphone_text = f'{n} selected carriers'
	else:
		iphone_text = f'{n} carrier{"s" if n != 1 else ""}' if listed else 'None listed'
	iphone_cell = (
		'live' if listed else 'none',
		'measured',
		iphone_text,
		', '.join(iphone['carriers']) or iphone['note'],
	)

	assert all(e['confidence'] == 'vendor-claim' for e in m['evidence'])
	status, text = ANDROID_STATUS[m['android_status']]
	latest = max(e['date'] for e in m['evidence'])
	android_note = ' | '.join(f'{e["date"]}: {e["note"]}' for e in m['evidence'])
	android_cell = (status, 'vendor-claim', text, android_note, f'latest {latest[:4]}')

	if not listed:
		enc_cell = ('none', 'measured', 'n/a', 'No iPhone RCS carrier listed')
	elif enc == n:
		enc_cell = ('live', 'measured', f'All {n}', ', '.join(iphone['encryption_beta_carriers']))
	elif enc:
		enc_cell = ('partial', 'measured', f'{enc} of {n}', ', '.join(iphone['encryption_beta_carriers']))
	else:
		enc_cell = (
			'none',
			'measured',
			'None listed',
			'No carrier in this market is listed for the encryption beta',
		)
	return {'iphone': iphone_cell, 'android': android_cell, 'enc': enc_cell}


def market_group(cells: dict) -> str:
	iphone_live = cells['iphone'][0] == 'live'
	android_live = cells['android'][0] == 'live'
	if iphone_live and android_live:
		return 'both'
	if iphone_live or android_live:
		return 'one'
	return 'neither'


def cell_html(cell: tuple) -> str:
	status, confidence, text, note, *extra = cell
	sub = f'<small>{escape(extra[0])}</small>' if extra else ''
	label = f'{STATUS_LABEL[status]}, {CONFIDENCE_LABEL[confidence].lower()}: {text}'
	return (
		f'<td title="{escape(note)}"><div class="cell">{status_glyph(status, confidence, label)}'
		f'<span>{escape(text)}{sub}</span></div></td>'
	)


def build_country() -> None:
	markets = DATA['markets']
	rows = []
	for m in markets:
		cells = market_cells(m)
		score = sum(SCORE[c[0]] for c in cells.values())
		rows.append((market_group(cells), -score, m['country'], m, cells))
	rows.sort()
	counts = {key: sum(1 for r in rows if r[0] == key) for key, _ in GROUPS}

	body_rows = []
	for key, title in GROUPS:
		group_rows = [r for r in rows if r[0] == key]
		if not group_rows:
			continue
		body_rows.append(
			f'<tr><th colspan="4" scope="rowgroup">{title} <span class="count">{len(group_rows)} markets</span></th></tr>'
		)
		for _, _, _, m, cells in group_rows:
			body_rows.append(
				f'<tr><th scope="row" class="market">{escape(m["country"])}<small>{escape(m["region"])}</small></th>'
				f'{cell_html(cells["iphone"])}{cell_html(cells["android"])}{cell_html(cells["enc"])}</tr>'
			)

	legend_status = ''.join(
		f'<li>{status_glyph(s, "measured", STATUS_LABEL[s])}{STATUS_LABEL[s]}</li>' for s in STATUS_LABEL
	)
	legend_conf = (
		f'<li>{status_glyph("live", "measured", "Solid")}Solid: counted from Apple’s carrier directory</li>'
		f'<li>{status_glyph("live", "vendor-claim", "Hatched")}Hatched: vendor or carrier claim</li>'
	)
	headline = f'{counts["both"]} of {len(markets)} markets have documented RCS on both iPhone and Android.'
	urls = [m['iphone']['source_url'] for m in markets] + [
		e['source_url'] for m in markets for e in m['evidence']
	]
	body = f"""<p class="eyebrow">RCS by market, local lines, {month(AS_OF)}</p>
<h1>{escape(headline)}</h1>
<p class="caption">For a traveler, “documented” means a local line in that country can use RCS: Apple lists iPhone carriers there, or carriers and Google document Android service. It says nothing about roaming on your home number or data-only travel eSIMs.</p>
<ul class="legend" aria-label="Status key">{legend_status}</ul>
<ul class="legend" aria-label="Confidence key">{legend_conf}</ul>
<div class="table-wrap"><table class="matrix">
<thead><tr><th scope="col">Market</th><th scope="col">iPhone<span>Apple-listed carriers</span></th><th scope="col">Android<span>Carrier or Google evidence</span></th><th scope="col">Encrypted<span>iPhone↔Android beta</span></th></tr></thead>
<tbody>
{chr(10).join(body_rows)}
</tbody></table></div>
<p class="small muted">Hover or long-press a cell for the carrier names or evidence notes. “Historical only” means the newest evidence is an old launch record or a business-messaging listing.</p>
{
		gaps_block(
			[
				'No market in the data has a count of active RCS users. Every country-level user total is unknown.',
				'Android evidence is vendor or carrier claims, some of it years old. The year under each Android cell is the newest evidence.',
				'iPhone counts are carrier brand names in Apple’s directory. Brands can share a network, and no subscriber totals are attached.',
				'United States: only 3 selected national brands are counted. Apple lists more.',
				'China mainland: Apple lists the three operators, but whether RCS reaches Google’s network or works for overseas numbers is unverified.',
				'Australia: Telstra started a rollout on 16 Nov 2026; iPhone availability there is unverified. Apple’s lists and carrier pages can lag.',
			]
		)
	}
{sources_block(urls)}
<p class="small muted">Data as of {AS_OF}.</p>"""
	write(
		'country-coverage.html',
		page('RCS coverage by market', COUNTRY_CSS, body, {'as_of': AS_OF, 'markets': markets}),
	)


# ---------- 3. platform support ----------

FEATURE_TITLE = {
	('Android / Google Messages', '2020-11-19'): 'RCS through Google or the carrier',
	('Android / Google Messages', '2023-08-08'): 'RCS on by default',
	('Android / Samsung Messages', '2026-07-06'): 'Samsung Messages retired in the US',
	('iPhone / iOS 18+', '2024-09-16'): 'Native RCS on supported carriers',
	('iPhone / iOS 26', '2026-05'): 'Pick any default texting app',
	(
		'iPhone / iOS 26.5 and Google Messages',
		'2026-05-11',
	): 'End-to-end encrypted chats, in beta, on by default',
	('iPhone / iOS 27', '2026-09'): 'Tapbacks and inline replies over RCS',
}

PLATFORM_CSS = """
.lanes { display: grid; grid-template-columns: minmax(0, 1fr); gap: 32px; margin: 8px 0 0; }
@media (min-width: 640px) { .lanes { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.lane h2 { margin: 0 0 8px; font-size: 22px; }
.lane h2 small { display: block; font-family: system-ui, sans-serif; letter-spacing: 0; color: var(--ink-2); font-weight: 400; }
.steps { list-style: none; margin: 0; padding: 0; }
.steps li { display: grid; grid-template-columns: 18px 1fr; gap: 8px; padding: 8px 0; border-top: 1px solid var(--rule); }
.steps li svg { margin-top: 4px; }
.steps .when { display: block; font-size: 13px; color: var(--ink-2); }
.steps .platform { font-size: 13px; color: var(--ink-2); }
.tile { margin-top: 12px; padding: 12px 14px; border-radius: 10px; background: var(--surface-2); }
.tile b { display: block; font-size: 22px; font-variant-numeric: tabular-nums; }
.tile.gap { background: none; border: 1px dashed var(--gap); }
.tile.gap b { color: var(--ink-2); }
.between { margin-top: 32px; padding: 16px 0 0; border-top: 2px solid var(--ink); }
.between h2 { margin: 0 0 8px; font-size: 22px; }
.carriers { list-style: none; margin: 16px 0 0; padding: 0; }
.carriers li { display: grid; grid-template-columns: 112px 1fr; gap: 10px; align-items: center; padding: 4px 0; }
.carriers .name { font-size: 14px; font-weight: 600; }
.carriers .bar { display: flex; align-items: center; gap: 8px; min-width: 0; }
.carriers .bar svg { flex: none; min-width: 0; }
.carriers .bar span { flex: none; font-size: 13px; color: var(--ink-2); font-variant-numeric: tabular-nums; }
"""


def lane_step(f: dict) -> str:
	title = FEATURE_TITLE[(f['platform'], f['date'])]
	sub = f['platform'].split(' / ', 1)[1]
	return (
		f'<li title="{escape(f["note"])}">{confidence_swatch(f["confidence"], 16)}<div>'
		f'<span class="when">{month(f["date"])} · <span class="platform">{escape(sub)}</span></span>'
		f'{escape(title)} <a class="small muted" href="{escape(f["source_url"])}">{escape(publisher(f["source_url"]))}</a></div></li>'
	)


def carrier_bar(m: dict, scale_max: int) -> str:
	n = m['iphone']['value']
	enc = len(m['iphone']['encryption_beta_carriers'])
	enc_w = enc / n * 100
	rest_w = (n - enc) / n * 100
	label = f'{enc} of {n}' if m['country_code'] != 'US' else f'{enc} of {n} selected'
	title = f'{m["country"]}: {n} carrier brands listed for iPhone RCS, {enc} listed for the encryption beta. Encrypted: {", ".join(m["iphone"]["encryption_beta_carriers"]) or "none"}.'
	rects = ''
	if enc:
		rects += f'<rect x="0" y="2" width="{enc_w:.3f}%" height="14" rx="3" style="fill:var(--bar);stroke:var(--surface)" stroke-width="2"/>'
	if n - enc:
		rects += f'<rect x="{enc_w:.3f}%" y="2" width="{rest_w:.3f}%" height="14" rx="3" style="fill:var(--bar-soft);stroke:var(--surface)" stroke-width="2"/>'
	return (
		f'<li><span class="name">{escape(m["country"])}</span><span class="bar">'
		f'<svg height="18" style="width:calc((100% - 96px) * {n / scale_max:.4f})" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>{rects}</svg>'
		f'<span>{label}</span></span></li>'
	)


def build_platform() -> None:
	features = DATA['platform_features']
	shared = [
		f for f in features if 'Google Messages' in f['platform'] and f['platform'].startswith('iPhone')
	]
	android = [f for f in features if f['platform'].startswith('Android')]
	iphone = [f for f in features if f['platform'].startswith('iPhone') and f not in shared]
	assert len(shared) + len(android) + len(iphone) == len(features)
	downloads = next(r for r in DATA['device_support'] if r['metric'] == 'google_messages_play_downloads')
	default_share = next(
		r for r in DATA['device_support'] if r['metric'].startswith('android_devices_with_google_messages')
	)
	encrypted_share = next(
		r for r in DATA['device_support'] if r['metric'].startswith('cross_platform_encrypted')
	)
	assert default_share['value'] is None and encrypted_share['value'] is None

	listed = sorted(
		(m for m in DATA['markets'] if m['iphone']['value'] > 0),
		key=lambda m: (-m['iphone']['value'], -len(m['iphone']['encryption_beta_carriers']), m['country']),
	)
	unlisted = sorted(m['country'] for m in DATA['markets'] if m['iphone']['value'] == 0)
	total = sum(m['iphone']['value'] for m in listed)
	enc_total = sum(len(m['iphone']['encryption_beta_carriers']) for m in listed)
	scale_max = max(m['iphone']['value'] for m in listed)

	headline = f'Both phones speak RCS now. Encryption between them is in beta on {enc_total} of the {total} iPhone carrier brands counted here.'
	urls = (
		[f['source_url'] for f in features]
		+ [u for f in features for u in f.get('source_urls', [])]
		+ [downloads['source_url'], default_share['source_url'], encrypted_share['source_url']]
		+ [m['iphone']['source_url'] for m in listed]
	)
	body = f"""<p class="eyebrow">RCS platform support, {month(AS_OF)}</p>
<h1>{escape(headline)}</h1>
<p class="caption">Android has had RCS through Google Messages since 2020. iPhone added it with iOS 18 in 2024, but only on carriers Apple lists. Messages between the two can now be end-to-end encrypted, in a beta that depends on the iPhone’s carrier.</p>
{confidence_legend()}
<div class="lanes">
	<section class="lane">
		<h2>Android<small>Google Messages, carrier or Google-hosted</small></h2>
		<ol class="steps">{''.join(lane_step(f) for f in android)}</ol>
		<div class="tile" title="{escape(downloads['note'])}"><b>{QUALIFIER[downloads['qualifier']]}{
		big_number(downloads['value'])
	}</b>Google Play downloads of Google Messages. Vendor claim; downloads are not devices or users.</div>
		<div class="tile gap" title="{
		escape(default_share['note'])
	}"><b>Unknown</b>Share of Android phones with Google Messages as the default app</div>
	</section>
	<section class="lane">
		<h2>iPhone<small>Messages app, carrier must support it</small></h2>
		<ol class="steps">{''.join(lane_step(f) for f in iphone)}</ol>
		<div class="tile" title="Measured from Apple carrier directories"><b>{
		total
	} carrier brands</b>listed for iPhone RCS across {len(listed)} of the {
		len(DATA['markets'])
	} markets in this data</div>
	</section>
</div>
<section class="between">
	<h2>Between iPhone and Android</h2>
	<ol class="steps">{''.join(lane_step(f) for f in shared)}</ol>
	<div class="tile gap" title="{
		escape(encrypted_share['note'])
	}"><b>Unknown</b>Share of iPhone–Android chats that are actually encrypted</div>
</section>
<h2>iPhone RCS carriers by market</h2>
<p class="caption">Carrier brands Apple lists for RCS. Dark part: also listed for the encrypted beta.</p>
<ul class="legend" aria-label="Bar key">
	<li><svg width="14" height="14" aria-hidden="true"><rect x="1" y="1" width="12" height="12" rx="3" style="fill:var(--bar)"/></svg>Encrypted beta listed</li>
	<li><svg width="14" height="14" aria-hidden="true"><rect x="1" y="1" width="12" height="12" rx="3" style="fill:var(--bar-soft)"/></svg>RCS only</li>
	<li>Solid: counted from Apple’s directory</li>
</ul>
<ul class="carriers">{''.join(carrier_bar(m, scale_max) for m in listed)}</ul>
<p class="small muted">No iPhone RCS carrier listed: {', '.join(unlisted)}.</p>
{
		gaps_block(
			[
				'Nobody publishes how many Android phones use Google Messages as their texting app. Play downloads are cumulative and count reinstalls.',
				'There is no figure for how many iPhone–Android chats are encrypted. Apple and Google describe a gradual rollout; look for the lock in each conversation.',
				'Carrier counts are brand names, not networks or subscribers. The US row counts only 3 selected national brands; Apple lists more.',
				'Carrier lists and release notes can lag. A feature in the standard is not proof that your carrier has switched it on.',
			]
		)
	}
{sources_block(urls)}
<p class="small muted">Data as of {AS_OF}.</p>"""
	write(
		'platform-support.html',
		page(
			'RCS platform support',
			PLATFORM_CSS,
			body,
			{
				'as_of': AS_OF,
				'platform_features': features,
				'device_support': DATA['device_support'],
				'markets_iphone': [{'country': m['country'], **m['iphone']} for m in DATA['markets']],
			},
		),
	)


if __name__ == '__main__':
	build_timeline()
	build_country()
	build_platform()
