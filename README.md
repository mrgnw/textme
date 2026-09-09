# textme

[textme.cc](https://textme.cc) turns a phone number into direct-message links. Paste or type a number and get one-tap buttons for Telegram, WhatsApp and SMS, a vCard download, a QR code, and a shareable link (`textme.cc/34612345678`, or `textme.cc/34612345678/Maria` for a named contact card). Paste a whole list of names and numbers and it becomes a contact list with a single `.vcf` export.

Phone numbers are parsed, validated and formatted by [svelte-tel-input](https://github.com/gyurielf/svelte-tel-input) and [libphonenumber-js](https://gitlab.com/catamphetamine/libphonenumber-js). The UI is SvelteKit with [shadcn-svelte](https://shadcn-svelte.com) components on Tailwind, deployed to Cloudflare Workers.

```sh
pnpm install
pnpm dev
```

```sh
pnpm check
pnpm test
pnpm test:e2e
```

Design mockups live in `mockups/` and are served at [mox.xcc.es/textme](https://mox.xcc.es/textme/) (card.html for the Card redesign, copylinks.html for the copy-link options); `node mockups/capture-app.mjs` screenshots every state of a running preview into `mockups/stills/app/`.

This project is developed with the help of LLM coding agents.
