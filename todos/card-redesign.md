# Card redesign — implementation plan

Source of truth for the look: `mockups/card.html` and `mockups/stills/card/`. Every state, token and class recipe in the deck is what the app should produce. This plan turns it into SvelteKit code while reusing the frameworks already in the repo. Hand-written phone parsing, hand-rolled dialogs, and ad-hoc spacing are out.

## Frameworks and the exact APIs to use

| Concern | Use | Notes |
|-|-|-|
| Phone input, as-you-type formatting, country | `svelte-tel-input` 4.3 `TelInput` (`bind:country`, `bind:valid`, `bind:detailedValue`, `onValueChange`, `options.validateOn: 'blur'`) | `validateOn: 'blur'` gives the deck's "no red while typing" for free |
| Parse / normalize outside the input | `svelte-tel-input/utils`: `parse(raw, country)` → `DetailedValue` (`isValid`, `e164`, `formatInternational`, `formatNational`, `nationalNumber`, `countryCode`, `validationError`), `normalizeToE164` | already used in `PhoneLinksCard.resolveInitial` |
| Incomplete vs invalid, finding numbers in text | `libphonenumber-js` 1.13: `validatePhoneNumberLength(text, country)` → `'TOO_SHORT' \| 'TOO_LONG' \| 'INVALID_COUNTRY' \| 'NOT_A_NUMBER' \| undefined`; `findPhoneNumbersInText(text, country)` → `{ number, startsAt, endsAt }[]` | transitive today; must be added to package.json (pnpm strict) |
| Words → digits prepass | existing `replaceDigitWords` in `src/lib/normalize.js` | keep |
| UI primitives | shadcn-svelte 1.6 on bits-ui 2.18: `button`, `dialog`, `popover`, `tabs`, `textarea`, `label` added via the CLI; existing `card`, `input`, `badge`, `sheet` | CLI keeps Tailwind v3 output when `components.json` is v3 (it is) |
| Textarea autosize, persisted recents, debounce | `runed` 0.37: `TextareaAutosize`, `PersistedState`, `useDebounce` | |
| QR | `uqr` 0.1 `renderSVG(text)` → inline SVG string | replaces api.qrserver.com; no canvas, works on Workers |
| Dark mode | `mode-watcher` 1.1 `<ModeWatcher />` | sets the `dark` class from `prefers-color-scheme`; no toggle UI |
| Display font | `@fontsource-variable/bricolage-grotesque` | import once in `+layout.svelte` |
| Toasts | existing `svelte-sonner` | |
| Icons | existing `lucide-svelte` + `~icons/ri/*` brand marks | optional last task: move to `@lucide/svelte` |

## Behaviors that must survive (from the current app)

cf-ipcountry default country; flag button opens the country picker (Sheet on phone, Combobox on desktop); words-to-digits on paste and in `/[slug]`; Telegram / WhatsApp / SMS links; copy E.164; vCard with optional name (`generateVCard` in `src/lib/utils.ts`); Telegram QR; URL updates to `/DIGITS` while typing (debounced `goto` with `replaceState`); `/bulk` list parsing with names; `/api/*` routes unchanged; e2e tests in `tests/paste.spec.ts` (updated deliberately where behavior changes).

Deliberate behavior changes: WhatsApp links become `https://wa.me/<digits>` without `+` everywhere (today the card uses `+`, `/api` and bulk strip it; wa.me documents the digits form). The konami debug panel is dropped. `api.qrserver.com` is dropped.

## Tasks

Each task ends with a passing `pnpm check` and `pnpm build`, then one commit, then push (branch `design/identity-mockups` or a new `feat/card-redesign` off main once the mockup branch is merged).

### 1. Dependencies and shadcn components

Files: `package.json`, `pnpm-lock.yaml`, `src/lib/components/ui/{button,dialog,popover,tabs,textarea,label}/`

```sh
pnpm add libphonenumber-js@^1.13.7 runed uqr mode-watcher @fontsource-variable/bricolage-grotesque
pnpm dlx shadcn-svelte@latest add button dialog popover tabs textarea label
```

If the CLI emits Tailwind v4 syntax (`@theme`, `tw-animate-css`) despite `components.json`, copy the v3 recipes by hand using `src/lib/components/ui/card/card.svelte` as the pattern (tailwind-variants + `cn`).

Verify: files exist, `pnpm check` clean, `pnpm build` passes. Commit: `Add card redesign dependencies and shadcn components`.

### 2. Theme tokens, font, dark mode

Files: `src/app.css`, `tailwind.config.ts`, `src/routes/+layout.svelte`

