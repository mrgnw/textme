# /// script
# requires-python = ">=3.14"
# ///
import argparse
import csv
import json
import re
import time
from calendar import month_abbr
from datetime import date, timedelta
from html import unescape
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / 'research/rcs/devices-by-region.json'
CACHE = ROOT / 'analysis/cache/statcounter'
SITE = 'https://gs.statcounter.com'
SELECTOR_URL = f'{SITE}/ios-version-market-share/mobile/worldwide'
UNIT = 'percent of sampled mobile web page views for this OS'
ISO_CODES = frozenset(
	"""
AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ BR BS BT BV BW BY
BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK
FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR
IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK
ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM
PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF
TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW
""".split()
)
OS_LABELS = {'ios': 'iOS Version', 'android': 'Android Version'}


def fetch(url, path, parse, offline):
	if path.exists():
		return parse(path.read_text(encoding='utf-8-sig'))
	if offline:
		raise FileNotFoundError(path)
	for delay in (0.6, 3, 12):
		time.sleep(delay)
		try:
			request = Request(url, headers={'User-Agent': 'textme RCS research (github.com/mrgnw/textme)'})
			with urlopen(request, timeout=20) as response:
				raw = response.read(1_000_001)
			if len(raw) > 1_000_000:
				raise ValueError(f'Response too large: {url}')
			result = parse(raw.decode('utf-8-sig'))
			path.parent.mkdir(parents=True, exist_ok=True)
			path.write_bytes(raw)
			return result
		except (URLError, TimeoutError) as error:
			last_error = error
	raise RuntimeError(f'Unable to fetch {url}') from last_error


def parse_selector(html):
	selector = re.search(r'<select\b[^>]*\bid="region"[^>]*>(.*?)</select>', html, re.DOTALL)
	if selector is None:
		raise ValueError('StatCounter region selector is missing')
	names = {
		code: unescape(name.strip())
		for code, name in re.findall(r'<option value="([A-Z]{2})">([^<]+)</option>', selector[1])
		if code in ISO_CODES
	}
	if not names or any(not name for name in names.values()):
		raise ValueError('StatCounter region selector has invalid country names')
	return names


def chart_url(stat, code, month):
	month_int = month.replace('-', '')
	query = urlencode(
		{
			'statType_hidden': stat,
			'region_hidden': code,
			'granularity': 'monthly',
			'fromInt': month_int,
			'toInt': month_int,
			'fromMonthYear': month,
			'toMonthYear': month,
			'device_hidden': 'mobile',
			'csv': 1,
		}
	)
	return f'{SITE}/chart.php?{query}'


def parse_csv(body, label, month):
	year, number = month.split('-')
	reader = csv.reader(body.splitlines(), strict=True)
	expected = [label, f'Market Share Perc. ({month_abbr[int(number)]} {year})']
	if next(reader, None) != expected:
		raise ValueError(f'Expected CSV header {expected!r}')
	shares = {}
	for name, value in reader:
		share = float(value)
		if not name or name in shares or not 0 <= share <= 100:
			raise ValueError(f'Invalid or duplicate CSV row: {(name, value)!r}')
		shares[name] = share
	return shares


def country_exports(month, offline):
	cache = CACHE / month
	names = fetch(SELECTOR_URL, cache / 'regions.html', parse_selector, offline)
	for index, (code, name) in enumerate(sorted(names.items()), start=1):
		for os, label in OS_LABELS.items():
			url = chart_url(f'{os}_version', code, month)
			try:
				shares = fetch(
					url, cache / f'{code}-{os}.csv', lambda body: parse_csv(body, label, month), offline
				)
			except ValueError as error:
				raise ValueError(f'{url}: {error}') from error
			yield code, name, os, url, shares
		if not offline and index % 25 == 0:
			print(f'Checked {index}/{len(names)} ISO geographies', flush=True)


def major_version(os, label):
	if os == 'ios':
		match = re.fullmatch(r'iOS (\d+)(?:\.\d+)*', label)
		if match and int(match[1]) in {*range(1, 19), 26, 27}:
			return int(match[1])
		return None
	match = re.fullmatch(r'(?:Android )?(\d+)\.\d+(?:\.\d+)?(?: [A-Za-z ]+)?', label)
	return int(match[1]) if match and 1 <= int(match[1]) <= 17 else None


def share_row(code, name, os, url, version, value, month):
	return {
		'geo_id': code,
		'geo_name': name,
		'geo_type': 'country',
		'os': os,
		'series': 'statcounter_mobile',
		'version': version,
		'major_version': major_version(os, version),
		'value': value,
		'unit': UNIT,
		'date': month,
		'source_url': url,
		'confidence': 'measured',
	}


