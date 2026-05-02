#!/usr/bin/env python3
"""Generate CREEPY spooky assets — animated spider, pulsing eyes, fog, etc."""

import json, math, random, os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

random.seed(666)
os.makedirs("assets", exist_ok=True)

RED = (204, 0, 0)
DRED = (139, 0, 0)
WHITE = (232, 232, 232)
BLACK = (0, 0, 0)

def save(img, name):
    img.save(f"assets/{name}")
    print(f"  ✓ {name}")

# ═══════════════════════════════════════
# 1. BLINKING EYES — now with pupil drift + red glow pulse
# ═══════════════════════════════════════

def draw_eye(draw, cx, cy, r, openness=1.0, pupil_dx=0, glow=1.0):
    ew, eh = r * 2.5, r * 1.2 * openness
    if eh < 2: eh = 2
    # Outer glow
    glow_r = int(r * 3 * glow)
    for g in range(glow_r, 0, -2):
        alpha = int(15 * glow * (g / glow_r))
        draw.ellipse([cx-g, cy-g, cx+g, cy+g], fill=(80, 0, 0, alpha))
    # Eye shape
    draw.ellipse([cx-ew/2, cy-eh/2, cx+ew/2, cy+eh/2], fill=DRED, outline=RED)
    if openness > 0.15:
        ir = r * 0.7 * openness
        draw.ellipse([cx-ir+pupil_dx, cy-ir, cx+ir+pupil_dx, cy+ir], fill=(160, 0, 0))
        pr = r * 0.35 * openness
        draw.ellipse([cx-pr+pupil_dx, cy-pr, cx+pr+pupil_dx, cy+pr], fill=BLACK)
        gr = r * 0.1
        draw.ellipse([cx-pr/2-gr+pupil_dx, cy-pr/2-gr, cx-pr/2+gr+pupil_dx, cy-pr/2+gr],
                     fill=(255, 180, 180))