- Replace the `:root` and `.dark` blocks in `src/app.css` with the deck's tokens verbatim (`mockups/card.html` `<style>`: background, foreground, card, popover, muted, muted-foreground, accent, secondary, border, input, primary, primary-foreground, destructive, ring, radius 0.75rem, telegram, whatsapp, sms, brand-foreground; both themes).
- `tailwind.config.ts`: add `fontFamily.display: ['Bricolage Grotesque Variable', ...defaultTheme.fontFamily.sans]` and colors `telegram`, `whatsapp`, `sms`, `'brand-foreground'` as `hsl(var(--…))` so the app uses `bg-telegram text-brand-foreground`, not arbitrary values.
- `+layout.svelte`: `import '@fontsource-variable/bricolage-grotesque'`, render `<ModeWatcher />` next to the Toaster.

Verify: build; open `/` and confirm the slate ground, indigo wordmark accent, and that `prefers-color-scheme: dark` flips tokens (Playwright `colorScheme: 'dark'`). Commit: `Apply Card theme tokens, display font, and system dark mode`.

### 3. Phone model module (pure functions, no UI)

Files: `src/lib/phone.ts` (new), delete `src/lib/bulkParse.ts`

- `classify(raw, country)` → `'empty' | 'incomplete' | 'invalid' | 'valid'` plus the `DetailedValue`: empty when no digits; valid when `parse(raw, country).isValid`; incomplete when `validatePhoneNumberLength(raw, country) === 'TOO_SHORT'`; otherwise invalid. Assert `country` is a 2-letter code.
- `links(e164)` → `{ telegram: https://t.me/${e164}, whatsapp: https://wa.me/${digits}, sms: sms:${e164} }`. Single source for the card, list rows and (later) `/api/links`.
- `shareUrl(origin, e164, name?)` → `${origin}/${digits}` + `/${encodeURIComponent(name)}` when a name is given.
- `findContacts(text, country)` → per line: skip blank lines and lines matching `/:\s*$/`; `findPhoneNumbersInText(line, country)`; take the first match; `name` = the line with the match span removed, trimmed of `[-:,\s]`; `inferred` = the matched text has no leading `+` or `00` (country came from the default). Bounded: stop after 200 lines. Returns `{ name, e164, formatInternational, inferred, key: e164 }[]` and a count of inferred numbers.
- `isListPaste(text, country)` → `findContacts(text, country).length >= 2`.

Verify: `pnpm check`; a `src/lib/phone.test.js` run with `node --test` (the repo already has `normalize.test.js` in that style) covering: Spanish mobile typed digit by digit (incomplete → valid), 8-digit invalid, `+1 202 456 1111` with ES default, the 8-line paste fixture from the deck (6 contacts, Pablo inferred, "Friends:" skipped). Commit: `Add phone model built on svelte-tel-input and libphonenumber-js`.

### 4. Recents store

Files: `src/lib/recent.svelte.ts` (new)

`PersistedState<{ e164: string; name: string; at: number }[]>('textme:recent', [])` from runed; `remember(e164, name)` moves to front and caps at 5; `forget(e164)`. Client-only by construction (runed guards SSR).

Verify: `pnpm check`. Commit: `Add persisted recent numbers`.

### 5. Number card, single mode, feature parity

Files: `src/components/NumberCard.svelte` (new), `src/components/ActionButtons.svelte` (new), `src/components/PhoneLinksCard.svelte` (rewrite), `src/components/CountrySelector.svelte` + `CountrySheet.svelte` + `CountryCombobox.svelte` (restyle to tokens and shadcn classes only), delete `src/components/ActionBar.svelte`, `ActionButton.svelte`, `ContactDownload.svelte`, `PhoneDebug.svelte`, `PhoneInput.svelte`

- `NumberCard`: `Card` > kicker row (`Phone number` / `Shared number` / `Pasted list` prop) + country stamp (`Button variant="outline" size="sm"` rounded-full with flag, `+CC`, chevron; opens `CountrySelector`); `TelInput` styled as the display line (`class="font-display text-4xl font-bold tracking-tight tabular-nums bg-transparent …"`, `initialFormat="national"`, `options.validateOn = 'blur'`, `bind:country`, `bind:detailedValue`, `onpaste` keeps the `replaceDigitWords` insertion and additionally calls `onListPaste(text)` when `isListPaste`); intl line (`detailedValue.formatInternational` + copy ghost icon button) only when valid; invalid line (`text-destructive`) only when `classify` says invalid and the input has blurred.
- `ActionButtons`: three `<a>` with `Button` classes (`size="lg"`, `rounded-full w-full bg-telegram text-brand-foreground` etc.) from `links(e164)`; when not valid: `aria-disabled="true"`, `tabindex="-1"`, `pointer-events-none opacity-50`, `href="#"`. Accessible names stay `Telegram`, `WhatsApp`, `SMS`.
- `PhoneLinksCard`: owns `value`, `country` (from `$page.data.ip_country`), `detailedValue`; derives `state = classify(value, country)`; URL sync moves out of `$effect` into the `onValueChange` handler using runed `useDebounce(() => goto('/' + digits, { replaceState: true, noScroll: true }), 500)` guarded by `state === 'valid'` and `value !== initialValue`; `remember()` on the same path. Layout: header wordmark (`font-display`), `main` `mx-auto w-full max-w-md px-4 pt-1 pb-6 sm:px-6 sm:pt-8`.

