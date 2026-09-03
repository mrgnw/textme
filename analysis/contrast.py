# /// script
# requires-python = ">=3.12"
# ///
import colorsys


def hsl_to_hex(h, s, l):
	r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
	return '#%02X%02X%02X' % (round(r * 255), round(g * 255), round(b * 255))


def luminance(hex_color):
	rgb = [int(hex_color[i : i + 2], 16) / 255 for i in (1, 3, 5)]
	lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
	return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(a, b):
	la, lb = luminance(a), luminance(b)
	hi, lo = max(la, lb), min(la, lb)
	return (hi + 0.05) / (lo + 0.05)


WHITE = '#FFFFFF'
LIGHT_BG = hsl_to_hex(216, 25, 95)
LIGHT_FG = hsl_to_hex(215, 25, 11)
DARK_BG = hsl_to_hex(220, 20, 8)
DARK_CARD = hsl_to_hex(220, 18, 12)
DARK_FG = hsl_to_hex(210, 20, 96)

pairs = [
	('light fg on card', LIGHT_FG, WHITE),
	('light fg on bg', LIGHT_FG, LIGHT_BG),
	('muted shadcn 215 16 47 on card', hsl_to_hex(215, 16, 47), WHITE),
	('muted 215 16 40 on card', hsl_to_hex(215, 16, 40), WHITE),
	('muted 215 19 35 on card', hsl_to_hex(215, 19, 35), WHITE),
	('muted 215 19 35 on bg', hsl_to_hex(215, 19, 35), LIGHT_BG),
	('primary 240 58 60 + white', hsl_to_hex(240, 58, 60), WHITE),
	('primary 240 55 55 + white', hsl_to_hex(240, 55, 55), WHITE),
	('primary 240 52 52 + white', hsl_to_hex(240, 52, 52), WHITE),
	('telegram #1A84C7 + white', '#1A84C7', WHITE),
	('telegram #1673B1 + white', '#1673B1', WHITE),
	('telegram #0D6AA8 + white', '#0D6AA8', WHITE),
	('whatsapp #128C7E + white', '#128C7E', WHITE),
	('whatsapp #0F7A6E + white', '#0F7A6E', WHITE),
	('whatsapp #0E6E63 + white', '#0E6E63', WHITE),
	('sms #22964F + white', '#22964F', WHITE),
	('sms #1C8A47 + white', '#1C8A47', WHITE),
	('sms #178040 + white', '#178040', WHITE),
	('dark fg on card', DARK_FG, DARK_CARD),
	('dark muted 215 15 66 on card', hsl_to_hex(215, 15, 66), DARK_CARD),
	('dark muted 215 15 70 on card', hsl_to_hex(215, 15, 70), DARK_CARD),
	('dark primary 240 70 74 + dark text', hsl_to_hex(240, 70, 74), hsl_to_hex(240, 30, 12)),
	('dark primary 240 70 74 on card', hsl_to_hex(240, 70, 74), DARK_CARD),
	('dark border 220 14 20 on card', hsl_to_hex(220, 14, 20), DARK_CARD),
	('light border 214 20 88 on card', hsl_to_hex(214, 20, 88), WHITE),
	('destructive 0 72 51 on card', hsl_to_hex(0, 72, 51), WHITE),
	('destructive 0 65 45 on card', hsl_to_hex(0, 65, 45), WHITE),
]

for name, a, b in pairs:
	r = ratio(a, b)
	mark = 'AAA' if r >= 7 else 'AA' if r >= 4.5 else 'AA-large' if r >= 3 else 'FAIL'
	print(f'{r:5.2f}  {mark:8}  {name}  ({a} on {b})')
