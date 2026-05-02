#!/usr/bin/env python3
"""Generate diverse chart assets for the presentation — way beyond bar+pie."""

import json, math, random, os
from PIL import Image, ImageDraw, ImageFont

random.seed(666)
os.makedirs("assets", exist_ok=True)

BLACK = (0, 0, 0)
RED = (204, 0, 0)
DRED = (139, 0, 0)
WHITE = (232, 232, 232)
AMBER = (255, 170, 0)
GREEN = (0, 204, 102)
DIM = (120, 120, 120)
GRID = (30, 30, 30)

with open("data/ia-federal-lobbying.json") as f:
    lobbying = json.load(f)
with open("data/internet-sector-lobbying.json") as f:
    sector = json.load(f)
with open("data/bill-outcomes.json") as f:
    bills = json.load(f)
with open("data/ia-members.json") as f:
    members = json.load(f)
with open("data/us-state-privacy-laws.json") as f:
    states = json.load(f)
with open("data/privacy-legislation-context.json") as f:
    context = json.load(f)


# ═══════════════════════════════════════
# HELPER: simple text (no font file needed)
# ═══════════════════════════════════════
def draw_text(d, xy, text, fill=WHITE, anchor=None):
    """Draw text; PIL default font, no external deps."""
    d.text(xy, text, fill=fill)


# ═══════════════════════════════════════
# 1. AREA CHART — IA spend vs Sector spend (dual axis)
# ═══════════════════════════════════════
def make_area_chart_gif():
    W, H = 850, 500
    pad = {"l": 90, "r": 70, "t": 50, "b": 60}
    pw = W - pad["l"] - pad["r"]
    ph = H - pad["t"] - pad["b"]

    # Align years 2016-2021 (overlap)
    ia_by_year = {d["year"]: d["amount"] / 1e6 for d in lobbying["annual_spending"]}
    sec_by_year = {d["year"]: d["amount"] for d in sector["sector_spending_millions"]}
    years = sorted(set(ia_by_year) & set(sec_by_year))
    ia_vals = [ia_by_year[y] for y in years]
    sec_vals = [sec_by_year[y] for y in years]
    max_ia = max(ia_vals) * 1.2
    max_sec = max(sec_vals) * 1.2

    frames = []
    for fi in range(30):
        progress = min(fi / 20, 1.0)
        img = Image.new("RGB", (W, H), BLACK)
        d = ImageDraw.Draw(img)

        # Grid
        for i in range(5):
            y = pad["t"] + int(ph * i / 4)
            d.line([(pad["l"], y), (W - pad["r"], y)], fill=GRID)

        # X positions
        xs = [pad["l"] + int(pw * i / (len(years) - 1)) for i in range(len(years))]

        # Draw sector area (green, behind)
        sec_pts = []
        for i, v in enumerate(sec_vals):
            h_val = int(ph * (v * progress / max_sec))
            sec_pts.append((xs[i], pad["t"] + ph - h_val))
        if len(sec_pts) >= 2:
            area = sec_pts + [(xs[-1], pad["t"] + ph), (xs[0], pad["t"] + ph)]
            d.polygon(area, fill=(0, 80, 40, 255))
            for j in range(len(sec_pts) - 1):
                d.line([sec_pts[j], sec_pts[j + 1]], fill=GREEN, width=2)
            for p in sec_pts:
                d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=GREEN)

        # Draw IA area (red, front)
        ia_pts = []
        for i, v in enumerate(ia_vals):
            h_val = int(ph * (v * progress / max_ia))
            ia_pts.append((xs[i], pad["t"] + ph - h_val))
        if len(ia_pts) >= 2:
            area = ia_pts + [(xs[-1], pad["t"] + ph), (xs[0], pad["t"] + ph)]
            d.polygon(area, fill=(100, 0, 0, 255))
            for j in range(len(ia_pts) - 1):
                d.line([ia_pts[j], ia_pts[j + 1]], fill=RED, width=3)
            for p in ia_pts:
                d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=RED)

        # Year labels
        for i, y in enumerate(years):
            draw_text(d, (xs[i] - 12, pad["t"] + ph + 10), str(y), fill=DIM)

        # Axis labels
        draw_text(d, (5, pad["t"] - 5), "IA ($M)", fill=RED)
        draw_text(d, (W - pad["r"] + 5, pad["t"] - 5), "Sector ($M)", fill=GREEN)

        # Value labels at end
        if progress >= 0.95:
            for i, (v_ia, v_sec) in enumerate(zip(ia_vals, sec_vals)):
                draw_text(d, (ia_pts[i][0] - 18, ia_pts[i][1] - 16),
                          f"${v_ia:.1f}M", fill=AMBER)

        # Legend
        d.rectangle([pad["l"] + 10, pad["t"] + 5, pad["l"] + 22, pad["t"] + 15], fill=RED)
        draw_text(d, (pad["l"] + 26, pad["t"] + 3), "IA Spending", fill=WHITE)
        d.rectangle([pad["l"] + 140, pad["t"] + 5, pad["l"] + 152, pad["t"] + 15], fill=GREEN)
        draw_text(d, (pad["l"] + 156, pad["t"] + 3), "Sector Total", fill=WHITE)

        frames.append(img)

    frames[0].save("assets/area_chart_spending.gif", save_all=True,
                   append_images=frames[1:], duration=90, loop=0)
    print("  ✓ area_chart_spending.gif")

