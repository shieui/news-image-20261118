#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news poster and save it as entry.png.

Build-time script only: it needs PIL and the DejaVu fonts on this machine.
The shipped main.py is stdlib-only and just copies the finished image.
Run:  python3 draw_poster.py   (writes entry.png next to this file)
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
NAVY = (22, 35, 63)
NAVY_LIGHT = (38, 56, 92)
RED = (180, 35, 24)
GOLD = (201, 162, 39)
INK = (28, 28, 28)
GREY = (90, 88, 80)
CARD = (255, 255, 255)
CARD_LINE = (216, 210, 196)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)           # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)     # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width` px."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


# ---------------------------------------------------------------- pictograms
def pic_gulf(d, x, y, s):
    """Jet and burst over Gulf waves."""
    d.rectangle([x, y, x + s, y + s], fill=(214, 232, 240))
    for i in range(3):  # sea
        yy = y + s - 26 + i * 9
        d.line([(x + 8, yy), (x + s - 8, yy)], fill=(46, 110, 158), width=3)
    # island + missile site
    d.polygon([(x + s * 0.55, y + s - 30), (x + s * 0.72, y + s - 58),
               (x + s * 0.88, y + s - 30)], fill=(120, 110, 88))
    # jet (side view: nose right, tail fin, swept wing)
    d.polygon([(x + 12, y + 30), (x + 46, y + 24), (x + 86, y + 28),
               (x + 92, y + 31), (x + 86, y + 34), (x + 46, y + 36),
               (x + 12, y + 32)], fill=(40, 40, 48))
    d.polygon([(x + 16, y + 30), (x + 22, y + 16), (x + 30, y + 28)],
              fill=(40, 40, 48))
    d.polygon([(x + 48, y + 26), (x + 58, y + 40), (x + 44, y + 36)],
              fill=(40, 40, 48))
    # explosion starburst
    cx, cy = x + s * 0.74, y + s * 0.42
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 8, 20
        a = math.radians(ang)
        d.line([(cx + r1 * math.cos(a), cy + r1 * math.sin(a)),
                (cx + r2 * math.cos(a), cy + r2 * math.sin(a))],
               fill=(214, 120, 30), width=4)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(240, 170, 40))


def pic_summit(d, x, y, s):
    """Three flags on poles."""
    d.rectangle([x, y, x + s, y + s], fill=(226, 232, 240))
    d.ellipse([x + 6, y + s - 22, x + s - 6, y + s - 6], fill=(150, 170, 150))
    cols = [(200, 40, 30), (30, 90, 170), (200, 40, 30)]
    for i, c in enumerate(cols):
        px = x + 16 + i * 34
        d.line([(px, y + 18), (px, y + s - 18)], fill=(60, 60, 60), width=3)
        d.polygon([(px, y + 18), (px + 30, y + 26), (px, y + 36)], fill=c)
        if i == 2:  # stripes on the third flag
            for k in range(3):
                d.line([(px + 2, y + 22 + k * 5), (px + 28, y + 28 + k * 5)],
                       fill=(255, 255, 255), width=2)
    # handshake arc
    d.arc([x + 22, y + s - 52, x + s - 22, y + s - 8], 200, 340,
          fill=(22, 35, 63), width=4)


def pic_bridge(d, x, y, s):
    """Bridge with its middle span fallen into the strait."""
    d.rectangle([x, y, x + s, y + s], fill=(214, 232, 240))
    for i in range(3):
        yy = y + s - 24 + i * 8
        d.line([(x + 8, yy), (x + s - 8, yy)], fill=(46, 110, 158), width=3)
    mid = x + s // 2
    # deck, left and right, gap in the middle
    d.rectangle([x + 6, y + 34, mid - 16, y + 44], fill=(90, 90, 96))
    d.rectangle([mid + 16, y + 34, x + s - 6, y + 44], fill=(90, 90, 96))
    # arch, broken at the gap
    d.arc([x + 10, y + 6, mid - 6, y + 62], 180, 360, fill=(60, 60, 66),
          width=5)
    d.arc([mid + 6, y + 6, x + s - 10, y + 62], 180, 360, fill=(60, 60, 66),
          width=5)
    # fallen span in the water
    d.polygon([(mid - 14, y + 62), (mid + 14, y + 62), (mid + 6, y + s - 26),
               (mid - 6, y + s - 26)], fill=(120, 120, 126))
    d.line([(mid - 10, y + 50), (mid - 4, y + 58)], fill=(214, 120, 30),
           width=3)
    d.line([(mid + 10, y + 50), (mid + 4, y + 58)], fill=(214, 120, 30),
           width=3)


