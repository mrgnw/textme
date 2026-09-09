#!/bin/sh
# Compiles the deck's CSS from the project's Tailwind config and app.css so
# the mockup uses the same utilities, tokens and preflight as the app.
cd "$(dirname "$0")/.."
pnpm exec tailwindcss -c tailwind.config.ts -i src/app.css -o mockups/card.css --content mockups/card.html --minify
