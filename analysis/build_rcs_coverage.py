# /// script
# requires-python = '>=3.14'
# dependencies = ['pycountry']
# ///
"""Writes src/lib/rcs/coverage.json from research/rcs/coverage-by-country.json and devices-by-region.json.
Adds ISO numeric codes so rows join the world-atlas map shapes, and the minimum phone requirements.
Per-country OS versions are built separately by scripts/build-rcs-versions.ts."""

import json
from pathlib import Path

import pycountry

source = Path('research/rcs/coverage-by-country.json')
devices = Path('research/rcs/devices-by-region.json')
out = Path('src/lib/rcs/coverage.json')

REQUIREMENTS = ('ios_min', 'iphone_models', 'android_google_play_services_floor', 'android_google_messages_setup')
SOURCED = ('value', 'date', 'source_url', 'confidence')


def requirements(device_data: dict) -> dict[str, dict]:
	keep = ('value', 'requirement_text', 'note', 'date', 'source_url', 'confidence')
	found = {r['id']: {k: r.get(k) for k in keep} for r in device_data['requirements'] if r['id'] in REQUIREMENTS}
	ios_min = int(found['ios_min']['value'])
	release = next(r for r in device_data['ios_model_support']['major_releases'] if r['major_version'] == ios_min)
	found['iphone_excluded'] = {k: release[k] for k in ('major_version', 'excluded_models', 'date', 'source_url', 'confidence')}
	return found


def main():
	rows = json.loads(source.read_text())
	device_data = json.loads(devices.read_text())
	for row in rows:
		row['n'] = pycountry.countries.get(alpha_2=row['iso2']).numeric
	rows.sort(key=lambda r: r['name'])
	as_of = max(row[platform]['date'] for row in rows for platform in ('android', 'iphone'))
	out.write_text(
		json.dumps({'as_of': as_of, 'requirements': requirements(device_data), 'countries': rows}, ensure_ascii=False, separators=(',', ':')) + '\n'
	)
	print(len(rows), 'rows ->', out, out.stat().st_size, 'bytes')


main()
