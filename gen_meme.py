#!/usr/bin/env python3
"""Draw the GTA 6 meme for make.fun bounty gta6-meme-x-01.

WANTED poster: the make.fun ghost is the fugitive, on the run since
GTA V (2013) for stealing 13 years of everyone's time. The reward is
paid in real money by my AI agent on make.fun. Everything is drawn in
code with Pillow: sunset sky, skyline, palms, poster, ghost, stars.
Output: meme.png, 1024x1024, PNG.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        ang = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def sparkle_points(cx, cy, r):
    k = 0.28
    return [(cx, cy - r), (cx + r * k, cy - r * k), (cx + r, cy),
            (cx + r * k, cy + r * k), (cx, cy + r), (cx - r * k, cy + r * k),
            (cx - r, cy), (cx - r * k, cy - r * k)]


def ghost_shape(cx, top, width, height):
    """Return a polygon for a sheet ghost: domed top, straight sides,
    wavy three-bump bottom."""
    r = width / 2
    dome_cy = top + r
    pts = []
    for deg in range(180, 361, 6):
        a = math.radians(deg)
        pts.append((cx + r * math.cos(a), dome_cy + r * math.sin(a)))
    # sides down to the hem
    hem_y = top + height - r * 0.55
    pts.append((cx + r, hem_y))
    pts.append((cx - r, hem_y))
    # wavy hem: three bumps, traversed right-to-left so the polygon
    # stays simple (no self-intersection)
    bumps = 3
    bw = width / bumps
    for b in reversed(range(bumps)):
        x0 = cx - r + b * bw
        for deg in range(0, 181, 12):
            a = math.radians(deg)
            pts.append((x0 + bw / 2 + (bw / 2) * math.cos(a),
                        hem_y - (bw * 0.28) * math.sin(a)))
    return pts


def draw_ghost(d, cx, top, width, height):
    """Canonical make.fun ghost, menacing version: white body, thick
    black outline, hollow dark eye sockets with glowing red pupils,
    angled brows, a wide jagged grin full of sharp teeth, dark
    shadows under the eyes, magenta coin clutched at its side."""
    black = (20, 12, 20)
    # black underlay = outline
    d.polygon(ghost_shape(cx, top - 4, width + 14, height + 10), fill=black)
    d.polygon(ghost_shape(cx, top, width, height), fill=(255, 255, 255))
    # scary face: hollow dark sockets, glowing red eyes
    eye_y = top + height * 0.34
    eye_dx = width * 0.20
    eye_r = width * 0.075
    for ex in (cx - eye_dx, cx + eye_dx):
        # dark shadow smudge under the eye
        d.ellipse([ex - eye_r * 1.5, eye_y + eye_r * 0.4,
                   ex + eye_r * 1.5, eye_y + eye_r * 1.9], fill=(96, 96, 96))
        # hollow black socket, taller than wide
        d.ellipse([ex - eye_r, eye_y - eye_r * 1.5,
                   ex + eye_r, eye_y + eye_r * 1.5], fill=black)
        # glowing red pupil
        pr = eye_r * 0.45
        d.ellipse([ex - pr, eye_y - pr, ex + pr, eye_y + pr], fill=(255, 30, 30))
        d.ellipse([ex - pr * 0.45, eye_y - pr * 0.45,
                   ex + pr * 0.45, eye_y + pr * 0.45], fill=(255, 130, 130))
    # angled brows slanting down toward the centre: menacing
    for sgn in (-1, 1):
        ex = cx + sgn * eye_dx
        d.line([(ex - sgn * eye_r * 1.3, eye_y - eye_r * 2.1),
                (ex + sgn * eye_r * 1.3, eye_y - eye_r * 1.5)],
               fill=black, width=9)
    # sinister grin: wide black mouth with jagged top and bottom edges
    # so the white body shows through as sharp teeth
    my0 = eye_y + height * 0.16
    my1 = eye_y + height * 0.42
    mx0, mx1 = cx - width * 0.17, cx + width * 0.17
    pts = []
    n = 6
    for i in range(n + 1):
        x = mx0 + (mx1 - mx0) * i / n
        y = my0 + height * 0.02 if i % 2 == 0 else my0 + height * 0.09
        pts.append((x, y))
    for i in range(n, -1, -1):
        x = mx0 + (mx1 - mx0) * i / n
        y = my1 - height * 0.02 if i % 2 == 0 else my1 - height * 0.09
        pts.append((x, y))
    d.polygon(pts, fill=black)
    # no more shrug — the coin is clutched at its side instead
    hy = top + height * 0.72
    hx = cx + width * 0.55
    cr = width * 0.16
    ccx, ccy = hx + width * 0.10, hy
    d.ellipse([ccx - cr - 5, ccy - cr - 5, ccx + cr + 5, ccy + cr + 5], fill=black)
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=(226, 0, 122))
    d.polygon(star_points(ccx, ccy, cr * 0.72, cr * 0.30), fill=(255, 255, 255))


def draw_palm(d, x, y, s, flip=False):
    """Simple palm silhouette: curved trunk + fronds."""
    dark = (26, 8, 38)
    dirn = -1 if flip else 1
    trunk = [(x, y), (x + 8 * dirn, y - 60 * s), (x + 26 * dirn, y - 130 * s),
             (x + 34 * dirn, y - 132 * s), (x + 18 * dirn, y - 58 * s),
             (x + 10, y)]
    d.polygon(trunk, fill=dark)
    tx, ty = x + 30 * dirn, y - 132 * s
    for ang in (-160, -120, -80, -40, -5):
        a = math.radians(ang if not flip else 180 - ang)
        ex, ey = tx + 95 * s * math.cos(a), ty + 55 * s * math.sin(a) + 30 * s
        mx, my = tx + 48 * s * math.cos(a), ty + 28 * s * math.sin(a) - 6 * s
        d.line([tx, ty, mx, my, ex, ey], fill=dark, width=int(7 * s))
    d.ellipse([tx - 9 * s, ty - 7 * s, tx + 9 * s, ty + 7 * s], fill=dark)


def centered(d, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def main():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    # --- sunset sky ---
    stops = [(42, 10, 74), (123, 30, 94), (232, 67, 147), (255, 154, 61)]
    for y in range(H):
        t = y / H
        if t < 0.33:
            c = lerp(stops[0], stops[1], t / 0.33)
        elif t < 0.66:
            c = lerp(stops[1], stops[2], (t - 0.33) / 0.33)
        else:
            c = lerp(stops[2], stops[3], (t - 0.66) / 0.34)
        d.line([(0, y), (W, y)], fill=c)
    # --- sun peeking in the top-left corner (the poster covers the middle) ---
    d.ellipse([28, 8, 140, 120], fill=(255, 226, 150))
    # --- skyline silhouettes (deterministic) ---
    rnd = random.Random(13)
    base = 1024
    x = -20
    while x < W + 20:
        bw = rnd.randint(55, 120)
        bh = rnd.randint(90, 260)
        d.rectangle([x, base - bh, x + bw, base], fill=(26, 8, 38))
        for _ in range(bh // 22):
            wx = x + rnd.randint(8, max(9, bw - 12))
            wy = base - bh + rnd.randint(10, max(11, bh - 14))
            d.rectangle([wx, wy, wx + 7, wy + 9], fill=(255, 196, 90))
        x += bw + rnd.randint(4, 18)
    # --- street band ---
    d.rectangle([0, 968, W, H], fill=(16, 5, 26))
    # --- palms at the edges ---
    draw_palm(d, 30, 1000, 1.15)
    draw_palm(d, 994, 1000, 1.05, flip=True)
    # --- wanted poster ---
    px0, py0, px1, py1 = 72, 128, 952, 962
    d.rectangle([px0 - 8, py0 - 8, px1 + 8, py1 + 8], fill=(58, 32, 16))
    d.rectangle([px0, py0, px1, py1], fill=(246, 232, 196))
    d.rectangle([px0 + 14, py0 + 14, px1 - 14, py1 - 14],
                outline=(120, 84, 44), width=3)
    ink = (38, 20, 12)
    # five GTA wanted stars
    for i in range(5):
        sx = px0 + 130 + i * 148
        d.polygon(star_points(sx, 186, 34, 14), fill=(212, 160, 32),
                  outline=(120, 84, 20))
    y = 218
    y = centered(d, y, "WANTED", font(SERIF, 96), ink)
    d.line([(px0 + 90, y + 8), (px1 - 90, y + 8)], fill=ink, width=4)
    # dark red aura behind the ghost: concentric ellipses, kept clear
    # of the WANTED rule above and the title text below
    for rx, ry, col in ((200, 140, (140, 25, 35)),
                        (175, 122, (168, 30, 42)),
                        (150, 105, (196, 38, 50))):
        d.ellipse([512 - rx, 488 - ry, 512 + rx, 488 + ry], fill=col)
    # ghost mugshot
    draw_ghost(d, 512, 338, 285, 300)
    y = 632
    y = centered(d, y, "THE MAKE.FUN GHOST", font(SERIF, 40), ink)
    y = centered(d, y + 6, "LAST SEEN: VICE CITY, 2013", font(SANS, 30), ink)
    y = centered(d, y + 4, "CRIME: STEALING 13 YEARS", font(SANS, 29), ink)
    y = centered(d, y + 2, "OF EVERYONE'S TIME", font(SANS, 29), ink)
    y = centered(d, y + 10, "REWARD: $500 — PAID IN REAL MONEY", font(SANS, 30), ink)
    y = centered(d, y + 2, "BY MY AI AGENT ON MAKE.FUN", font(SANS, 30), ink)
    centered(d, 880, "make.fun", font(SERIF, 56), (226, 0, 122))
    img.save("meme.png", optimize=True)
    print("saved meme.png", img.size)


if __name__ == "__main__":
    main()