Verify: `pnpm build && pnpm test:e2e` after updating `tests/paste.spec.ts` (see task 11 for the selector changes; do the minimal edits here: `.disabled` → `aria-disabled`, WhatsApp href without `+`). Compare `/34612345678` against `mockups/stills/card/light-valid.png`. Commit: `Rebuild the number card on the Card design`.

### 6. Paste button and recents UI

Files: `src/components/NumberCard.svelte`, `src/components/RecentNumbers.svelte` (new), `src/components/PhoneLinksCard.svelte`

- Empty state: `Button size="lg" class="w-full rounded-full"` "Paste number" → `navigator.clipboard.readText()`; on success run the same path as `onpaste` (words-to-digits, list detection); on rejection or missing API focus the input and toast "Press ⌘V / long-press to paste". Hide the button once the input has digits.
- Hint line under it (`text-sm text-muted-foreground`).
- `RecentNumbers`: kicker "Recent" + `Badge`-style chips (`rounded-full border bg-card`) with remove icon button; tap → `goto('/' + digits)`.

Verify: e2e with `page.context().grantPermissions(['clipboard-read'])` and `page.evaluate(() => navigator.clipboard.writeText(...))` then click Paste → buttons enabled; a second test stubs `readText` to reject and asserts the toast. Commit: `Add Paste button and recent numbers`.

### 7. Secondary actions: Save contact, Share link, QR

Files: `src/components/SecondaryActions.svelte` (new), `src/components/ShareDialog.svelte` (new), `src/components/QrPanel.svelte` (new), `src/components/NumberCard.svelte`

- Row of three `Button variant="ghost" size="sm"` under a `border-t pt-4` divider; the active one gets `bg-accent`.
- Save contact toggles an inline `rounded-lg bg-muted p-3` block: `Label` + `Input` (name) + `Button` "Save .vcf" → existing `downloadVCard(e164, name)`; then `remember(e164, name)`.
- Share link: on phone `Sheet side="bottom"`, on desktop `Dialog` (reuse the matchMedia choice already in `CountrySelector`; extract it to `src/lib/media.svelte.ts` if both need it). Content: sentence, `Input` name (optional), readonly `Input` with `shareUrl(...)` reacting to the name, `Button` Copy (existing `copyToClipboard`), `Button variant="outline"` "Share…" that calls `navigator.share({ url })` when available (hide otherwise).
- QR: the card swaps its body for `QrPanel`: `Tabs` (Telegram link / textme link), `{@html renderSVG(url)}` inside a `h-52 w-52 rounded-lg border bg-white p-3` box, caption, close icon button. No network.

Verify: e2e: open Share, type `Maria`, assert the readonly input shows `/34612345678/Maria`; open QR, assert an `<svg>` is rendered inside the card and no request to `api.qrserver.com` (route interception). Commit: `Add Save contact, Share link, and client-side QR`.

### 8. List mode

Files: `src/components/ListEditor.svelte` (new), `src/components/ContactRow.svelte` (new), delete `src/components/BulkRow.svelte`, `src/routes/bulk/+page.svelte` (thin), `src/components/PhoneLinksCard.svelte`, `src/lib/utils.ts`

- `PhoneLinksCard` gets `mode: 'single' | 'list'`; a paste that `isListPaste` switches to list with the pasted text; `/bulk` renders the card with `mode="list"`; Clear returns to single.
- `ListEditor`: top `Card` with kicker "Pasted list" + stamp; `Textarea` bound to the text with runed `new TextareaAutosize({ element: () => el, input: () => text })`; `contacts = $derived(findContacts(text, country))`; count row (`font-display text-lg font-semibold` count, muted "· N got +CC", ghost Clear); buttons `Download all .vcf` (primary, `generateVCards(contacts)` → one multi-entry `.vcf`, added to `src/lib/utils.ts` next to `generateVCard`) and `Copy all` (outline, E.164 per line).
- Second `Card divide-y` of `ContactRow`: name (click → `Input h-8` inline edit, Enter/blur commits into a `names` map keyed by `e164`), number line with the `+CC added` `Badge` when `inferred`, five ghost icon buttons (copy, Telegram, WhatsApp, SMS, Save contact) from `links(e164)`.
- Desktop: `max-w-xl` for list mode.

