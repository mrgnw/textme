# textme

Type a phone number, get one-tap links to message it — Telegram, WhatsApp, or SMS — plus a downloadable contact card and a QR code. Live at [textme.cc](https://textme.cc).

> [!NOTE]
> This project was built with heavy LLM assistance and should be considered proof-of-concept. Contributions are welcome, but I can't guarantee the accuracy of the code or that I will continue to maintain it. If there are any mistakes in attribution or anything else, please let me know.

## Features

- One input → direct-message links: Telegram (`t.me`), WhatsApp (`wa.me`), and SMS (`sms:`)
- Download a contact card (`.vcf`) with WhatsApp and Telegram profiles attached
- QR code for the Telegram link
- Phone validation via [svelte-tel-input](https://github.com/gyurielf/svelte-tel-input), with your country auto-detected from Cloudflare's `cf-ipcountry` header
- Bulk mode at [textme.cc/bulk](https://textme.cc/bulk) — paste `Name number` lines and get a row of links per contact

## Deep links

Any path is treated as a phone number and prefills the form:

```
https://textme.cc/+15551234567
```

Number words work too, in English and Spanish (`five` and `cinco` → `5`), as do circled digits (`①`, `❶`).

## API

```sh
curl https://textme.cc/api/links/+15551234567
```

Returns `{ "phone": ..., "links": { "telegram", "whatsapp", "sms" } }`. The `/api/telegram/{phone}`, `/api/whatsapp/{phone}`, and `/api/sms/{phone}` routes 302-redirect straight to the deep link.

## Develop

Needs Node 20 and [pnpm](https://pnpm.io).

```sh
pnpm install
pnpm dev
```

## Build & test

```sh
pnpm build
pnpm preview
pnpm check
pnpm test:e2e
```

Deploys to Cloudflare Pages via `@sveltejs/adapter-cloudflare` (see `wrangler.toml`).

## Stack

Svelte 5 + SvelteKit 2, TypeScript, TailwindCSS, bits-ui, svelte-tel-input, deployed on Cloudflare Pages.