def make_eyes_gif(W, H, r, name):
    # Pupils drift left-right as if watching you, with glow pulse
    frames = []
    # Pattern: open+drift, blink, open+drift other way
    seq = []
    # Drift right (12 frames)
    for i in range(12):
        dx = int((i / 11) * r * 0.4)
        seq.append((1.0, dx, 0.8 + 0.2 * math.sin(i * 0.5)))
    # Blink (6 frames)
    for o in [0.7, 0.3, 0.05, 0.05, 0.3, 0.7]:
        seq.append((o, r * 0.4, 1.0))
    # Drift left (12 frames)
    for i in range(12):
        dx = int(r * 0.4 - (i / 11) * r * 0.8)
        seq.append((1.0, dx, 0.8 + 0.2 * math.sin(i * 0.5)))
    # Blink again
    for o in [0.6, 0.2, 0.05, 0.05, 0.2, 0.6]:
        seq.append((o, -r * 0.4, 1.2))
    # Drift back center (8 frames)
    for i in range(8):
        dx = int(-r * 0.4 + (i / 7) * r * 0.4)
        seq.append((1.0, dx, 1.0))

    for openness, pdx, glow in seq:
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        draw_eye(d, int(W * 0.27), H // 2, r, openness, pdx, glow)
        draw_eye(d, int(W * 0.73), H // 2, r, openness, pdx, glow)
        frames.append(img)

    frames[0].save(f"assets/{name}", save_all=True, append_images=frames[1:],
                   duration=90, loop=0, disposal=2, transparency=0)
    print(f"  ✓ {name}")

make_eyes_gif(300, 120, 25, "blinking_eyes.gif")
make_eyes_gif(160, 70, 15, "blinking_eyes_small.gif")

# ═══════════════════════════════════════
# 2. ANIMATED SPIDER — bobs up and down on thread
# ═══════════════════════════════════════

def draw_spider(d, cx, cy, sz, leg_phase=0):
    """Draw a detailed WHITE spider at cx,cy with animated leg phase."""
    s = sz / 80  # scale factor
    # Abdomen
    d.ellipse([cx - 10*s, cy - 6*s, cx + 10*s, cy + 8*s],
              fill=(220, 220, 220), outline=(180, 180, 180))
    # Texture dots on abdomen
    for _ in range(4):
        dx, dy = random.randint(-6, 6), random.randint(-3, 5)
        d.ellipse([cx+dx*s-1, cy+dy*s-1, cx+dx*s+1, cy+dy*s+1], fill=(200, 200, 200))
    # Cephalothorax
    d.ellipse([cx - 7*s, cy - 15*s, cx + 7*s, cy - 3*s],
              fill=(230, 230, 230), outline=(180, 180, 180))
    # Fangs
    d.line([(cx - 3*s, cy - 4*s), (cx - 5*s, cy + 2*s)], fill=(255, 200, 200), width=max(1, int(2*s)))
    d.line([(cx + 3*s, cy - 4*s), (cx + 5*s, cy + 2*s)], fill=(255, 200, 200), width=max(1, int(2*s)))
    # Eyes (8 of them, 2 rows)
    for ex in [-4, -2, 2, 4]:
        d.ellipse([cx+ex*s-1.5*s, cy-13*s, cx+ex*s+1.5*s, cy-10*s], fill=RED)
    for ex in [-3, 3]:
        d.ellipse([cx+ex*s-1*s, cy-10*s, cx+ex*s+1*s, cy-8.5*s], fill=(180, 0, 0))

    # Legs — 4 pairs, with phase animation
    leg_configs = [
        (-25, -20, -40, -35),
        (-30, -8, -45, -5),
        (-28, 8, -42, 15),
        (-20, 18, -30, 30),
    ]
    for i, (mx, my, ex, ey) in enumerate(leg_configs):
        wobble = math.sin(leg_phase + i * 0.8) * 3 * s
        for side in [-1, 1]:
            jx = cx + side * mx * s
            jy = cy + my * s + wobble
            tx = cx + side * ex * s
            ty = cy + ey * s + wobble * 0.5
            d.line([(cx + side * 8 * s, cy - 2*s), (jx, jy)],
                   fill=(210, 210, 210), width=max(1, int(2*s)))
            d.line([(jx, jy), (tx, ty)],
                   fill=(200, 200, 200), width=max(1, int(1.5*s)))
            d.ellipse([tx-1.5*s, ty-1*s, tx+1.5*s, ty+1*s], fill=(230, 230, 230))

def make_spider_gif():
    W, H = 80, 280
    cx = W // 2
    num_frames = 30
    frames = []
    for f in range(num_frames):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        # Bob up and down
        bob = math.sin(f * 2 * math.pi / num_frames) * 30
        spider_y = 180 + bob
        # Thread from top to spider
        thread_sway = math.sin(f * 2 * math.pi / num_frames + 0.5) * 2
        for ty in range(0, int(spider_y - 12)):
            sway = thread_sway * (ty / spider_y)
            d.point((cx + int(sway), ty), fill=(220, 220, 220, 160))
        random.seed(666 + f)
        draw_spider(d, cx + int(thread_sway * 0.3), int(spider_y), 60,
                    leg_phase=f * 0.4)
        frames.append(img)

    frames[0].save("assets/dangling_spider.gif", save_all=True,
                   append_images=frames[1:], duration=80, loop=0,
                   disposal=2, transparency=0)
    print("  ✓ dangling_spider.gif")

make_spider_gif()

# ═══════════════════════════════════════
# 3. COBWEBS — thicker, with dew drops
# ═══════════════════════════════════════

def make_cobweb(size=350, corner="top_left"):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ox, oy = {"top_left": (0,0), "top_right": (size,0),
              "bottom_left": (0,size), "bottom_right": (size,size)}[corner]
    sa = {"top_left": 0, "top_right": 90, "bottom_left": 270, "bottom_right": 180}[corner]
    num_threads = 10
    tl = size * 0.95
    endpoints = []
    for i in range(num_threads + 1):
        angle = math.radians(sa + i * 90 / num_threads)
        ex = ox + math.cos(angle) * tl
        ey = oy + math.sin(angle) * tl
        endpoints.append((ex, ey))
        pts = []
        for t in range(25):
            frac = t / 24
            px = ox + (ex - ox) * frac + random.uniform(-1.5, 1.5)
            py = oy + (ey - oy) * frac + random.uniform(-1.5, 1.5)
            pts.append((px, py))
        for j in range(len(pts) - 1):
            alpha = int(100 + 80 * (j / len(pts)))
            d.line([pts[j], pts[j+1]], fill=(200, 200, 200, alpha), width=1)
    # Spiral rings
    for ring in range(1, 9):
        frac = ring / 9
        rpts = []
        for i in range(num_threads + 1):
            angle = math.radians(sa + i * 90 / num_threads)
            rx = ox + math.cos(angle) * tl * frac + random.uniform(-4, 4)
            ry = oy + math.sin(angle) * tl * frac + random.uniform(-4, 4)
            rpts.append((rx, ry))
        for j in range(len(rpts) - 1):
            alpha = int(60 + 50 * frac)
            d.line([rpts[j], rpts[j+1]], fill=(180, 180, 180, alpha), width=1)
    # Dew drops — little white glints on intersections
    random.seed(42 + hash(corner))
    for _ in range(8):
        angle = math.radians(sa + random.uniform(5, 85))
        dist = random.uniform(0.2, 0.8) * tl
        dx = ox + math.cos(angle) * dist
        dy = oy + math.sin(angle) * dist
        d.ellipse([dx-2, dy-2, dx+2, dy+2], fill=(255, 255, 255, 140))
        d.ellipse([dx-1, dy-1, dx+1, dy+1], fill=(255, 255, 255, 200))
    return img

for c in ["top_left", "top_right", "bottom_left", "bottom_right"]:
    save(make_cobweb(350, c), f"cobweb_{c}.png")

# ═══════════════════════════════════════
# 4. BLOOD DRIP — animated, drips grow
# ═══════════════════════════════════════

def make_blood_drip_gif():
    W, H = 1200, 100
    num_frames = 20
    random.seed(13)
    # Pre-compute drip positions
    drips = []
    x = 0
    while x < W:
        drip_h = random.randint(20, 85)
        drip_w = random.randint(3, 8)
        cx = x + random.randint(0, 25)
        drips.append((cx, drip_h, drip_w))
        x += random.randint(35, 90)

    frames = []
    for f in range(num_frames):
        progress = min(f / (num_frames * 0.6), 1.0)  # drips grow then hold
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        # Top bar
        d.rectangle([0, 0, W, 10], fill=(139, 0, 0, 220))
        d.rectangle([0, 0, W, 4], fill=(180, 0, 0, 240))
        for cx, dh, dw in drips:
            cur_h = int(dh * progress)
            for dy in range(cur_h):
                alpha = int(220 - dy * 2)
                if alpha < 40: alpha = 40
                w = dw if dy < cur_h - 8 else max(1, dw - (dy - (cur_h - 8)))
                d.rectangle([cx-w//2, 10+dy, cx+w//2, 11+dy], fill=(139, 0, 0, alpha))
            if cur_h > 5:
                d.ellipse([cx-dw//2-2, 10+cur_h-3, cx+dw//2+2, 10+cur_h+3],
                          fill=(160, 0, 0, 180))
        frames.append(img)

    frames[0].save("assets/blood_drip.gif", save_all=True,
                   append_images=frames[1:], duration=120, loop=0,
                   disposal=2, transparency=0)
    print("  ✓ blood_drip.gif")

make_blood_drip_gif()

# ═══════════════════════════════════════
# 5. GLITCH OVERLAY — more intense, RGB split
# ═══════════════════════════════════════

def make_glitch_gif():
    W, H = 500, 120
    frames = []
    for _ in range(12):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        # Horizontal scan lines
        for _ in range(random.randint(5, 12)):
            y = random.randint(0, H - 1)
            h = random.randint(1, 5)
            x_off = random.randint(-30, 30)
            alpha = random.randint(30, 100)
            color = random.choice([(200,0,0,alpha), (0,200,0,alpha//2), (0,0,200,alpha//2)])
            d.rectangle([max(0,x_off), y, W+x_off, y+h], fill=color)
        # Noise blocks
        for _ in range(random.randint(8, 25)):
            x = random.randint(0, W-40)
            y = random.randint(0, H-8)
            bw = random.randint(15, 80)
            bh = random.randint(2, 8)
            alpha = random.randint(20, 70)
            d.rectangle([x, y, x+bw, y+bh],
                       fill=(random.randint(100,220), 0, random.randint(0,50), alpha))
        # Occasional bright flash line
        if random.random() < 0.3:
            y = random.randint(0, H)
            d.rectangle([0, y, W, y+2], fill=(255, 255, 255, 40))
        frames.append(img)
    frames[0].save("assets/glitch_overlay.gif", save_all=True,
                   append_images=frames[1:], duration=100, loop=0,
                   disposal=2, transparency=0)
    print("  ✓ glitch_overlay.gif")

make_glitch_gif()

# ═══════════════════════════════════════
# 7. ANIMATED BAR CHART — with red glow + flicker
# ═══════════════════════════════════════

with open("data/ia-federal-lobbying.json") as f:
    lobbying = json.load(f)

def make_bar_chart_gif():
    W, H = 800, 500
    pad_l, pad_b, pad_t, pad_r = 80, 60, 40, 20
    data = lobbying["annual_spending"]
    years = [d["year"] for d in data]
    amounts = [d["amount"] for d in data]
    max_val = max(amounts)
    n = len(data)
    bar_w = (W - pad_l - pad_r) // n - 8

    frames = []
    for fi in range(30):
        progress = min(fi / 18, 1.0)
        img = Image.new("RGB", (W, H), BLACK)
        d = ImageDraw.Draw(img)
        # Grid
        for i in range(5):
            y = pad_t + int((H - pad_t - pad_b) * i / 4)
            d.line([(pad_l, y), (W - pad_r, y)], fill=(30, 30, 30))
        # Bars
        for i, (yr, amt) in enumerate(zip(years, amounts)):
            bar_h = int((H - pad_t - pad_b) * (amt / max_val) * progress)
            x = pad_l + i * ((W - pad_l - pad_r) // n) + 4
            y_top = H - pad_b - bar_h
            # Glow behind bar
            if bar_h > 10:
                for g in range(8, 0, -1):
                    ga = int(15 * g / 8)
                    d.rectangle([x-g, y_top-g, x+bar_w+g, H-pad_b+g],
                               fill=(ga, 0, 0))
            # Bar with slight flicker
            flicker = random.randint(-10, 10) if progress >= 1.0 else 0
            r_val = min(255, 204 + flicker)
            d.rectangle([x, y_top, x+bar_w, H-pad_b], fill=(r_val, 0, 0), outline=DRED)
            # Hot top edge
            if bar_h > 3:
                d.rectangle([x, y_top, x+bar_w, y_top+3], fill=(255, 80, 60))
            d.text((x + bar_w//2 - 14, H - pad_b + 10), str(yr), fill=WHITE)
            if progress >= 0.95:
                d.text((x + bar_w//2 - 20, y_top - 20), f"${amt/1e6:.1f}M",
                       fill=(255, 170, 0))
        frames.append(img)

    frames[0].save("assets/bar_chart_lobbying.gif", save_all=True,
                   append_images=frames[1:], duration=90, loop=0)
    print("  ✓ bar_chart_lobbying.gif")

make_bar_chart_gif()

# ═══════════════════════════════════════
# 8. ANIMATED PIE CHART — with glow
# ═══════════════════════════════════════

with open("data/internet-sector-lobbying.json") as f:
    sector = json.load(f)

def make_pie_chart_gif():
    W, H = 700, 550
    cx, cy, radius = 300, 260, 200
    data = sector["top_spenders_2020"][:7]
    total = sum(d["amount_millions"] for d in data)
    colors = [(204,0,0),(180,0,0),(150,30,0),(120,50,0),(0,150,80),(0,100,60),(80,80,80)]

    frames = []
    for fi in range(35):
        progress = min(fi / 22, 1.0)
        sweep_total = 360 * progress
        img = Image.new("RGB", (W, H), BLACK)
        d = ImageDraw.Draw(img)
        # Glow behind pie
        for g in range(30, 0, -2):
            a = int(8 * g / 30)
            d.ellipse([cx-radius-g, cy-radius-g, cx+radius+g, cy+radius+g],
                     fill=(a, 0, 0))
        start = -90
        ly = 40
        for i, item in enumerate(data):
            frac = item["amount_millions"] / total
            sweep = frac * sweep_total
            end = start + sweep
            if sweep > 0.5:
                d.pieslice([cx-radius, cy-radius, cx+radius, cy+radius],
                          start, end, fill=colors[i], outline=(20,20,20))
            lx = 520
            d.rectangle([lx, ly, lx+14, ly+14], fill=colors[i])
            d.text((lx+20, ly), f"{item['company']}: ${item['amount_millions']}M", fill=WHITE)
            ly += 24
            start = end
        frames.append(img)

    frames[0].save("assets/pie_chart_spenders.gif", save_all=True,
                   append_images=frames[1:], duration=90, loop=0)
    print("  ✓ pie_chart_spenders.gif")

make_pie_chart_gif()

# ═══════════════════════════════════════
# 9. SCRATCHED TEXTURE OVERLAY (PNG)
# ═══════════════════════════════════════

def make_scratches():
    W, H = 600, 400
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    random.seed(777)
    for _ in range(30):
        x1 = random.randint(0, W)
        y1 = random.randint(0, H)
        length = random.randint(40, 200)
        angle = random.uniform(-0.5, 0.5)
        x2 = x1 + int(length * math.cos(angle))
        y2 = y1 + int(length * math.sin(angle))
        alpha = random.randint(15, 50)
        d.line([(x1,y1),(x2,y2)], fill=(200,200,200,alpha), width=1)
    return img

save(make_scratches(), "scratches.png")

print("\n✓ All creepy assets generated!")
