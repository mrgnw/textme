---
branch: design/copy-links
---

# Copy a direct link, not just open it

Users sometimes want the t.me / wa.me / sms: URL itself to send to someone, not to open it.

Options mocked at https://mox.xcc.es/textme/copylinks.html (source `mockups/copylinks.html`, stills in `mockups/stills/copylinks/`):

- A split pill: trailing copy segment inside each brand pill. Recommended.
- B copy icon beside each pill
- C Open / Copy link mode toggle
- D URL rows under the pills
- E direct-link rows inside the Share sheet
- F long-press / right-click menu on a pill
- G copy + QR, two segments per pill. Label goes off-centre on the phone.
- H one segment per pill, QR / Copy toggle under the pills sets what it does; footer QR folds in. Tapping QR flips the card to its back with a tab per app.

Where the QR shows once an H segment is tapped, without losing the card:

- I inline: a panel opens under the tapped pill, segment becomes the close. Card grows 140 px.
- J popover: 256 px popover off the segment, nothing moves; covers the SMS pill and toggle.
- K pill grows: the pill stretches into a brand-coloured block with the QR inside.
- L sheet on phone (number stays above the scrim), side card on desktop.
- M pills swap: number and footer stay, the pill zone becomes a tabbed QR block.

Pick (2026-09-09): H for the pills, L for showing the code. One segment per pill, QR / Copy toggle below, footer QR dropped. Tapping a QR segment opens a bottom sheet on the phone and a side card on desktop, tabs Telegram / WhatsApp / SMS / textme preselected to the tapped app.

Implementation notes for A:

- `ActionButtons.svelte`: wrap each pill in a flex container, `<a>` body + `<button>` segment, 56px wide, `aria-label="Copy Telegram link"`.
- Feedback: segment icon flips to a check for ~1.5 s, toast reads `Copied t.me/+34612345678` (extend `copyToClipboard` to take a label).
- Pills stay `<a href>`, so native right-click / long-press copy keeps working.
- `ContactRow.svelte` list rows keep native copy only; a per-row menu is a later step.