def gap(code, name, os, month, url, note):
	return {
		'geo_id': code,
		'geo_name': name,
		'geo_type': 'country',
		'os': os,
		'value': None,
		'unit': UNIT,
		'date': month,
		'source_url': url,
		'confidence': None,
		'note': note,
	}


def country_rows(existing, exports, month):
	added = {}
	fetched = set()
	gaps = []
	covered = {os: set() for os in OS_LABELS}
	names = {}
	historical_names = {row['geo_id']: row['geo_name'] for row in existing if row['geo_type'] == 'country'}
	for code, name, os, url, shares in exports:
		name = historical_names.get(code, name)
		names[code] = name
		fetched.add((code, os))
		if not shares:
			gaps.append(gap(code, name, os, month, url, 'The published CSV contains no version rows.'))
			continue
		covered[os].add(code)
		for version, value in shares.items():
			row = share_row(code, name, os, url, version, value, month)
			added[code, os, version] = row
	for code in sorted(ISO_CODES - names.keys()):
		for os in OS_LABELS:
			gaps.append(
				gap(code, None, os, month, SELECTOR_URL, 'The StatCounter region selector omits this code.')
			)
	merged = []
	for row in existing:
		code, os, version = row['geo_id'], row['os'], row['version']
		is_snapshot = (
			row['geo_type'] == 'country' and row['series'] == 'statcounter_mobile' and row['date'] == month
		)
		if not is_snapshot:
			merged.append(row)
			continue
		if (code, os) not in fetched:
			raise ValueError(f'Existing country series missing from refreshed region selector: {code} {os}')
		new = added.pop((code, os, version), None)
		if new is not None:
			merged.append(row if row['value'] == new['value'] else new)
	merged.extend(added.values())
	return merged, covered, gaps


def validate_shares(rows, covered, month):
	required = {
		'geo_id',
		'geo_name',
		'geo_type',
		'os',
		'series',
		'version',
		'value',
		'unit',
		'date',
		'source_url',
		'confidence',
	}
	keys = set()
	totals = {}
	for row in rows:
		if required - row.keys():
			raise ValueError(f'Missing fields on OS share row: {row}')
		series_field = {
			'statcounter_mobile': 'major_version',
			'apple_app_store': 'cohort',
			'google_android_studio': 'api_level',
		}.get(row['series'])
		if series_field not in row:
			raise ValueError(f'Missing series field {series_field!r}: {row}')
		code, os = row['geo_id'], row['os']
		key = (row['geo_type'], code, os, row['series'], row['date'], row['version'], row.get('cohort'))
		if key in keys:
			raise ValueError(f'Duplicate OS share key: {key}')
		keys.add(key)
		if row['geo_type'] == 'country' and code not in ISO_CODES:
			raise ValueError(f'Invalid ISO 3166-1 alpha-2 code: {code}')
		if os not in OS_LABELS or not 0 <= row['value'] <= 100 or row['confidence'] != 'measured':
			raise ValueError(f'Invalid OS share row: {row}')
		if (row['geo_type'], row['series'], row['date']) == ('country', 'statcounter_mobile', month):
			totals.setdefault((code, os), []).append(row)
	if set(totals) != {(code, os) for os, codes in covered.items() for code in codes}:
		raise ValueError('Country series do not match the successfully parsed exports')
	flags = []
	for (code, os), group in sorted(totals.items()):
		total = round(sum(row['value'] for row in group), 8)
		if abs(total - 100) > 2:
			flags.append(
				{
					'geo_id': code,
					'geo_name': group[0]['geo_name'],
					'os': os,
					'value': total,
					'unit': UNIT,
					'date': month,
					'source_url': group[0]['source_url'],
					'confidence': 'measured',
					'note': 'Published version shares differ from 100% by more than two percentage points.',
				}
			)
	return flags


def figure(value, unit, date, source_url, confidence='measured'):
	return dict(value=value, unit=unit, date=date, source_url=source_url, confidence=confidence)


