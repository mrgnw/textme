# PWA support (installable + offline) — issue #2

Make textme an installable PWA that works offline. SvelteKit 2 + Svelte 5,
adapter-cloudflare. Core link-generation flow is already client-side.

**Approach (lazy, zero new deps):** native SvelteKit `src/service-worker.js`
+ `$service-worker`, a static `manifest.webmanifest`, coral-branded PNG icons
rendered with the already-installed Playwright chromium. No vite-plugin-pwa,
no workbox.

**Decisions (locked):**
- Manifest = static file `static/manifest.webmanifest` (served as
  `application/manifest+json`). No route.
- Service worker = native `src/service-worker.js`; SvelteKit auto-registers it
  in prod at scope `/`. No `svelte.config.js` change.
- Icons rendered via Playwright (`scripts/make-icons.mjs`), committed as PNGs.
  Overwrite the placeholder gray-Svelte `favicon.png` with real branding.
- Offline shell = runtime-cache `/` (root layout SSRs `cf-ipcountry`, so it is
  not prerenderable; cache the SSR'd copy at SW install + refresh on online nav).
- Brand coral `hsl(16 85% 60%)` = `#f07142`; light bg `#ffffff`.
- Same PNGs serve `purpose: any` and `maskable` (glyph inside safe zone).

## Tasks (TDD: red → implement → green → commit)

- [ ] **Task 1 — failing tests.** `tests/pwa.spec.ts`: manifest fields, icons
  served as PNG, head links (manifest/theme-color/apple-touch-icon), SW
  activates + precaches app shell. Verify all red. Commit.
- [ ] **Task 2 — icons.** `scripts/make-icons.mjs` renders a coral speech-bubble
  SVG to `static/icon-192.png`, `icon-512.png`, `apple-touch-icon.png` (180),
  and overwrites `favicon.png` (128). Run it; eyeball the 512. Icon test green.
  Commit script + PNGs.
- [ ] **Task 3 — manifest + head.** `static/manifest.webmanifest` +
  three `<link>/<meta>` lines in `src/app.html`. Tests 1–3 green. Commit.
- [ ] **Task 4 — service worker.** `src/service-worker.js`: versioned cache,
  precache `build`+`files`+`/`, cleanup on activate, cache-first for hashed
  assets, network-first with `/`-shell fallback for navigations, skip
  `/api/*` + cross-origin + non-GET. `playwright test` all green (paste.spec
  must stay green) + `pnpm check`. Commit.
- [ ] **Task 5 — offline proof + preview.** `scripts/verify-offline.mjs`
  (spawns preview, kills it, reloads, generates a link fully offline; group-kills
  the server so nothing is orphaned). Icon preview deck for the human. Run;
  commit; PR carries the Lighthouse-12 note.

## Verification
- `pnpm exec playwright test` — full suite green (5 old + 4 new).
- `pnpm check` — svelte-check clean (SW uses the documented triple-slash refs).
- `pnpm build && node scripts/verify-offline.mjs` → `OFFLINE OK: …/+12024561111`.
- Installability = manifest (name + 192/512 icons + display + start_url) + SW
  fetch handler + HTTPS in prod. Lighthouse 12 dropped the PWA category; these
  are the checks DevTools > Application > Manifest now enforces.

## Notes / risks
- First offline load requires one prior online visit (inherent to SWs).
- Offline deep-link `/{number}` serves the `/` shell (hydrates as `/`) —
  acceptable degradation, marked with a `ponytail:` comment.
- Icon is placeholder-quality branding; regenerate via `make-icons.mjs` after
  editing the SVG. Flagged for the human in the PR.