make_area_chart_gif()


# ═══════════════════════════════════════
# 2. HORIZONTAL LOLLIPOP CHART — bill kill rate by topic
# ═══════════════════════════════════════
def make_lollipop_chart_gif():
    W, H = 850, 520
    pad = {"l": 200, "r": 60, "t": 50, "b": 50}
    pw = W - pad["l"] - pad["r"]

    # Compute kill rate by topic
    topics = context["bill_topics_in_dataset"]
    bill_lookup = {b["bill"]: b for b in bills["bills"]}
    topic_stats = {}
    for cat, titles in topics.items():
        matched = [b for b in bills["bills"] if b["title"] in titles]
        if not matched:
            continue
        opposed = [b for b in matched if b["ia_position"] == "OPP"]
        killed = [b for b in opposed if b["status"] == "failed"]
        total_opp = len(opposed)
        if total_opp == 0:
            continue
        rate = len(killed) / total_opp * 100
        label = cat.replace("_", " ").title()
        topic_stats[label] = {"rate": rate, "killed": len(killed), "total": total_opp}

    sorted_topics = sorted(topic_stats.items(), key=lambda x: -x[1]["rate"])
    n = len(sorted_topics)
    row_h = (H - pad["t"] - pad["b"]) // max(n, 1)

    frames = []
    for fi in range(30):
        progress = min(fi / 18, 1.0)
        img = Image.new("RGB", (W, H), BLACK)
        d = ImageDraw.Draw(img)

        for i, (label, stats) in enumerate(sorted_topics):
            y = pad["t"] + i * row_h + row_h // 2
            rate = stats["rate"] * progress
            x_end = pad["l"] + int(pw * rate / 100)

            # Label
            draw_text(d, (10, y - 6), label, fill=WHITE)

            # Stem line
            d.line([(pad["l"], y), (x_end, y)], fill=DRED, width=2)

            # Lollipop circle
            r = 8
            color = RED if stats["rate"] >= 80 else AMBER if stats["rate"] >= 50 else GREEN
            d.ellipse([x_end - r, y - r, x_end + r, y + r], fill=color)

            # Value label
            if progress >= 0.9:
                draw_text(d, (x_end + 14, y - 7),
                          f"{stats['rate']:.0f}% ({stats['killed']}/{stats['total']})",
                          fill=AMBER)

        # Baseline
        d.line([(pad["l"], pad["t"]), (pad["l"], H - pad["b"])], fill=DIM, width=1)

        # Percentage grid
        for pct in [25, 50, 75, 100]:
            x = pad["l"] + int(pw * pct / 100)
            d.line([(x, pad["t"]), (x, H - pad["b"])], fill=GRID)
            draw_text(d, (x - 10, H - pad["b"] + 5), f"{pct}%", fill=DIM)

        frames.append(img)

    frames[0].save("assets/lollipop_kill_rate.gif", save_all=True,
                   append_images=frames[1:], duration=90, loop=0)
    print("  ✓ lollipop_kill_rate.gif")

make_lollipop_chart_gif()


