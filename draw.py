#!/usr/bin/env python3
"""Draw the news-image-20261120 entry: one broadsheet front page that sums up
the world news of Friday 20 November 2026.

Layout follows the classic newspaper front-page formula: a serif masthead
naming the day, a one-line deck, a by-the-numbers strip, a colour region bar,
13 illustrated story panels (3 heroes, 5 medium, 5 small), a dotted world map
with numbered pins, a list of 22 further briefs and a DATE CHECK footer.
All artwork is drawn here with PIL primitives; all text is set in Liberation
fonts. The output is deterministic: same code, same bytes.

Run locally to (re)generate entry.png beside this file:
    python3 draw.py
The competition program itself is main.py, which only copies entry.png to
/output/entry.png using the standard library.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
CW = W - 2 * MARGIN  # content width = 976

CREAM = (247, 243, 233)
PAPER_LINE = (196, 188, 168)
INK = (20, 19, 17)
GREY = (92, 89, 80)
RED = (176, 28, 26)
NAVY = (15, 31, 63)
TEAL = (33, 104, 116)
SAND = (226, 205, 160)
ORANGE = (238, 122, 36)
GOLD = (198, 148, 38)
GREEN = (52, 116, 66)
PURPLE = (96, 62, 140)
BROWN = (140, 96, 52)

FD = "/usr/share/fonts/truetype/liberation/"
SERIF_B = FD + "LiberationSerif-Bold.ttf"
SERIF_BI = FD + "LiberationSerif-BoldItalic.ttf"
SANS = FD + "LiberationSans-Regular.ttf"
SANS_B = FD + "LiberationSans-Bold.ttf"

FONTS = {}


def font(path, size):
    key = (path, size)
    if key not in FONTS:
        FONTS[key] = ImageFont.truetype(path, size)
    return FONTS[key]


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)


def text_w(s, f):
    return d.textlength(s, font=f)


def wrap(s, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if text_w(trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(x, y, s, f, max_w, fill=INK, leading=1.18, max_lines=None):
    lines = wrap(s, f, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = int(f.size * leading)
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=f, fill=fill)
    return y + len(lines) * lh


def centered(y, s, f, fill=INK):
    d.text(((W - text_w(s, f)) / 2, y), s, font=f, fill=fill)


def kicker_tag(x, y, s, fill=RED):
    """White-on-red uppercase label, returns its width."""
    f = font(SANS_B, 13)
    w = int(text_w(s, f)) + 14
    d.rectangle([x, y, x + w, y + 20], fill=fill)
    d.text((x + 7, y + 3), s, font=f, fill=(255, 255, 255))
    return w


def panel_frame(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=PAPER_LINE, width=1)


def story_head(x, y, w, num, place, headline, body, source,
               head_size=20, body_size=13, head_lines=2, body_lines=3):
    """Red location line, serif headline, grey body, source credit."""
    f_loc = font(SANS_B, 12)
    d.text((x, y), f"{num}  {place}", font=f_loc, fill=RED)
    y2 = draw_text_block(x, y + 17, headline, font(SERIF_B, head_size), w,
                         fill=INK, leading=1.08, max_lines=head_lines)
    y3 = draw_text_block(x, y2 + 3, body, font(SANS, body_size), w,
                         fill=(52, 50, 46), leading=1.16, max_lines=body_lines)
    d.text((x, y3 + 2), source, font=font(SANS, 10), fill=GREY)
    return y3


# ---------------------------------------------------------------- masthead
f_kick = font(SANS_B, 14)
d.text((MARGIN, 16), "THE WORLD IN ONE DAY", font=f_kick, fill=RED)
right = "35 STORIES · 7 REGIONS · EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
d.text((W - MARGIN - text_w(right, f_kick), 16), right, font=f_kick, fill=INK)
d.line([MARGIN, 42, W - MARGIN, 42], fill=INK, width=3)

centered(48, "Friday 20 November 2026", font(SERIF_B, 62))
d.line([MARGIN, 120, W - MARGIN, 120], fill=INK, width=1)
centered(128, "Missiles hit Kyiv's bridges  ·  Cyclone Akvan strikes India  "
              "·  An AI sell-off sinks Asia  ·  A genocide ruling",
         font(SERIF_BI, 17.5), fill=(60, 30, 20))

# ---------------------------------------------------------------- numbers
NUMBERS = [
    ("3", "Dnipro bridges hit in the Kyiv barrage"),
    ("300,000+", "people moved to shelters before Akvan"),
    ("-4.8%", "Nikkei's fall on Friday in the AI sell-off"),
    ("9-6", "ICJ vote: Myanmar committed genocide"),
    ("$48.3bn", "US cost of the Iran war so far, Pentagon"),
    ("118", "runs by Glenn Phillips against India"),
]
ny, nh = 156, 62
cell_w = CW // 6
d.line([MARGIN, ny, W - MARGIN, ny], fill=INK, width=1)
for i, (big, small) in enumerate(NUMBERS):
    x = MARGIN + i * cell_w
    if i:
        d.line([x, ny + 6, x, ny + nh - 6], fill=PAPER_LINE, width=1)
    f_big = font(SERIF_B, 27)
    d.text((x + (cell_w - text_w(big, f_big)) / 2, ny + 3), big,
           font=f_big, fill=RED)
    draw_text_block(x + 8, ny + 36, small, font(SANS, 10), cell_w - 16,
                    fill=GREY, leading=1.1, max_lines=2)
d.line([MARGIN, ny + nh, W - MARGIN, ny + nh], fill=INK, width=1)

# ---------------------------------------------------------------- region bar
REGIONS = [
    ("EUROPE 8", 8, NAVY),
    ("ASIA 6", 6, RED),
    ("AMERICAS 7", 7, GREEN),
    ("MIDDLE EAST 4", 4, GOLD),
    ("AFRICA 4", 4, BROWN),
    ("OCEANIA 2", 2, TEAL),
    ("GLOBAL 4", 4, PURPLE),
]
ry, rh = ny + nh + 8, 22
x = MARGIN
total = sum(n for _, n, _ in REGIONS)
for label, n, col in REGIONS:
    wseg = int(CW * n / total)
    d.rectangle([x, ry, x + wseg - 2, ry + rh], fill=col)
    f_r = font(SANS_B, 10.5)
    d.text((x + (wseg - text_w(label, f_r)) / 2, ry + 5), label,
           font=f_r, fill=(255, 255, 255))
    x += wseg

# ---------------------------------------------------------------- hero art
def art_kyiv(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # stars
    for sx, sy in [(30, 14), (90, 30), (170, 10), (250, 26), (290, 8), (130, 44)]:
        d.point((x + sx, y + sy), fill=(220, 225, 240))
    # skyline silhouettes
    for bx, bw, bh in [(0, 46, 52), (52, 34, 70), (92, 52, 44), (150, 36, 78),
                       (192, 58, 50), (256, 40, 66)]:
        d.rectangle([x + bx, y + h - 26 - bh, x + bx + bw, y + h - 26],
                    fill=(8, 16, 36))
        for wy in range(y + h - 26 - bh + 8, y + h - 34, 12):
            d.point((x + bx + 8, wy), fill=GOLD)
            d.point((x + bx + 20, wy), fill=GOLD)
    # missile arcs
    for x0, x1 in [(10, 120), (70, 200), (180, 290)]:
        d.arc([x + x0, y + 2, x + x1 + 60, y + 92], start=200, end=330,
              fill=ORANGE, width=4)
        d.ellipse([x + x1 + 44, y + 62, x + x1 + 58, y + 76], fill=ORANGE)
    # river + bridge
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(24, 62, 110))
    d.line([x, y + h - 26, x + w, y + h - 26], fill=(240, 200, 90), width=3)
    for px in range(18, w, 44):
        d.line([x + px, y + h - 26, x + px, y + h - 12], fill=(240, 200, 90),
               width=2)
    # fires
    for fx in (66, 236):
        d.ellipse([x + fx, y + h - 44, x + fx + 16, y + h - 28], fill=RED)
        d.ellipse([x + fx + 4, y + h - 50, x + fx + 12, y + h - 36],
                  fill=ORANGE)


def art_cyclone(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 216, 222))
    # sea
    d.rectangle([x, y + h - 34, x + w, y + h], fill=TEAL)
    # coast landmass
    d.polygon([(x, y), (x + 120, y), (x + 96, y + 44), (x + 128, y + 84),
               (x + 84, y + h - 30), (x, y + h - 30)], fill=SAND)
    d.text((x + 12, y + 36), "INDIA", font=font(SANS_B, 12), fill=(90, 70, 30))
    d.text((x + 10, y + h - 26), "ODISHA", font=font(SANS_B, 11),
           fill=(255, 255, 255))
    # spiral cyclone
    cx, cy = x + 218, y + 56
    for r, a0 in [(44, 20), (34, 140), (24, 260), (14, 60)]:
        d.arc([cx - r, cy - r * 0.72, cx + r, cy + r * 0.72], start=a0,
              end=a0 + 250, fill=(255, 255, 255), width=5)
    d.ellipse([cx - 6, cy - 5, cx + 6, cy + 5], fill=RED)
    # palms
    for px in (150, 276):
        d.line([x + px, y + h - 30, x + px + 4, y + h - 58], fill=BROWN,
               width=3)
        for a in (-40, -10, 25, 55):
            import math
            ex = x + px + 4 + int(20 * math.cos(math.radians(a - 90)))
            ey = y + h - 58 + int(12 * math.sin(math.radians(a - 90)))
            d.line([x + px + 4, y + h - 58, ex, ey], fill=GREEN, width=2)
    # rain streaks
    for rx in range(150, w - 8, 26):
        d.line([x + rx, y + 84, x + rx - 6, y + 98], fill=(90, 140, 160),
               width=2)


def art_selloff(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 14, 16))
    # grid
    for gy in range(16, h - 20, 22):
        d.line([x + 8, y + gy, x + w - 8, y + gy], fill=(44, 44, 48), width=1)
    # falling line
    pts = [(10, 38), (58, 44), (104, 40), (148, 58), (196, 54), (238, 76),
           (282, 72), (306, 90)]
    d.line([(x + px, y + py) for px, py in pts], fill=RED, width=4)
    for px, py in pts:
        d.ellipse([x + px - 3, y + py - 3, x + px + 3, y + py + 3], fill=RED)
    d.polygon([(x + 306, y + 90), (x + 294, y + 88), (x + 302, y + 78)],
              fill=RED)
    f_i = font(SANS_B, 12)
    d.text((x + 158, y + 8), "TAIEX -6.2%", font=f_i, fill=(255, 120, 110))
    d.text((x + 244, y + 8), "SEOUL -5.2%", font=f_i, fill=(255, 120, 110))
    d.text((x + 12, y + h - 22), "SOFTBANK -16%", font=f_i,
           fill=(255, 255, 255))
    d.text((x + w - 108, y + h - 22), "NIKKEI -4.8%", font=f_i,
           fill=(255, 120, 110))


# ---------------------------------------------------------------- heroes
HY, HH = ry + rh + 12, 224
hero_w = (CW - 24) // 3
HEROES = [
    (art_kyiv, "MISSILE BARRAGE", "1  KYIV, UKRAINE · WAR",
     "Russia's mass strike hits Kyiv's Dnipro bridges",
     "100+ missiles and some 400 drones in one of the war's biggest "
     "barrages. Three Dnipro bridges hit, eight killed, and the Austrian "
     "and Dutch embassies damaged.", "(BBC · Reuters)"),
    (art_cyclone, "LANDFALL", "2  GOPALPUR, INDIA · WEATHER",
     "Cyclone Akvan comes ashore on the Odisha coast",
     "Landfall near Gopalpur at 70-80 km/h, gusting to 90. More than "
     "300,000 people were moved to shelters before the storm arrived.",
     "(IMD · BBC)"),
    (art_selloff, "AI SELL-OFF", "3  TOKYO - TAIPEI - SEOUL · MARKETS",
     "Asia's AI sell-off sinks markets across the region",
     "Doubts over AI valuations deepened: the Nikkei fell 4.8%, Taiwan's "
     "Taiex 6.2% and Seoul 5.2%, while SoftBank dropped more than 16%.",
     "(Reuters · CNBC)"),
]
for i, (art, tag, place, head, body, src) in enumerate(HEROES):
    x = MARGIN + i * (hero_w + 12)
    panel_frame(x, HY, hero_w, HH)
    art(x + 1, HY + 1, hero_w - 2, 100)
    kicker_tag(x + 8, HY + 8, tag)
    story_head(x + 10, HY + 110, hero_w - 20, "", place, head, body, src,
               head_size=19, body_size=12, head_lines=2, body_lines=4)


# ---------------------------------------------------------------- medium art
def icon_court(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    cx = x + w // 2
    d.polygon([(cx, y + 8), (cx - 52, y + 26), (cx + 52, y + 26)],
              fill=NAVY)
    for i in range(4):
        px = x + 22 + i * 34
        d.rectangle([px, y + 30, px + 12, y + h - 18], fill=(255, 255, 255),
                    outline=GREY)
    d.rectangle([x + 12, y + h - 16, x + w - 12, y + h - 8], fill=NAVY)


def icon_summit(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 224, 238))
    # skyline
    for bx, bw, bh in [(6, 26, 30), (38, 20, 44), (130, 24, 38), (158, 18, 28)]:
        d.rectangle([x + bx, y + h - 14 - bh, x + bx + bw, y + h - 14],
                    fill=(120, 150, 180))
    # table with three pennants
    d.rectangle([x + 40, y + h - 26, x + w - 40, y + h - 14], fill=BROWN)
    for i, col in enumerate([(60, 90, 200), (200, 40, 40), (230, 180, 40)]):
        px = x + 62 + i * 42
        d.line([px, y + h - 26, px, y + 16], fill=INK, width=2)
        d.polygon([(px, y + 16), (px + 22, y + 21), (px, y + 27)], fill=col)
    d.text((x + 44, y + 4), "US · CHINA · RUSSIA", font=font(SANS_B, 11),
           fill=NAVY)


def icon_cop(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 236, 224))
    cx, cy = x + w // 2 - 14, y + h // 2
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=TEAL, width=3)
    d.ellipse([cx - 10, cy - 26, cx + 10, cy + 26], outline=TEAL, width=2)
    d.line([cx - 26, cy, cx + 26, cy], fill=TEAL, width=2)
    # thermometer
    tx = x + w - 34
    d.rectangle([tx, y + 10, tx + 8, y + h - 22], outline=RED, width=2)
    d.rectangle([tx + 2, y + 20, tx + 6, y + h - 24], fill=RED)
    d.ellipse([tx - 3, y + h - 24, tx + 11, y + h - 10], fill=RED)
    d.text((x + 8, y + 6), "COP31", font=font(SANS_B, 13), fill=GREEN)


def icon_flags(x, y, w, h):
    # left half EU blue with star circle, right half UK-ish cross
    d.rectangle([x, y, x + w // 2, y + h], fill=(28, 52, 140))
    d.rectangle([x + w // 2, y, x + w, y + h], fill=(240, 240, 240))
    import math
    cx, cy = x + w // 4, y + h // 2
    for i in range(8):
        a = math.radians(i * 45)
        sx, sy = cx + int(20 * math.cos(a)), cy + int(20 * math.sin(a))
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD)
    ux = x + w // 2
    d.polygon([(ux, y), (ux + 26, y), (ux, y + 20)], fill=(30, 50, 140))
    d.polygon([(x + w, y + h), (x + w - 26, y + h), (x + w, y + h - 20)],
              fill=(30, 50, 140))
    d.rectangle([ux + (w // 2) // 2 - 6, y, ux + (w // 2) // 2 + 6, y + h],
                fill=RED)
    d.rectangle([ux, y + h // 2 - 6, x + w, y + h // 2 + 6], fill=RED)
    d.text((x + 8, y + h - 20), "EU", font=font(SANS_B, 12),
           fill=(255, 255, 255))
    d.text((x + w - 30, y + h - 20), "UK", font=font(SANS_B, 12), fill=NAVY)


def icon_tower(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 44, 66))
    # towers
    for bx, bw, bh in [(16, 26, 44), (52, 20, 34), (128, 24, 40),
                       (158, 16, 30)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                    fill=(24, 20, 34))
    d.polygon([(x + 88, y + 6), (x + 96, y + 6), (x + 100, y + h),
               (x + 84, y + h)], fill=(96, 88, 120))
    for wy in range(y + 16, y + h - 10, 12):
        d.point((x + 92, wy), fill=GOLD)
    # missile trail
    d.arc([x + 96, y + 2, x + w + 30, y + 60], start=90, end=190,
          fill=ORANGE, width=3)
    d.ellipse([x + 104, y + 34, x + 116, y + 46], fill=ORANGE)
    d.ellipse([x + 106, y + 38, x + 114, y + 44], fill=RED)


MEDIUM = [
    (icon_court, "4  THE HAGUE · JUSTICE",
     "Myanmar rejects World Court genocide ruling",
     "The ICJ found Myanmar responsible for genocide against the "
     "Rohingya, 9-6 - a first against a state. 1.3m remain displaced.",
     "(UN News · BBC)"),
    (icon_summit, "5  SHENZHEN · DIPLOMACY",
     "Europe rejects a 'new Yalta' after Shenzhen",
     "Merz warns the US, China and Russia cannot settle Europe's "
     "future without Europe, after the three leaders' declaration.",
     "(Reuters · Euronews)"),
    (icon_cop, "6  ANTALYA · CLIMATE",
     "COP31 draft drops fossil-fuel phase-out",
     "The final-day draft deletes any call to end fossil fuels and "
     "drops net-zero dates. Pacific nations demand it back.",
     "(Reuters · CBC)"),
    (icon_flags, "7  BRUSSELS · EUROPE",
     "UK and EU seal post-Brexit reset deal",
     "Burnham, Costa and von der Leyen agree youth mobility, eased "
     "food checks and linked carbon markets.", "(Guardian · Al Jazeera)"),
    (icon_tower, "8  RIYADH · CONFLICT",
     "Houthi missiles damage Riyadh finance tower",
     "Missiles hit the financial district, damaging the sovereign "
     "wealth fund's PIF tower. No injuries were reported.",
     "(Sky News · Reuters)"),
]
MY = HY + HH + 12
MH = 176
med_w = (CW - 40) // 5
for i, (icon, place, head, body, src) in enumerate(MEDIUM):
    x = MARGIN + i * (med_w + 10)
    panel_frame(x, MY, med_w, MH)
    icon(x + 1, MY + 1, med_w - 2, 52)
    story_head(x + 8, MY + 60, med_w - 16, "", place, head, body, src,
               head_size=14.5, body_size=10.5, head_lines=3, body_lines=5)

# ---------------------------------------------------------------- small row
SMALL = [
    ("9  MERCURY · SPACE", "BepiColombo reaches Mercury after 8 years",
     "The Europe-Japan probe enters orbit - only the second mission "
     "ever to do so.", "8 YRS"),
    ("10  TOKYO · ECONOMY", "Japan inflation hits year's high at 2.2%",
     "Core CPI of 2.2% in October keeps a Bank of Japan rate hike "
     "on track.", "2.2%"),
    ("11  HORMUZ · ENERGY", "Tanker hits mine as Hormuz attacks grow",
     "46 ships wait to transit; the Iran war enters month nine, its "
     "US cost put at $48.3bn.", "46"),
    ("12  SUDAN · CONFLICT", "Drone strike kills 10 at a gold mine",
     "Attack on the Bajoun site in South Kordofan; Amnesty urges a "
     "probe of strikes on civilians.", "10"),
    ("13  ROME · SOCIETY", "General strike halts Italy over living costs",
     "Workers and students join a nationwide strike over wages, "
     "prices and the budget.", "24H"),
]
SY = MY + MH + 12
SH = 122
for i, (place, head, body, big) in enumerate(SMALL):
    x = MARGIN + i * (med_w + 10)
    panel_frame(x, SY, med_w, SH)
    story_head(x + 8, SY + 8, med_w - 16, "", place, head, body, "",
               head_size=14.5, body_size=10.5, head_lines=3, body_lines=4)
    f_big = font(SERIF_B, 24)
    d.text((x + med_w - text_w(big, f_big) - 8, SY + SH - 34), big,
           font=f_big, fill=RED)

# ---------------------------------------------------------------- bottom
BY = SY + SH + 12
d.line([MARGIN, BY - 4, W - MARGIN, BY - 4], fill=INK, width=2)
f_also = font(SANS_B, 14)
d.text((MARGIN, BY + 2), "ALSO ON FRIDAY 20 NOVEMBER - 22 MORE STORIES",
       font=f_also, fill=INK)

BRIEFS = [
    "14 BERLIN - Allies say Europe ready to talk with Russia",
    "15 GAZA - Troops cross Yellow Line, first since truce",
    "16 HAITI - Raid on Martissant kills 34 gang suspects",
    "17 SENEGAL - Migrant boat capsizes; dozens missing",
    "18 EL SALVADOR - Bukele registers for a third term",
    "19 CALIFORNIA - Nvidia probed over AI chips to China",
    "20 WELLINGTON - Phillips smashes 118 against India",
    "21 LOS ANGELES - GTA VI day-one sales pass $2.3bn",
    "22 BARCELONA - Pill shrinks pancreatic tumours 60.7%",
    "23 BAGHDAD - Militia told to quit Jurf al-Sakhar",
    "24 COPENHAGEN - Greenland security deal ratified",
    "25 BEIJING - Lending rates held, 18th month in a row",
    "26 CARACAS - US signs military deal with Venezuela",
    "27 FIJI - Disaster declared as El Nino drought bites",
    "28 25+ COUNTRIES - Youth strike over living costs",
    "29 WASHINGTON - Measles cases near 5,838 in the US",
    "30 LUANDA - Angola pays $180m for 10% of De Beers",
    "31 DEEP SPACE - Voyager 1 now one light-day away",
    "32 NAIROBI - US group wins $60bn Mrima Hill deal",
    "33 WASHINGTON - Cyber director fired after outages",
    "34 WARSAW - Russian missile lands in Polish field",
    "35 DHAKA - Violence flares ahead of Hasina return",
]
brief_w = 640
col_w = (brief_w - 14) // 2
f_br = font(SANS, 11)
for i, b in enumerate(BRIEFS):
    col = 0 if i < 11 else 1
    row = i if i < 11 else i - 11
    x = MARGIN + col * (col_w + 14)
    y = BY + 26 + row * 12.5
    num, rest = b.split(" ", 1)
    d.text((x, y), num, font=font(SANS_B, 11), fill=RED)
    lines = wrap(rest, f_br, col_w - 24)
    d.text((x + 24, y), lines[0] if lines else "", font=f_br, fill=INK)

# dotted world map with pins for stories 1-13
MAP = [
    "     ### ##                                        ",
    "  ########## ##       ####  ##################     ",
    " ##############     ###########################    ",
    "  ######## ###       #######################       ",
    "   ######  ##         ##### #############  ##      ",
    "    ####               ###    ########             ",
    "    #####               ##      #####      ##      ",
    "     ####                        ###      ####     ",
    "     ###                         ##        ##      ",
    "      ##                                   ##      ",
    "      #                                                ",
]
mx = MARGIN + brief_w + 18
mw = W - MARGIN - mx
d.text((mx, BY + 2), "WHERE IT HAPPENED", font=f_also, fill=INK)
d.rectangle([mx, BY + 24, mx + mw, BY + 24 + 116], fill=(233, 230, 218))
cell = 5.6
for r, row in enumerate(MAP):
    for c, ch in enumerate(row):
        if ch == "#":
            cxp = mx + 8 + c * cell
            cyp = BY + 31 + r * 10.2
            d.ellipse([cxp, cyp, cxp + 3.4, cyp + 3.4], fill=(120, 116, 104))
# pins: (story, x fraction, y fraction); story 9 is at Mercury, not pinned
PINS = [(1, .52, .16), (2, .70, .44), (3, .84, .30), (4, .46, .14),
        (5, .79, .34), (6, .56, .28), (7, .44, .22), (8, .61, .38),
        (10, .88, .36), (11, .63, .34), (12, .56, .56),
        (13, .48, .26)]
for num, fx, fy in PINS:
    px = mx + 8 + fx * (mw - 30)
    py = BY + 30 + fy * 104
    d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED)
    f_p = font(SANS_B, 9)
    s = str(num)
    d.text((px - text_w(s, f_p) / 2, py - 5), s, font=f_p,
           fill=(255, 255, 255))
d.text((mx, BY + 144), "Pins: illustrated stories (9 is at Mercury).",
       font=font(SANS, 10.5), fill=GREY)

# ---------------------------------------------------------------- date check
DY = BY + 162
d.rectangle([MARGIN, DY, W - MARGIN, DY + 40], outline=RED, width=2)
draw_text_block(
    MARGIN + 10, DY + 6,
    "DATE CHECK - Every story above happened or was first reported on "
    "Friday 20 November 2026. Left out as Thursday 19 Nov news: the "
    "Shenzhen three-way talks themselves (only Friday's European reaction "
    "is reported) and Anthropic's Nasdaq debut (only Friday's Asia "
    "sell-off is headlined). Sources: Reuters, BBC, AP wires and the "
    "outlets credited under each story.",
    font(SANS, 11), CW - 20, fill=(90, 20, 18), leading=1.15, max_lines=3)

img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)
