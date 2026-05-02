import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random
import math

# Load image
img_cv = cv2.imread("source_photo.png")
if img_cv is None:
    # Try jpg
    img_cv = cv2.imread("source_photo.jpg")

gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

# Detect faces
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
print(f"Detected {len(faces)} faces")

# Convert to PIL
img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
base_img = Image.fromarray(img_rgb).convert("RGBA")
W, H = base_img.size

def draw_x_eye(draw, cx, cy, size, color, thickness=3, jitter=0):
    """Draw a glitchy X over an eye position"""
    jx = random.randint(-jitter, jitter)
    jy = random.randint(-jitter, jitter)
    half = size // 2
    # Draw X with multiple offset lines for glitch effect
    for t in range(-thickness, thickness + 1):
        draw.line([(cx - half + jx + t, cy - half + jy), (cx + half + jx + t, cy + half + jy)], fill=color, width=2)
        draw.line([(cx + half + jx + t, cy - half + jy), (cx - half + jx + t, cy + half + jy)], fill=color, width=2)

def draw_devil_horns(draw, fx, fy, fw, fh):
    """Draw devil horns above a face"""
    horn_h = int(fh * 0.55)
    horn_w = int(fw * 0.18)
    
    # Left horn
    lx = fx + int(fw * 0.15)
    ly = fy - int(fh * 0.05)
    left_horn = [
        (lx, ly),
        (lx - horn_w, ly - horn_h),
        (lx + horn_w, ly),
    ]
    draw.polygon(left_horn, fill=(180, 0, 0, 240))
    # Inner highlight
    inner_left = [
        (lx, ly - 2),
        (lx - horn_w + 4, ly - horn_h + 8),
        (lx + horn_w - 6, ly - 2),
    ]
    draw.polygon(inner_left, fill=(220, 30, 0, 200))
    
    # Right horn
    rx = fx + int(fw * 0.85)
    ry = fy - int(fh * 0.05)
    right_horn = [
        (rx, ry),
        (rx + horn_w, ry - horn_h),
        (rx - horn_w, ry),
    ]
    draw.polygon(right_horn, fill=(180, 0, 0, 240))
    inner_right = [
        (rx, ry - 2),
        (rx + horn_w - 4, ry - horn_h + 8),
        (rx - horn_w + 6, ry - 2),
    ]
    draw.polygon(inner_right, fill=(220, 30, 0, 200))

def add_glitch_slice(img, intensity=10):
    """Add horizontal glitch slices to the image"""
    arr = np.array(img)
    h, w = arr.shape[:2]
    num_slices = random.randint(3, 8)
    for _ in range(num_slices):
        y = random.randint(0, h - 10)
        slice_h = random.randint(2, 15)
        shift = random.randint(-intensity, intensity)
        if y + slice_h < h:
            arr[y:y+slice_h] = np.roll(arr[y:y+slice_h], shift, axis=1)
    return Image.fromarray(arr)

def add_red_channel_shift(img, shift=5):
    """Shift the red channel for chromatic aberration"""
    arr = np.array(img)
    shifted = arr.copy()
    sx = random.randint(-shift, shift)
    sy = random.randint(-shift, shift)
    shifted[:, :, 0] = np.roll(np.roll(arr[:, :, 0], sx, axis=1), sy, axis=0)
    return Image.fromarray(shifted)

def add_scanlines(img, opacity=60):
    """Add CRT-style scanlines"""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(0, img.size[1], 3):
        draw.line([(0, y), (img.size[0], y)], fill=(0, 0, 0, opacity), width=1)
    return Image.alpha_composite(img, overlay)

def add_vignette(img, strength=0.7):
    """Add dark vignette around edges"""
    arr = np.array(img).astype(float)
    h, w = arr.shape[:2]
    Y, X = np.ogrid[:h, :w]
    cx, cy = w / 2, h / 2
    dist = np.sqrt((X - cx)**2 + (Y - cy)**2)
    max_dist = np.sqrt(cx**2 + cy**2)
    vignette = 1 - strength * (dist / max_dist) ** 2
    vignette = np.clip(vignette, 0, 1)
    for c in range(3):
        arr[:, :, c] *= vignette
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