Verify: e2e: paste the 8-line fixture into the tel input → 6 rows, `Pablo` row shows the badge, `Download all .vcf` triggers a download whose text contains six `BEGIN:VCARD`; `/bulk` still renders the editor. Commit: `Turn a multi-number paste into the list editor`.

### 9. Named landing route

Files: `src/routes/[slug=phone]/+page.svelte` (rename from `[slug]`), `src/routes/[slug=phone]/[name]/+page.svelte` (new), `src/params/phone.ts` (new), `src/components/NumberCard.svelte`, `src/components/PhoneLinksCard.svelte`

- `src/params/phone.ts`: match `/^[\d\s+\-().]+$|^[a-z\-]+$/i`-style: digits and separators, or number words (so `/six-one-two…` still works) — keep it one regex, reject empty.
- `[name]` page passes `initialName` to the card; the card renders the landing header (avatar initial `bg-primary`, `font-display text-3xl` name, muted international number + copy) instead of the kicker/input, prefills Save contact with the name, shows the footer "Shared with textme · Make your own link" (link to `/`). Without a name (`/[slug=phone]`) the kicker reads "Shared number" and the footer appears; input stays editable.
- URL sync never writes the name (the share dialog is the only producer of named links).

Verify: e2e: `/34612345678/Maria` shows heading `Maria`, `Save Maria` button, WhatsApp href `https://wa.me/34612345678`; `/bulk/x` and `/api/x` return 404 (matcher). Commit: `Add the named contact-card landing`.

### 10. Cleanup

Files: delete anything unreferenced after tasks 5–9 (`ActionBar`, `ActionButton`, `ContactDownload`, `PhoneDebug`, `PhoneInput`, `BulkRow`, `bulkParse.ts`, unused `normalize()` if `normalize.test.js` is the only caller — keep `replaceDigitWords`), `src/routes/api/links/[phone]/+server.ts` (use `links()` so the JSON matches the UI), `README.md` (one paragraph: what the app does, `pnpm dev`, `pnpm test:e2e`).

Verify: `rg -n 'ActionBar|BulkRow|bulkParse|qrserver|PhoneDebug' src` returns nothing; build; e2e. Commit: `Remove superseded components and the external QR service`.

### 11. Tests

Files: `tests/paste.spec.ts`, `tests/card.spec.ts` (new), `playwright.config.ts`

- `paste.spec.ts`: selectors `input[type="tel"]` and `getByRole('link', { name: 'WhatsApp' })` stay; replace `toHaveClass(/disabled/)` with `toHaveAttribute('aria-disabled', 'true')` and the enabled check with `not.toHaveAttribute('aria-disabled')`; WhatsApp href `https://wa.me/12024561111`; keep the geo test (`cf-ipcountry: ES` → stamp shows `🇪🇸`).
- `card.spec.ts`: the checks listed in tasks 6–9 plus dark mode (`test.use({ colorScheme: 'dark' })` → `html.dark` present) and the invalid state (type 8 digits, blur → destructive message visible; while typing → not visible).
- `playwright.config.ts`: port 4319 is used by another project on this machine and `reuseExistingServer` would attach to it. Pick a port no other project uses and keep `strictPort`.

Verify: `pnpm test:e2e` green in CI mode (`CI=1` so the server is always rebuilt). Commit: `Cover the Card flows with e2e tests`.

### 12. Optional: icons package

Replace `lucide-svelte` with `@lucide/svelte` (same icon names, new import path). Only if it stays a mechanical find-and-replace. Commit: `Move to @lucide/svelte`.

## Risks

- shadcn-svelte CLI output on a Tailwind v3 repo: documented as supported; fallback is copying recipes.
- Styling `TelInput` as 36px display type: it is a normal `<input>`, so this is CSS only, but check caret and placeholder rendering on iOS Safari.
- `findPhoneNumbersInText` on a line with two numbers takes the first; document, do not special-case.
- WhatsApp `+` change alters existing hrefs; the api route already strips it, so the UI is catching up, not diverging.
- Removing the konami debug panel removes the only view of `cf_data`; `+layout.server.js` still returns it for a future debug route.
- The e2e server port collision is a pre-existing trap; fix it in task 11 before trusting green runs.

## Out of scope

PWA (branch `feat/2-add-pwa-support-installable-offline`), auth (`feat/4-add-auth-anahtar…`), Signal links, analytics, URL shortening, changing `/api/*` contracts.