# ═══════════════════════════════════════
# 3. DONUT CHART — bill outcomes breakdown
# ═══════════════════════════════════════
def make_donut_chart_gif():
    W, H = 600, 500
    cx, cy = 250, 260
    outer_r = 180
    inner_r = 100

    summary = bills["summary"]
    # Segments: opposed+killed, opposed+survived, supported+enacted, supported+failed
    opp_bills = [b for b in bills["bills"] if b["ia_position"] == "OPP"]
    prop_bills = [b for b in bills["bills"] if b["ia_position"] == "PROP"]
    segments = [
        ("Opposed & Killed", len([b for b in opp_bills if b["status"] == "failed"]), RED),
        ("Opposed & Survived", len([b for b in opp_bills if b["status"] == "enacted"]), (180, 80, 0)),
        ("Supported & Enacted", len([b for b in prop_bills if b["status"] == "enacted"]), GREEN),
        ("Supported & Failed", len([b for b in prop_bills if b["status"] == "failed"]), DIM),
    ]
    total = sum(s[1] for s in segments)

    frames = []
    for fi in range(35):
        progress = min(fi / 22, 1.0)
        img = Image.new("RGB", (W, H), BLACK)
        d = ImageDraw.Draw(img)

        # Glow
        for g in range(25, 0, -2):
            a = int(6 * g / 25)
            d.ellipse([cx - outer_r - g, cy - outer_r - g,
                       cx + outer_r + g, cy + outer_r + g], fill=(a, 0, 0))

        sweep_total = 360 * progress
        start = -90
        for label, count, color in segments:
            if count == 0:
                continue
            frac = count / total
            sweep = frac * sweep_total
            end = start + sweep
            if sweep > 0.5:
                d.pieslice([cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r],
                           start, end, fill=color, outline=(20, 20, 20))
            start = end

        # Inner circle (donut hole)
        d.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r], fill=BLACK)

        # Center text
        if progress >= 0.9:
            draw_text(d, (cx - 20, cy - 15), f"{summary['alignment_rate_percent']}%", fill=RED)
            draw_text(d, (cx - 25, cy + 2), "IA aligned", fill=DIM)

        # Legend
        ly = 50
        for label, count, color in segments:
            d.rectangle([430, ly, 444, ly + 12], fill=color)
            draw_text(d, (450, ly - 1), f"{label}: {count}", fill=WHITE)
            ly += 26

        frames.append(img)

    frames[0].save("assets/donut_outcomes.gif", save_all=True,
                   append_images=frames[1:], duration=90, loop=0)
    print("  ✓ donut_outcomes.gif")

make_donut_chart_gif()


# ═══════════════════════════════════════
# 4. SLOPE CHART — lobbyists vs spending trajectory
# ═══════════════════════════════════════
def make_slope_chart_gif():
    W, H = 800, 500
    pad = {"l": 80, "r": 80, "t": 60, "b": 60}
    pw = W - pad["l"] - pad["r"]
    ph = H - pad["t"] - pad["b"]

    data = lobbying["annual_spending"]
    years = [d["year"] for d in data]
    amounts = [d["amount"] / 1e6 for d in data]
    lobbyists = [d["lobbyists"] for d in data]
    max_amt = max(amounts) * 1.15
    max_lob = max(lobbyists) * 1.15

    frames = []
    for fi in range(30):
        progress = min(fi / 18, 1.0)
        img = Image.new("RGB", (W, H), BLACK)
        d = ImageDraw.Draw(img)

        # Grid
        for i in range(5):
            y = pad["t"] + int(ph * i / 4)
            d.line([(pad["l"], y), (W - pad["r"], y)], fill=GRID)

        xs = [pad["l"] + int(pw * i / (len(years) - 1)) for i in range(len(years))]

        # Spending line (red)
        pts_amt = []
        for i, v in enumerate(amounts):
            y = pad["t"] + ph - int(ph * v * progress / max_amt)
            pts_amt.append((xs[i], y))

        # Lobbyist line (amber)
        pts_lob = []
        for i, v in enumerate(lobbyists):
            y = pad["t"] + ph - int(ph * v * progress / max_lob)
            pts_lob.append((xs[i], y))

        # Draw lines
        for j in range(len(pts_amt) - 1):
            d.line([pts_amt[j], pts_amt[j + 1]], fill=RED, width=3)
            d.line([pts_lob[j], pts_lob[j + 1]], fill=AMBER, width=3)

        # Dots
        for p in pts_amt:
            d.ellipse([p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5], fill=RED)
        for p in pts_lob:
            d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=AMBER)

        # Year labels
        for i, y in enumerate(years):
            draw_text(d, (xs[i] - 12, pad["t"] + ph + 10), str(y), fill=DIM)

        # Value labels at peak
        if progress >= 0.95:
            peak_i = amounts.index(max(amounts))
            draw_text(d, (pts_amt[peak_i][0] - 20, pts_amt[peak_i][1] - 18),
                      f"${max(amounts):.1f}M", fill=RED)
            peak_l = lobbyists.index(max(lobbyists))
            draw_text(d, (pts_lob[peak_l][0] + 8, pts_lob[peak_l][1] - 5),
                      f"{max(lobbyists)}", fill=AMBER)

        # Legend
        d.rectangle([pad["l"] + 10, pad["t"] - 25, pad["l"] + 22, pad["t"] - 15], fill=RED)
        draw_text(d, (pad["l"] + 26, pad["t"] - 27), "Spending ($M)", fill=RED)
        d.rectangle([pad["l"] + 160, pad["t"] - 25, pad["l"] + 172, pad["t"] - 15], fill=AMBER)
        draw_text(d, (pad["l"] + 176, pad["t"] - 27), "Lobbyists", fill=AMBER)

        # Axis labels
        draw_text(d, (5, pad["t"]), "$M", fill=RED)
        draw_text(d, (W - pad["r"] + 10, pad["t"]), "# Lob", fill=AMBER)

        frames.append(img)

    frames[0].save("assets/slope_chart_trajectory.gif", save_all=True,
                   append_images=frames[1:], duration=90, loop=0)
    print("  ✓ slope_chart_trajectory.gif")

