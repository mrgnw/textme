# /// script
# requires-python = ">=3.12"
# dependencies = ["playwright"]
# ///
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = 'http://localhost:5912/_mox/textme'
OUT = Path(__file__).parent / '../../captures'
WIDTHS = (390, 1280)
SCHEMES = ('light', 'dark')


def main(names: list[str]) -> None:
	OUT.mkdir(exist_ok=True)
	with sync_playwright() as p:
		browser = p.chromium.launch(channel='chrome')
		for name in names:
			for width in WIDTHS:
				for scheme in SCHEMES:
					page = browser.new_page(viewport={'width': width, 'height': 900}, color_scheme=scheme)
					page.goto(f'{BASE}/{name}/')
					overflow = page.evaluate('document.documentElement.scrollWidth - window.innerWidth')
					path = OUT / f'rcs-{name}-{width}-{scheme}.png'
					page.screenshot(path=path, full_page=True)
					page.screenshot(path=path.with_name(path.stem + '-top.png'))
					print(f'{path.name} overflow={overflow}px')
					page.close()
		browser.close()


if __name__ == '__main__':
	main(sys.argv[1:])
