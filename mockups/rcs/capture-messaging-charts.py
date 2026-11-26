# /// script
# requires-python = '>=3.14'
# dependencies = ['playwright']
# ///
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
CAPTURES = HERE.parents[1] / 'captures'
CHARTS = sys.argv[1:] or ['app-patchwork', 'global-app-reach', 'ios-android-split']
WIDTHS = {'mobile': 390, 'desktop': 1280}

CAPTURES.mkdir(exist_ok=True)
problems = 0
with sync_playwright() as p:
	browser = p.chromium.launch(channel='chrome')
	for scheme in ('light', 'dark'):
		for label, width in WIDTHS.items():
			page = browser.new_page(viewport={'width': width, 'height': 900}, color_scheme=scheme)
			for chart in CHARTS:
				page.goto((HERE / f'{chart}.html').as_uri())
				wide = page.evaluate(
					"""() => [...document.querySelectorAll('main *')]
						.filter((el) => !el.closest('.table-wrap') && el.getBoundingClientRect().right > innerWidth + 1)
						.map((el) => el.tagName + '.' + el.className)
						.slice(0, 5)"""
				)
				if wide:
					problems += 1
					print(f'overflow {chart} {label}: {wide}')
				out = CAPTURES / f'{chart}-{label}-{scheme}.png'
				page.screenshot(path=out, full_page=True)
				print(out.name)
			page.close()
	browser.close()
sys.exit(1 if problems else 0)
