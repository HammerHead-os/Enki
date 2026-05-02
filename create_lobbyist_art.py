#!/usr/bin/env python3
"""Generate the lobbyist meeting scene + devil reveal version."""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 800, 500
BG = (18, 18, 30)
TABLE = (40, 35, 55)
SUIT = (50, 50, 70)
SKIN = (220, 190, 160)
HAIR = (60, 45, 35)
WHITE_SHIRT = (200, 200, 210)
RED = (230, 57, 70)
DEVIL_RED = (180, 20, 20)
DARK = (25, 20, 35)
GLOW = (255, 80, 60)

def draw_person(d, cx, cy, facing_right=True, is_speaker=False, devil=False):
    """Draw a simple stylized person at position."""
    # Body
    body_color = DEVIL_RED if devil else SUIT
    skin_color = (200, 80, 60) if devil else SKIN
    
    # Torso
    d.rounded_rectangle([cx-18, cy+10, cx+18, cy+55], radius=6, fill=body_color)
    # Shirt collar
    d.polygon([(cx-8, cy+10), (cx, cy+18), (cx+8, cy+10)], fill=WHITE_SHIRT if not devil else (100, 20, 20))
    
    # Head
    d.ellipse([cx-14, cy-20, cx+14, cy+12], fill=skin_color)
    # Hair
    hair_color = (150, 30, 20) if devil else HAIR
    d.ellipse([cx-15, cy-22, cx+15, cy-4], fill=hair_color)
    
    # Eyes
    ex = 5 if facing_right else -5
    d.ellipse([cx+ex-3, cy-8, cx+ex+3, cy-2], fill=(255,255,255))
    d.ellipse([cx+ex-1, cy-7, cx+ex+1, cy-3], fill=(20,20,30) if not devil else RED)
    
    # Devil horns
    if devil:
        d.polygon([(cx-12, cy-18), (cx-8, cy-38), (cx-4, cy-16)], fill=RED)
        d.polygon([(cx+4, cy-16), (cx+8, cy-38), (cx+12, cy-18)], fill=RED)
        # Tail (from behind)
        points = []
        for t in range(20):
            tt = t / 19
            tx = cx + 20 + math.sin(tt * 3) * 12
            ty = cy + 55 - tt * 30
            points.append((tx, ty))
        if len(points) > 1:
            d.line(points, fill=RED, width=3)
        # Arrow tip
        if len(points) > 1:
            lx, ly = points[-1]
            d.polygon([(lx-5, ly-2), (lx+5, ly-2), (lx, ly-10)], fill=RED)
    
    # Arms
    if is_speaker:
        # Raised arm pointing
        d.line([(cx+18, cy+20), (cx+40, cy-5)], fill=body_color, width=6)
        d.ellipse([cx+36, cy-10, cx+44, cy-2], fill=skin_color)
        # Other arm gesturing
        d.line([(cx-18, cy+20), (cx-35, cy+5)], fill=body_color, width=6)
        d.ellipse([cx-39, cy+1, cx-31, cy+9], fill=skin_color)
    else:
        # Arms on table
        arm_dir = 1 if facing_right else -1
        d.line([(cx+arm_dir*18, cy+25), (cx+arm_dir*30, cy+40)], fill=body_color, width=5)

def draw_scene(devil_mode=False):
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    
    # Conference table (oval)
    d.ellipse([150, 250, 650, 420], fill=TABLE, outline=(60, 55, 75))
    # Table shine
    d.ellipse([200, 270, 600, 380], fill=(50, 45, 65))
    
    # Documents on table
    for dx, dy in [(300, 310), (350, 330), (420, 300), (480, 325)]:
        d.rectangle([dx, dy, dx+30, dy+20], fill=(180, 180, 190), outline=(140, 140, 150))
        for line_y in range(dy+4, dy+18, 4):
            d.line([(dx+3, line_y), (dx+27, line_y)], fill=(120, 120, 130))
    
    # Laptop
    d.rectangle([370, 285, 420, 310], fill=(60, 60, 80), outline=(80, 80, 100))
    d.rectangle([372, 287, 418, 308], fill=(100, 140, 180))
    
    # People sitting around table (audience)
    positions = [
        (220, 200, True),   # left side
        (300, 180, True),   # left-center
        (500, 180, False),  # right-center  
        (580, 200, False),  # right side
        (260, 380, True),   # bottom-left
        (540, 380, False),  # bottom-right
    ]
    
    for px, py, facing in positions:
        draw_person(d, px, py, facing, is_speaker=False, devil=False)
    
    # Speaker (standing, at the top-center)
    speaker_x, speaker_y = 400, 130
    draw_person(d, speaker_x, speaker_y, True, is_speaker=True, devil=devil_mode)
    
    # Whiteboard behind speaker
    d.rectangle([320, 40, 480, 120], fill=(240, 240, 245), outline=(200, 200, 210))
    # Chart lines on whiteboard
    d.line([(340, 100), (360, 80), (380, 90), (400, 60), (420, 70), (440, 50), (460, 55)], 
           fill=RED if devil_mode else (100, 100, 200), width=2)
    # Text on whiteboard
    d.text((335, 45), "PRIVACY", fill=(80, 80, 100))
    d.text((335, 58), "BILLS", fill=(80, 80, 100))
    
    if devil_mode:
        # Add evil glow around speaker
        for r in range(40, 0, -2):
            alpha_img = Image.new('RGB', (W, H), BG)
            alpha_d = ImageDraw.Draw(alpha_img)
            glow_color = (min(255, 30 + r*2), max(0, 20 - r), max(0, 20 - r))
            alpha_d.ellipse([speaker_x-r-30, speaker_y-r-30, speaker_x+r+30, speaker_y+r+80], 
                          fill=glow_color)
        
        # Red tint overlay on whiteboard
        d.rectangle([320, 40, 480, 120], fill=None, outline=RED, width=2)
        # "KILL" text
        d.text((390, 45), "KILL", fill=RED)
        d.text((390, 58), "LIST", fill=RED)
        
        # Flames at bottom
        for fx in range(0, W, 30):
            fh = 20 + (fx * 7 % 30)
            d.polygon([(fx, H), (fx+15, H-fh), (fx+30, H)], fill=(80, 15, 5))
            d.polygon([(fx+5, H), (fx+15, H-fh+8), (fx+25, H)], fill=(120, 25, 10))
    
    return img

# Generate both versions
normal = draw_scene(devil_mode=False)
normal.save('assets/lobbyist_normal.png')
print('✓ lobbyist_normal.png')

devil = draw_scene(devil_mode=True)
devil.save('assets/lobbyist_devil.png')
print('✓ lobbyist_devil.png')
