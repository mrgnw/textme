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

print('--- brand colors as used by the apps ---')
BRAND = [('telegram #2AABEE', '#2AABEE'), ('whatsapp #25D366', '#25D366'), ('sms (iOS Messages) #34C759', '#34C759')]
for name, hex_color in BRAND:
	for label, text in (('white text', WHITE), ('dark text', LIGHT_FG), ('icon on white card', WHITE)):
		r = ratio(hex_color, text)
		mark = 'AAA' if r >= 7 else 'AA' if r >= 4.5 else 'AA-large' if r >= 3 else 'FAIL'
		print(f'{r:5.2f}  {mark:8}  {name} + {label}')

print('--- per-app light/dark accents, text options ---')
DARK_INK = hsl_to_hex(220, 20, 8)
PAIRS = [
	('telegram light #0088FF', '#0088FF'), ('telegram dark #3E88F7', '#3E88F7'),
	('whatsapp light #008069', '#008069'), ('whatsapp light #1DAA61', '#1DAA61'), ('whatsapp dark #25D366', '#25D366'), ('whatsapp dark #21C063', '#21C063'),
	('purple light #AF52DE', '#AF52DE'), ('purple dark #BF5AF2', '#BF5AF2'),
]
for name, hex_color in PAIRS:
	w, d = ratio(hex_color, WHITE), ratio(hex_color, DARK_INK)
	print(f'{name}: white {w:4.2f}  dark {d:4.2f}')

print('--- jet.com purple candidates for SMS ---')
for name, hex_color in [
	('jet #8F44F2 (Pantone 2665 C)', '#8F44F2'), ('jet #7D43F3', '#7D43F3'),
	('dark tint hsl(266 90% 70%)', hsl_to_hex(266, 90, 70)), ('dark tint hsl(266 90% 74%)', hsl_to_hex(266, 90, 74)),
	('dark tint hsl(262 92% 72%)', hsl_to_hex(262, 92, 72)),
]:
	print(f'{name}: white {ratio(hex_color, WHITE):4.2f}  dark {ratio(hex_color, DARK_INK):4.2f}  on dark card {ratio(hex_color, DARK_CARD):4.2f}  ({hex_color})')
