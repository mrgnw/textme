# /// script
# requires-python = '>=3.14'
# dependencies = ['pycountry']
# ///
"""Writes src/lib/rcs/coverage.json.

Uses research/rcs/coverage-by-country.json when present. Otherwise builds a fixture from the
real rows in adoption.json and messaging-by-country.json and marks every other country unknown.
"""

import json
from pathlib import Path

import pycountry

research = Path('research/rcs')
out = Path('src/lib/rcs/coverage.json')

EXTRA_NUMERIC = {'XK': 'XK'}
UNKNOWN_ANDROID = {'status': 'unknown', 'detail': None, 'date': None, 'source_url': None, 'confidence': None}
UNKNOWN_IPHONE = {'status': 'unknown', 'carriers': [], 'date': None, 'source_url': None, 'confidence': None}
ANDROID_STATUS_WORDS = {
	'documented_historically': 'A launch is documented historically. Current service is not confirmed.',
	'announced_historically': 'A launch was announced historically. Current service is not confirmed.',
	'unverified': 'Consumer service is not verified.',
	'carrier_ecosystem': 'Carriers run a domestic RCS service. Links with Google Messages are not verified.',
}


def numeric_of(iso2: str) -> str | None:
	if iso2 in EXTRA_NUMERIC:
		return EXTRA_NUMERIC[iso2]
	country = pycountry.countries.get(alpha_2=iso2)
	return country.numeric if country else None


def share(entry: dict | None) -> dict | None:
	if not entry or entry.get('value') is None:
		return None
	return {k: entry[k] for k in ('value', 'date', 'source_url', 'confidence')}


def android_from_market(market: dict) -> dict:
	latest = max(market['evidence'], key=lambda e: e['date'])
	status = market['android_status']
	if status == 'confirmed':
		return {
			'status': 'live',
			'detail': latest['note'],
			**{k: latest[k] for k in ('date', 'source_url', 'confidence')},
		}
	detail = f'{ANDROID_STATUS_WORDS[status]} {latest["note"]}'
	return {
		'status': 'unknown',
		'detail': detail,
		**{k: latest[k] for k in ('date', 'source_url', 'confidence')},
	}


def iphone_from_market(market: dict) -> dict:
	iphone = market['iphone']
	return {k: iphone[k] for k in ('status', 'carriers', 'date', 'source_url', 'confidence')}


def fixture() -> dict:
	adoption = json.loads((research / 'adoption.json').read_text())
	messaging = json.loads((research / 'messaging-by-country.json').read_text())
	markets = {m['country_code']: m for m in adoption['markets']}
	shares = {c['country_iso']: c for c in messaging['countries']}
	rows = []
	for country in pycountry.countries:
		iso2 = country.alpha_2
		market = markets.get(iso2)
		os_row = shares.get(iso2, {})
		rows.append(
			{
				'iso2': iso2,
				'name': getattr(country, 'common_name', country.name),
				'android': android_from_market(market) if market else UNKNOWN_ANDROID,
				'iphone': iphone_from_market(market) if market else UNKNOWN_IPHONE,
				'ios_share': share(os_row.get('ios_share')),
				'android_share': share(os_row.get('android_share')),
				'note': None,
			}
		)
	rows.append(
		{
			'iso2': 'XK',
			'name': 'Kosovo',
			'android': UNKNOWN_ANDROID,
			'iphone': UNKNOWN_IPHONE,
			'ios_share': None,
			'android_share': None,
			'note': None,
		}
	)
	return {'as_of': adoption['as_of'], 'source': 'fixture', 'countries': rows}


def research_data() -> dict:
	data = json.loads((research / 'coverage-by-country.json').read_text())
	return {'as_of': data['as_of'], 'source': 'research', 'countries': data['countries']}


def main():
	data = research_data() if (research / 'coverage-by-country.json').exists() else fixture()
	for row in data['countries']:
		row['n'] = numeric_of(row['iso2'])
	data['countries'].sort(key=lambda r: r['name'])
	out.parent.mkdir(parents=True, exist_ok=True)
	out.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n')
	print(data['source'], len(data['countries']), 'rows ->', out, out.stat().st_size, 'bytes')


main()
