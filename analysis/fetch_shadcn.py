# /// script
# requires-python = ">=3.12"
# ///
# Fetches shadcn-svelte (Tailwind v3 registry, "default" style) component files
# into src/lib/components/ui/<name>/ — the CLI cannot resolve this registry any more.
import json
import sys
import urllib.request
from pathlib import Path

REGISTRY = 'https://tw3.shadcn-svelte.com/registry/default'
UI_DIR = Path('src/lib/components/ui')
COMPONENTS = sys.argv[1:] or ['button', 'dialog', 'popover', 'tabs', 'textarea', 'label']

for name in COMPONENTS:
	req = urllib.request.Request(f'{REGISTRY}/{name}.json', headers={'User-Agent': 'curl/8'})
	with urllib.request.urlopen(req, timeout=30) as res:
		item = json.load(res)
	target = UI_DIR / name
	target.mkdir(parents=True, exist_ok=True)
	for f in item['files']:
		(target / f['name']).write_text(f['content'])
	deps = item.get('dependencies', []) + item.get('devDependencies', [])
	print(f'{name}: {len(item["files"])} files; deps {deps}; registryDeps {item.get("registryDependencies", [])}')