def estimate_phones(rows, bases, month, offline):
	base_by_code = {base['geo_id']: base for base in bases}
	if len(base_by_code) != len(bases):
		raise ValueError('Duplicate smartphone base country')
	for code, base in base_by_code.items():
		if (
			code not in ISO_CODES
			or base['value'] <= 0
			or not base['unit']
			or not base['date']
			or not base['source_url'].startswith('https://')
			or base['confidence'] not in {'measured', 'vendor-claim', 'estimate'}
		):
			raise ValueError(f'Invalid smartphone base: {base}')
	platform_shares = {}
	for geo_id in sorted(base_by_code):
		url = chart_url('os', geo_id, month)
		path = CACHE / month / f'{geo_id}-platform.csv'
		shares = fetch(url, path, lambda body: parse_csv(body, 'OS', month), offline)
		platform_shares[geo_id] = {
			os: figure(shares[label], 'percent of sampled mobile web page views', month, url)
			for os, label in (('ios', 'iOS'), ('android', 'Android'))
			if label in shares
		}

	estimates = []
	for row in rows:
		code, os = row['geo_id'], row['os']
		if (
			row['geo_type'] != 'country'
			or code not in base_by_code
			or row['date'] != month
			or row['series'] != 'statcounter_mobile'
			or row['major_version'] is None
		):
			continue
		platform = platform_shares[code].get(os)
		if platform is None:
			continue
		base = base_by_code[code]
		value = round(base['value'] * (platform['value'] / 100) * (row['value'] / 100))
		share_ref = {key: row[key] for key in ('geo_type', 'geo_id', 'os', 'series', 'version', 'date')}
		estimates.append(
			{
				'geo_id': code,
				'geo_name': row['geo_name'],
				'os': os,
				'version': row['version'],
				'estimated_phones': value,
				**figure(value, base['unit'], month, row['source_url'], 'estimate'),
				'inputs': {
					'smartphone_base': base,
					'platform_share': platform,
					'version_share_row': share_ref,
				},
				'formula': 'round(smartphone base × (platform share / 100) × (within-platform version share / 100))',
			}
		)
	return estimates


def updated_json(original, updates):
	for key, value in updates.items():
		encoded = json.dumps(value, ensure_ascii=False, allow_nan=False, indent='\t').replace('\n', '\n\t')
		if isinstance(value, list) and value:
			lines = ',\n'.join(f'\t\t{json.dumps(row, ensure_ascii=False, allow_nan=False)}' for row in value)
			encoded = f'[\n{lines}\n\t]'
		match = re.search(rf'(?m)^\t"{re.escape(key)}": ', original)
		if match is None:
			body = original.rstrip().removesuffix('}').rstrip()
			original = f'{body},\n\t"{key}": {encoded}\n}}\n'
			continue
		start = match.end()
		_, length = json.JSONDecoder().raw_decode(original[start:])
		original = original[:start] + encoded + original[start + length :]
	return original


def refresh(args, exports):
	original = DATASET.read_text()
	data = json.loads(original)
	rows, covered, gaps = country_rows(data['os_share'], exports, args.month)
	flags = validate_shares(rows, covered, args.month)
	bases = data.get('smartphone_bases', [])
	estimates = estimate_phones(rows, bases, args.month, args.offline)
	coverage = {
		'date': args.month,
		'iso_geographies': figure(
			len(ISO_CODES), 'ISO 3166-1 countries and territories', args.month, SELECTOR_URL
		),
		'countries_with_ios_version_data': figure(
			len(covered['ios']),
			'ISO geographies',
			args.month,
			SELECTOR_URL,
		),
		'countries_with_android_version_data': figure(
			len(covered['android']),
			'ISO geographies',
			args.month,
			f'{SITE}/android-version-market-share/mobile/worldwide',
		),
		'smartphone_base_note': 'Only geographies listed in smartphone_bases have a verified base.',
		'countries_with_smartphone_base': figure(
			len({base['geo_id'] for base in bases}),
			'ISO geographies',
			args.month,
			'devices-by-region.json#/smartphone_bases',
		),
		'statcounter_gaps': gaps,
		'version_share_sum_flags': flags,
	}
	updates = {'os_share': rows, 'estimated_phones_by_version': estimates, 'coverage': coverage}
	result = updated_json(original, updates)
	parsed = json.loads(result)
	if parsed != data | updates:
		raise ValueError('Generated JSON differs from the expected dataset')
	if args.check and result != original:
		raise ValueError('Dataset differs from refreshed exports and estimates')
	if not args.check and result != original:
		with NamedTemporaryFile(mode='w', encoding='utf-8', dir=DATASET.parent, delete=False) as file:
			file.write(result)
		Path(file.name).replace(DATASET)
	print(f'iOS {len(covered["ios"])}, Android {len(covered["android"])}, smartphone bases {len(bases)}')
	print(
		f'{len(rows)} OS share rows, {len(gaps)} export gaps, {len(flags)} share sum flags, {len(estimates)} estimates'
	)


def main():
	latest_complete_month = (date.today().replace(day=1) - timedelta(days=1)).isoformat()[:7]
	parser = argparse.ArgumentParser(description='Refresh StatCounter country version shares.')
	parser.add_argument('--month', default=latest_complete_month, help='Complete calendar month, YYYY-MM')
	parser.add_argument('--offline', action='store_true', help='Read cached exports only')
	parser.add_argument('--check', action='store_true', help='Verify the dataset against the exports')
	args = parser.parse_args()
	if not re.fullmatch(r'\d{4}-(0[1-9]|1[0-2])', args.month) or args.month > latest_complete_month:
		parser.error('--month must be a complete calendar month in YYYY-MM format')
	exports = list(country_exports(args.month, args.offline))
	refresh(args, exports)


if __name__ == '__main__':
	main()