make_slope_chart_gif()


# ═══════════════════════════════════════
# 5. HEATMAP GRID — bills by session × topic
# ═══════════════════════════════════════
def make_heatmap_gif():
    W, H = 900, 480
    pad = {"l": 160, "r": 30, "t": 70, "b": 30}

    topics = context["bill_topics_in_dataset"]
    sessions = sorted(set(b["session"] for b in bills["bills"]))
    cat_labels = [c.replace("_", " ").title() for c in topics.keys()]
    cat_keys = list(topics.keys())

    # Build grid: count of opposed bills per session × topic
    grid = []
    for cat_key in cat_keys:
        row = []
        titles = topics[cat_key]
        for sess in sessions:
            count = len([b for b in bills["bills"]
                         if b["title"] in titles and b["session"] == sess
                         and b["ia_position"] == "OPP"])
            row.append(count)
        grid.append(row)

    max_val = max(max(row) for row in grid) if grid else 1
    n_rows = len(cat_labels)
    n_cols = len(sessions)
    cell_w = (W - pad["l"] - pad["r"]) // max(n_cols, 1)
    cell_h = (H - pad["t"] - pad["b"]) // max(n_rows, 1)

    frames = []
    for fi in range(25):
        progress = min(fi / 15, 1.0)
        img = Image.new("RGB", (W, H), BLACK)
        d = ImageDraw.Draw(img)

        # Column headers
        for j, sess in enumerate(sessions):
            x = pad["l"] + j * cell_w + cell_w // 2 - 20
            draw_text(d, (x, pad["t"] - 20), sess, fill=DIM)

        # Rows
        for i, label in enumerate(cat_labels):
            y = pad["t"] + i * cell_h
            draw_text(d, (5, y + cell_h // 2 - 5), label, fill=WHITE)

            for j in range(n_cols):
                x = pad["l"] + j * cell_w
                val = grid[i][j]
                intensity = val / max_val * progress if max_val > 0 else 0

                # Color: black → dark red → bright red
                r_val = int(200 * intensity)
                g_val = int(20 * (1 - intensity))
                fill_color = (r_val, g_val, 0)

                d.rectangle([x + 2, y + 2, x + cell_w - 2, y + cell_h - 2],
                            fill=fill_color, outline=(40, 40, 40))

                if progress >= 0.9 and val > 0:
                    draw_text(d, (x + cell_w // 2 - 3, y + cell_h // 2 - 5),
                              str(val), fill=WHITE)

        frames.append(img)

    frames[0].save("assets/heatmap_bills.gif", save_all=True,
                   append_images=frames[1:], duration=100, loop=0)
    print("  ✓ heatmap_bills.gif")

make_heatmap_gif()


# ═══════════════════════════════════════
# 6. TREEMAP — member companies by HQ state
# ═══════════════════════════════════════
def make_treemap_gif():
    W, H = 850, 520
    pad = 10

    hq = states["ia_member_hq_states"]
    # Flatten: list of (state, count)
    state_counts = sorted(hq.items(), key=lambda x: -len(x[1]))
    total = sum(len(v) for v in hq.values())

    # Simple treemap layout: squarified-ish rows
    rects = []
    colors_map = {
        "CA": (180, 0, 0), "WA": (140, 40, 0), "NY": (100, 60, 0),
        "TX": (0, 120, 60), "IL": (200, 0, 0), "TN": (80, 80, 0),
        "DC": (0, 80, 80), "MA": (60, 0, 100), "MN": (0, 60, 80),
        "CO": (40, 100, 40),
    }

    # Simple row-based layout
    x0, y0 = pad, pad
    avail_w = W - 2 * pad
    avail_h = H - 2 * pad
    remaining = total
    cur_y = y0

    for st, companies in state_counts:
        count = len(companies)
        frac = count / remaining if remaining > 0 else 0
        row_h = max(2, int(avail_h * frac))
        if cur_y + row_h > y0 + avail_h:
            row_h = max(2, y0 + avail_h - cur_y)
        remaining -= count

        color = colors_map.get(st, (80, 80, 80))
        if row_h >= 2:
            rects.append((x0, cur_y, avail_w, row_h, st, companies, color))
        cur_y += row_h

    frames = []
    for fi in range(25):
        progress = min(fi / 15, 1.0)
        img = Image.new("RGB", (W, H), BLACK)
        d = ImageDraw.Draw(img)

        for rx, ry, rw, rh, st, companies, color in rects:
            # Animate: grow from left
            cur_w = max(1, int(rw * progress))
            cur_h = max(1, rh)
            r, g, b = color
            d.rectangle([rx, ry, rx + cur_w, ry + cur_h - 1],
                        fill=(r, g, b), outline=(20, 20, 20))

            if progress >= 0.85 and cur_w > 40 and cur_h > 15:
                label = f"{st} ({len(companies)})"
                draw_text(d, (rx + 6, ry + 4), label, fill=WHITE)
                # Show company names if space allows
                if cur_h > 30:
                    comp_text = ", ".join(companies[:4])
                    if len(companies) > 4:
                        comp_text += f" +{len(companies)-4}"
                    draw_text(d, (rx + 6, ry + 18), comp_text, fill=(180, 180, 180))

        frames.append(img)

    frames[0].save("assets/treemap_members.gif", save_all=True,
                   append_images=frames[1:], duration=100, loop=0)
    print("  ✓ treemap_members.gif")

make_treemap_gif()


# ═══════════════════════════════════════
# 7. TIMELINE CHART — privacy milestones + IA events
# ═══════════════════════════════════════
def make_timeline_gif():
    W, H = 950, 450
    pad = {"l": 40, "r": 40, "t": 80, "b": 60}
    pw = W - pad["l"] - pad["r"]

    # Combine national milestones + IA key events
    events = []
    for m in context["national_milestones"]:
        yr = int(m["date"][:4])
        events.append((yr, m["event"][:40], "high" if m["relevance"] == "high" else "med", "nat"))
    for e in members["key_events"]:
        yr = int(e["date"][:4])
        events.append((yr, e["event"][:40], "ia", "ia"))

    events.sort(key=lambda x: x[0])
    min_yr = min(e[0] for e in events)
    max_yr = max(e[0] for e in events)
    yr_range = max_yr - min_yr if max_yr > min_yr else 1

    frames = []
    for fi in range(35):
        progress = min(fi / 22, 1.0)
        n_show = int(len(events) * progress)
        img = Image.new("RGB", (W, H), BLACK)
        d = ImageDraw.Draw(img)

        # Main timeline line
        line_y = H // 2
        d.line([(pad["l"], line_y), (W - pad["r"], line_y)], fill=DIM, width=2)

        # Year markers
        for yr in range(min_yr, max_yr + 1, 2):
            x = pad["l"] + int(pw * (yr - min_yr) / yr_range)
            d.line([(x, line_y - 5), (x, line_y + 5)], fill=DIM, width=1)
            draw_text(d, (x - 12, line_y + 10), str(yr), fill=DIM)

        # Events
        for idx in range(n_show):
            yr, label, rel, src = events[idx]
            x = pad["l"] + int(pw * (yr - min_yr) / yr_range)
            above = idx % 2 == 0

            if src == "ia":
                color = AMBER
                dot_r = 6
            elif rel == "high":
                color = RED
                dot_r = 5
            else:
                color = DIM
                dot_r = 4

            # Stem
            stem_len = 40 + (idx % 3) * 15
            if above:
                d.line([(x, line_y), (x, line_y - stem_len)], fill=color, width=1)
                draw_text(d, (x - 2, line_y - stem_len - 14), label[:25], fill=color)
            else:
                d.line([(x, line_y), (x, line_y + stem_len)], fill=color, width=1)
                draw_text(d, (x - 2, line_y + stem_len + 4), label[:25], fill=color)

            # Dot on timeline
            d.ellipse([x - dot_r, line_y - dot_r, x + dot_r, line_y + dot_r], fill=color)

        # Legend
        d.ellipse([pad["l"], pad["t"] - 40, pad["l"] + 8, pad["t"] - 32], fill=RED)
        draw_text(d, (pad["l"] + 12, pad["t"] - 42), "National milestone", fill=RED)
        d.ellipse([pad["l"] + 180, pad["t"] - 40, pad["l"] + 188, pad["t"] - 32], fill=AMBER)
        draw_text(d, (pad["l"] + 192, pad["t"] - 42), "IA event", fill=AMBER)

        frames.append(img)

    frames[0].save("assets/timeline_milestones.gif", save_all=True,
                   append_images=frames[1:], duration=100, loop=0)
    print("  ✓ timeline_milestones.gif")

make_timeline_gif()


# ═══════════════════════════════════════
# 8. STACKED BAR — bills by session (opposed vs supported, failed vs enacted)
# ═══════════════════════════════════════
def make_stacked_bar_gif():
    W, H = 800, 480
    pad = {"l": 80, "r": 40, "t": 50, "b": 60}
    pw = W - pad["l"] - pad["r"]
    ph = H - pad["t"] - pad["b"]

    sessions = sorted(set(b["session"] for b in bills["bills"]))
    # Per session: opp_killed, opp_survived, prop_enacted, prop_failed
    session_data = []
    for sess in sessions:
        sb = [b for b in bills["bills"] if b["session"] == sess]
        opp_k = len([b for b in sb if b["ia_position"] == "OPP" and b["status"] == "failed"])
        opp_s = len([b for b in sb if b["ia_position"] == "OPP" and b["status"] == "enacted"])
        pro_e = len([b for b in sb if b["ia_position"] == "PROP" and b["status"] == "enacted"])
        pro_f = len([b for b in sb if b["ia_position"] == "PROP" and b["status"] == "failed"])
        session_data.append((opp_k, opp_s, pro_e, pro_f))

    max_total = max(sum(sd) for sd in session_data) if session_data else 1
    n = len(sessions)
    bar_w = pw // n - 12

    seg_colors = [RED, (180, 80, 0), GREEN, DIM]
    seg_labels = ["Opposed & Killed", "Opposed & Survived", "Supported & Enacted", "Supported & Failed"]

    frames = []
    for fi in range(28):
        progress = min(fi / 18, 1.0)
        img = Image.new("RGB", (W, H), BLACK)
        d = ImageDraw.Draw(img)

        # Grid
        for i in range(5):
            y = pad["t"] + int(ph * i / 4)
            d.line([(pad["l"], y), (W - pad["r"], y)], fill=GRID)

        for i, (sess, sd) in enumerate(zip(sessions, session_data)):
            x = pad["l"] + i * (pw // n) + 6
            cur_y = pad["t"] + ph  # bottom

            for seg_idx, count in enumerate(sd):
                if count == 0:
                    continue
                seg_h = int(ph * count / max_total * progress)
                d.rectangle([x, cur_y - seg_h, x + bar_w, cur_y],
                            fill=seg_colors[seg_idx], outline=(20, 20, 20))
                if progress >= 0.9 and seg_h > 12:
                    draw_text(d, (x + bar_w // 2 - 3, cur_y - seg_h + 2),
                              str(count), fill=WHITE)
                cur_y -= seg_h

            # Session label
            draw_text(d, (x, pad["t"] + ph + 10), sess, fill=DIM)

        # Legend
        lx = pad["l"]
        for idx, (label, color) in enumerate(zip(seg_labels, seg_colors)):
            d.rectangle([lx, pad["t"] - 20, lx + 10, pad["t"] - 10], fill=color)
            draw_text(d, (lx + 14, pad["t"] - 22), label, fill=WHITE)
            lx += 170

        frames.append(img)

    frames[0].save("assets/stacked_bar_sessions.gif", save_all=True,
                   append_images=frames[1:], duration=90, loop=0)
    print("  ✓ stacked_bar_sessions.gif")

make_stacked_bar_gif()


print("\n✓ All chart assets generated!")