def pic_ballot(d, x, y, s):
    """Ballot box with a big check and 56-44."""
    d.rectangle([x, y, x + s, y + s], fill=(232, 228, 214))
    d.rectangle([x + 18, y + 52, x + s - 18, y + s - 14], fill=(38, 56, 92))
    d.rectangle([x + 12, y + 42, x + s - 12, y + 54], fill=(22, 35, 63))
    d.rectangle([x + s // 2 - 14, y + 44, x + s // 2 + 14, y + 50],
                fill=(246, 241, 231))
    # ballot going in
    d.rectangle([x + s // 2 - 12, y + 16, x + s // 2 + 12, y + 44],
                fill=(255, 255, 255), outline=(120, 120, 120))
    d.line([(x + s // 2 - 6, y + 30), (x + s // 2 - 1, y + 36),
            (x + s // 2 + 7, y + 24)], fill=(34, 139, 34), width=4)
    # 56-44
    d.text((x + s // 2, y + s - 52), "56-44", font=SANS_B(26),
           fill=(255, 255, 255), anchor="ma")


def pic_virus(d, x, y, s):
    """Spiky virus ball with a red cross."""
    import math
    d.rectangle([x, y, x + s, y + s], fill=(240, 224, 222))
    cx, cy = x + s // 2, y + s // 2 - 4
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        d.line([(cx + 26 * math.cos(a), cy + 26 * math.sin(a)),
                (cx + 40 * math.cos(a), cy + 40 * math.sin(a))],
               fill=(180, 35, 24), width=5)
        ex, ey = cx + 44 * math.cos(a), cy + 44 * math.sin(a)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(180, 35, 24))
    d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(214, 90, 70))
    d.ellipse([cx - 16, cy - 20, cx - 2, cy - 6], fill=(232, 140, 120))
    # small red cross badge
    bx, by = x + s - 34, y + s - 34
    d.rectangle([bx, by, bx + 26, by + 26], fill=(255, 255, 255),
                outline=(180, 35, 24), width=2)
    d.rectangle([bx + 11, by + 4, bx + 15, by + 22], fill=(180, 35, 24))
    d.rectangle([bx + 4, by + 11, bx + 22, by + 15], fill=(180, 35, 24))


def pic_voyager(d, x, y, s):
    """Dish antenna, stars and a tiny probe on a signal line."""
    import math
    d.rectangle([x, y, x + s, y + s], fill=(22, 35, 63))
    for (sx, sy, r) in [(18, 18, 2), (70, 12, 2), (96, 30, 2), (30, 40, 1),
                        (88, 60, 1), (14, 70, 2), (60, 88, 1)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                  fill=(255, 255, 255))
    # dish
    d.pieslice([x + 14, y + 44, x + 62, y + 92], 180, 360, fill=(200, 205, 215))
    d.line([(x + 38, y + 68), (x + 38, y + s - 10)], fill=(200, 205, 215),
           width=4)
    d.line([(x + 24, y + s - 10), (x + 52, y + s - 10)], fill=(200, 205, 215),
           width=4)
    # signal line to the probe
    d.line([(x + 56, y + 34), (x + 92, y + 18)], fill=(201, 162, 39), width=3)
    d.ellipse([x + 88, y + 12, x + 100, y + 24], fill=(201, 162, 39))
    d.line([(x + 94, y + 12), (x + 98, y + 4)], fill=(201, 162, 39), width=2)
    d.text((x + s - 6, y + s - 26), "1 light-day", font=SANS_B(13),
           fill=(201, 162, 39), anchor="ra")


# ------------------------------------------------------------------- stories
STORIES = [
    ("MIDDLE EAST", "U.S. strikes Iran;\nIran hits Gulf bases",
     "U.S. jets hit a missile site on Qeshm Island. Iran fired drones "
     "at U.S. bases in Kuwait and Bahrain.", pic_gulf),
    ("ASIA", "Xi and Putin meet\nbefore Trump summit",
     "The two leaders opened the APEC summit in Shenzhen, a day before "
     "a first three-way meeting with Donald Trump.", pic_summit),
    ("UKRAINE", "Kerch Bridge road span\nfalls into the sea",
     "A second night of Ukrainian strikes brought down the bridge's "
     "main road arch; rail traffic partly resumed.", pic_bridge),
    ("UNITED STATES", "Democrats take\nthe Senate, 56-44",
     "Mary Peltola beat Dan Sullivan in Alaska, the last Senate race "
     "of the midterms, called by the AP.", pic_ballot),
    ("HEALTH", "U.S. loses measles-free\nstatus after 26 years",
     "PAHO ruled the virus has spread for over a year: 5,412 cases in "
     "2026, the most since 1991.", pic_virus),
    ("SPACE", "Voyager 1 reaches one\nlight-day from Earth",
     "At 5:16 a.m. ET the 1977 probe became the first human-made "
     "object a full day of light away - 16 billion miles.", pic_voyager),
]

ALSO_TODAY = ("Ebola in DR Congo passes 11,000 cases  ·  "
              "Nvidia reports a record $115.8bn quarter  ·  "
              "Category 5 Cyclone Xavier nears the Northern Cook Islands")


def draw_card(d, x, y, w, h, kicker, headline, body, pic):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=CARD_LINE, width=2)
    d.rectangle([x, y, x + w, y + 6], fill=RED)
    px, py, ps = x + 14, y + 20, 108
    pic(d, px, py, ps)
    tx = px + ps + 14
    tw = x + w - 16 - tx
    d.text((tx, y + 18), kicker, font=SANS_B(15), fill=RED)
    hf = SERIF_B(25)
    lines = []
    for part in headline.split("\n"):
        lines += wrap(d, part, hf, tw)
    ly = y + 42
    for ln in lines[:2]:
        d.text((tx, ly), ln, font=hf, fill=INK)
        ly += 30
    bf = SANS(18)
    blines = wrap(d, body, bf, tw)
    by = ly + 4
    for ln in blines[:4]:
        d.text((tx, by), ln, font=bf, fill=(58, 56, 50))
        by += 23


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    d.text((W // 2, 22), "THE WORLD IN ONE DAY", font=SERIF_B(52),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 92), "Wednesday 18 November 2026", font=SANS_B(34),
           fill=GOLD, anchor="ma")
    # story grid: 2 cols x 3 rows
    gx, gy, gap = 20, 172, 16
    cw = (W - 2 * gx - gap) // 2
    ch = 218
    for i, (kicker, head, body, pic) in enumerate(STORIES):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        draw_card(d, cx, cy, cw, ch, kicker, head, body, pic)
    # footer strip
    fy = gy + 3 * ch + 2 * gap + 12
    d.rectangle([gx, fy, W - gx, fy + 74], fill=NAVY_LIGHT)
    d.text((gx + 16, fy + 10), "ALSO TODAY", font=SANS_B(16), fill=GOLD)
    af = SANS(17)
    alines = wrap(d, ALSO_TODAY, af, W - 2 * gx - 32)
    ay = fy + 34
    for ln in alines[:2]:
        d.text((gx + 16, ay), ln, font=af, fill=(255, 255, 255))
        ay += 21
    d.text((W // 2, H - 26),
           "Sources: Reuters  ·  AP  ·  NASA  ·  PAHO  ·  UN  —  18 November 2026",
           font=SANS(14), fill=GREY, anchor="ma")
    # thin outer border
    d.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=3)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
