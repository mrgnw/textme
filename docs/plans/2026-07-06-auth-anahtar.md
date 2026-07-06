# Auth via @mrgnw/anahtar (issue #4)

Email OTP + passkeys, session cookie, `requireUser` guard, minimal signed-in/out UI.
Reuses `@mrgnw/anahtar@0.0.29` as-is — no blocker; it drops in cleanly on Cloudflare D1.

## Decisions (locked)

1. **Local/test D1**: adapter-cloudflare 4.9's `emulate()` runs Wrangler `getPlatformProxy`
   in `vite dev` and `vite preview` (Playwright's webServer uses `pnpm build && pnpm preview`),
   reading `wrangler.toml`. A `[[d1_databases]]` binding with a **placeholder `database_id`**
   gives `platform.env.DB` locally; anahtar's `init()` auto-creates the `auth_*` tables on the
   first request. Human creates the real D1 before deploy (see Verification).
2. **OTP capture for e2e**: `onSendOTP` records `email→code` in a bounded in-module Map, only
   when `platform.env.OTP_TEST_HOOK === '1'`, exposed via `GET /api/dev/otp?email=` which 404s
   without the flag. The flag lives in a committed `.dev.vars` (local/preview only — wrangler
   never deploys that file). Never set the flag in Cloudflare.
3. **Passkey e2e**: register + re-login via Playwright CDP virtual authenticator
   (`ctap2`/`internal`, `automaticPresenceSimulation`). Fallback if flaky: `test.fixme` it and
   list passkey as manual QA — OTP + guard stay automated regardless.
4. **Guard + gated route**: `requireUser(event)` in `src/lib/server/guard.ts` (303 → `/login?next=`);
   demo gated route `/gated` whose `+page.server.ts` calls it. Reusable pattern for future gating.
5. **UI surface**: `AuthPill` island fixed top-right in the root layout (signed-in/out + sign-out,
   delegated to parent via `onSignOut`) + `/login` page with `AuthFlow` (guard redirect target,
   honors validated `?next=`). Both stock anahtar components. Visual preview: `/`, `/login`, `/gated`.
6. **Email (prod)**: `onSendOTP` logs to console without `RESEND_API_KEY`, else sends via Resend's
   REST API (plain fetch, no dep). Human picks provider + verified sender.

## Task 1 — platform plumbing (no behavior change; existing suite stays green)

- deps: `@mrgnw/anahtar`, `@simplewebauthn/browser`, dev `@cloudflare/workers-types` (done)
- `wrangler.toml`: add `compatibility_flags = ["nodejs_als","nodejs_compat"]` + `[[d1_databases]]` binding `DB`
- `.dev.vars` (committed, local-only): `OTP_TEST_HOOK=1`
- `.gitignore`: add `.wrangler` (local D1 state)
- `src/app.d.ts`: `App.Locals.user` + `App.Platform.env` (DB, OTP_TEST_HOOK?, RESEND_API_KEY?)
- Green: `pnpm check && pnpm test:e2e` (risk gate: getPlatformProxy accepts D1 binding + compat flags)

## Task 2 — email OTP round-trip (API-level, TDD)

- `tests/auth.spec.ts`: OTP round-trip via `/api/auth/start` → `/api/dev/otp` → `/api/auth/verify`
- `src/lib/server/auth.ts`: singleton `getAuth(env)`, OTP capture Map, Resend `onSendOTP`
- `src/hooks.server.ts`: `await getAuth(platform.env)` then `auth.handle`
- `src/routes/api/auth/[...path]/+server.ts`: mount `auth.handlers`
- `src/routes/api/dev/otp/+server.ts`: dev-only OTP read, 404 without flag

## Task 3 — requireUser guard + /gated route (TDD)

- tests: `/gated` redirects to `/login?next=%2Fgated` signed out; shows email signed in
- `src/lib/server/guard.ts`: `requireUser(event)` → 303 `/login?next=`
- `src/routes/gated/+page.server.ts` + `+page.svelte`

## Task 4 — /login page + AuthPill island + sign-out (TDD, visual)

- test: login via page, pill shows email, sign out returns to signed-out pill + guard blocks again
- `src/routes/login/+page.svelte`: `AuthFlow`, validated `?next=`
- `src/routes/+layout.server.js`: pass `user: locals.user`
- `src/routes/+layout.svelte`: `AuthPill` island top-right + `onSignOut` posts logout + invalidateAll

## Task 5 — passkey register + re-login (CDP virtual authenticator)

- test: OTP login → add passkey → sign out → sign back in with passkey → gated route accessible
- no implementation (anahtar serves the WebAuthn ceremonies); class selectors `.anahtar-passkey-add`/`-later`

## Verification

Automated: `pnpm check` (types) + `pnpm test:e2e` (paste suite + auth suite: OTP, guard redirect,
guard pass, UI login/sign-out, passkey register+re-login). Build runs via the Playwright webServer.

Manual / human before production:
1. `pnpm dlx wrangler d1 create textme-auth` → paste `database_id` into `wrangler.toml`.
2. If Pages deploys via dashboard git integration, set prod+preview: compat flags `nodejs_als`,
   `nodejs_compat`, and D1 binding `DB` → textme-auth. Do NOT set `OTP_TEST_HOOK` in Cloudflare.
3. Email: set `RESEND_API_KEY` + verified sender for `textme.cc` (from `auth@textme.cc` — adjust in
   `src/lib/server/auth.ts`). Without the key, prod OTP codes only go to worker logs.
4. Real-device passkey QA (Touch ID / iCloud Keychain) on the deployed HTTPS origin.

Risks (bounded): getPlatformProxy + `compatibility_date = "2026-01-20"` on wrangler 3.114 — gated by
Task 1 smoke run; contingency `wrangler@^4` devDep, never lower the prod compat date. If `.dev.vars`
isn't read in preview, fallback gate the dev-otp route on `url.hostname === 'localhost'`.