# Build eye positions for each face
face_data = []
for (fx, fy, fw, fh) in faces:
    # Estimate eye positions within face region
    left_eye = (fx + int(fw * 0.3), fy + int(fh * 0.38))
    right_eye = (fx + int(fw * 0.7), fy + int(fh * 0.38))
    eye_size = max(int(fw * 0.15), 8)
    face_data.append({
        'rect': (fx, fy, fw, fh),
        'left_eye': left_eye,
        'right_eye': right_eye,
        'eye_size': eye_size
    })

print(f"Processing {len(face_data)} faces with eye positions")

# Generate frames
NUM_FRAMES = 24
frames = []

for frame_idx in range(NUM_FRAMES):
    # Start with base image
    frame = base_img.copy()
    
    # Darken the image with a red/dark tint
    tint = Image.new("RGBA", frame.size, (20, 0, 0, 80))
    frame = Image.alpha_composite(frame, tint)
    
    overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Flicker intensity varies per frame
    flicker = random.random()
    
    for fd in face_data:
        fx, fy, fw, fh = fd['rect']
        lex, ley = fd['left_eye']
        rex, rey = fd['right_eye']
        eye_sz = fd['eye_size']
        
        # Draw devil horns (with slight jitter)
        jx = random.randint(-2, 2)
        jy = random.randint(-2, 2)
        draw_devil_horns(draw, fx + jx, fy + jy, fw, fh)
        
        # Draw X eyes with glitch jitter
        jitter = random.randint(0, 4)
        
        # Alternate colors for creepiness
        if frame_idx % 3 == 0:
            eye_color = (255, 0, 0, 255)  # Red
        elif frame_idx % 3 == 1:
            eye_color = (255, 255, 255, 255)  # White
        else:
            eye_color = (200, 0, 0, 230)  # Dark red
        
        thickness = random.randint(2, 5)
        draw_x_eye(draw, lex, ley, eye_sz, eye_color, thickness, jitter)
        draw_x_eye(draw, rex, rey, eye_sz, eye_color, thickness, jitter)
        
        # Add glow around X eyes
        glow_color = (255, 0, 0, 40)
        for g in range(3):
            draw_x_eye(draw, lex, ley, eye_sz + g * 4, glow_color, 1, jitter + g)
            draw_x_eye(draw, rex, rey, eye_sz + g * 4, glow_color, 1, jitter + g)
    
    frame = Image.alpha_composite(frame, overlay)
    
    # Apply glitch effects (more intense on some frames)
    if random.random() > 0.3:
        intensity = random.choice([5, 10, 20, 30])
        frame = add_glitch_slice(frame, intensity)
    
    # Chromatic aberration
    if random.random() > 0.4:
        frame = add_red_channel_shift(frame, shift=random.randint(2, 8))
    
    # Scanlines
    frame = add_scanlines(frame, opacity=random.randint(30, 80))
    
    # Vignette
    frame = add_vignette(frame, strength=random.uniform(0.5, 0.8))
    
    # Random brightness flicker
    if random.random() > 0.7:
        dark = Image.new("RGBA", frame.size, (0, 0, 0, random.randint(30, 100)))
        frame = Image.alpha_composite(frame, dark)
    
    # Occasional heavy red flash
    if frame_idx % 8 == 0:
        red_flash = Image.new("RGBA", frame.size, (150, 0, 0, 60))
        frame = Image.alpha_composite(frame, red_flash)
    
    frames.append(frame.convert("RGB"))
    print(f"  Frame {frame_idx + 1}/{NUM_FRAMES}")

# Add some duplicate frames with heavy glitch for stutter effect
final_frames = []
for i, f in enumerate(frames):
    final_frames.append(f)
    # Randomly stutter
    if random.random() > 0.7:
        glitched = add_glitch_slice(f.convert("RGBA"), 40)
        final_frames.append(glitched.convert("RGB"))

# Save as GIF
durations = [random.choice([80, 100, 120, 150]) for _ in final_frames]
# Make some frames flash faster
for i in range(len(durations)):
    if random.random() > 0.8:
        durations[i] = 40  # Quick flash

final_frames[0].save(
    "assets/creepy_censored.gif",
    save_all=True,
    append_images=final_frames[1:],
    duration=durations,
    loop=0,
    optimize=False
)

print(f"\nDone! Saved creepy_censored.gif with {len(final_frames)} frames")
