# /// script
# requires-python = '>=3.14'
# dependencies = ['pycountry']
# ///
"""Writes src/lib/rcs/coverage.json from research/rcs/coverage-by-country.json, adding ISO numeric codes
so rows join the world-atlas map shapes."""

import json
from pathlib import Path

import pycountry

source = Path('research/rcs/coverage-by-country.json')
out = Path('src/lib/rcs/coverage.json')


def main():
	rows = json.loads(source.read_text())
	for row in rows:
		row['n'] = pycountry.countries.get(alpha_2=row['iso2']).numeric
	rows.sort(key=lambda r: r['name'])
	as_of = max(row[platform]['date'] for row in rows for platform in ('android', 'iphone'))
	out.write_text(
		json.dumps({'as_of': as_of, 'countries': rows}, ensure_ascii=False, separators=(',', ':')) + '\n'
	)
	print(len(rows), 'rows ->', out, out.stat().st_size, 'bytes')


main()
