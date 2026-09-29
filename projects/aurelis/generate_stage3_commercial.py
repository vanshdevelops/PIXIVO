#!/usr/bin/env python3
"""
STAGE 3.3 — AURELIS AI COMMERCIAL FILM
Production Asset Generation & Video Rendering Engine
Generates:
1. High-resolution shot stills (9:16, 16:9, 4:5)
2. Posters (16:9, 9:16)
3. Master Storyboard Board (2400x1500)
4. Animated WebP previews (16:9, 9:16)
5. Bespoke 48kHz stereo luxury audio track
6. REAL 12-second H.264 MP4 commercial film (16:9 1080p master & 9:16 vertical)
"""

import os
import sys
import math
import subprocess
import wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# Locate and verify FFmpeg binary early
def locate_and_verify_ffmpeg():
    """
    Early dependency verification for FFmpeg.
    Checks system PATH, imageio_ffmpeg fallback, and verifies executability.
    Stops execution early with a clear error if FFmpeg is unavailable.
    """
    import shutil
    candidates = []
    
    # Check system PATH
    sys_ffmpeg = shutil.which("ffmpeg")
    if sys_ffmpeg:
        candidates.append(("system PATH", sys_ffmpeg))
        
    # Check imageio_ffmpeg fallback
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe:
            candidates.append(("imageio_ffmpeg", exe))
    except Exception:
        pass
        
    # Check bare 'ffmpeg' command
    candidates.append(("ffmpeg command", "ffmpeg"))
    
    for source, exe_path in candidates:
        try:
            res = subprocess.run([exe_path, "-version"], capture_output=True, text=True, check=False)
            if res.returncode == 0:
                print(f"[FFmpeg Check] Verified FFmpeg binary ({source}): {exe_path}")
                return exe_path
        except (FileNotFoundError, PermissionError, OSError):
            continue
            
    print("\n" + "="*70, file=sys.stderr)
    print("FATAL ERROR: FFmpeg executable could not be found or executed!", file=sys.stderr)
    print("Stage 3.3 requires FFmpeg to compile the H.264/AVC 1080p commercial video.", file=sys.stderr)
    print("Please install FFmpeg on your system or install imageio-ffmpeg.", file=sys.stderr)
    print("="*70 + "\n", file=sys.stderr)
    sys.exit(1)

FFMPEG_BIN = locate_and_verify_ffmpeg()

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(BASE_DIR, "assets", "video")
SHOTS_DIR = os.path.join(VIDEO_DIR, "shots")
POSTERS_DIR = os.path.join(VIDEO_DIR, "posters")
MASTERS_DIR = os.path.join(VIDEO_DIR, "masters")
PREVIEWS_DIR = os.path.join(VIDEO_DIR, "previews")
AUDIO_DIR = os.path.join(VIDEO_DIR, "audio")
FINAL_DIR = os.path.join(VIDEO_DIR, "final")

for d in [
    os.path.join(SHOTS_DIR, "shot-01"),
    os.path.join(SHOTS_DIR, "shot-02"),
    os.path.join(SHOTS_DIR, "shot-03"),
    os.path.join(SHOTS_DIR, "shot-04"),
    POSTERS_DIR,
    MASTERS_DIR,
    PREVIEWS_DIR,
    AUDIO_DIR,
    FINAL_DIR
]:
    os.makedirs(d, exist_ok=True)

# Reference Masters
REF_HERO = os.path.join(BASE_DIR, "assets", "photography", "campaign-master", "aurelis-noir-eclat-campaign-master.webp")
REF_FRONT = os.path.join(BASE_DIR, "assets", "product-master", "aurelis-noir-eclat-front-master.webp")
REF_CINEMATIC = os.path.join(BASE_DIR, "assets", "photography", "cinematic", "aurelis-noir-eclat-dark-cinematic.webp")
REF_AMBER = os.path.join(BASE_DIR, "assets", "photography", "amber", "aurelis-noir-eclat-warm-amber.webp")

# Typography fonts
FONT_SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
FONT_SANS = "/System/Library/Fonts/Helvetica.ttc"
if not os.path.exists(FONT_SERIF):
    FONT_SERIF = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"

def get_font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()

def draw_letterspaced_text(draw, center_x, y, text, font, fill, spacing=6):
    """Draw centered text with custom tracking."""
    total_w = 0
    char_widths = []
    for ch in text:
        bbox = draw.textbbox((0, 0), ch, font=font)
        w = bbox[2] - bbox[0]
        char_widths.append(w)
        total_w += w + spacing
    total_w -= spacing
    curr_x = center_x - total_w / 2
    for i, ch in enumerate(text):
        draw.text((curr_x, y), ch, font=font, fill=fill)
        curr_x += char_widths[i] + spacing

def create_gradient_radial(width, height, center, radius, color_inner, color_outer):
    """Create radial gradient overlay."""
    cx, cy = center
    x = np.linspace(0, width - 1, width)
    y = np.linspace(0, height - 1, height)
    xx, yy = np.meshgrid(x, y)
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    norm_dist = np.clip(dist / radius, 0.0, 1.0)
    
    r = (color_inner[0] * (1 - norm_dist) + color_outer[0] * norm_dist).astype(np.uint8)
    g = (color_inner[1] * (1 - norm_dist) + color_outer[1] * norm_dist).astype(np.uint8)
    b = (color_inner[2] * (1 - norm_dist) + color_outer[2] * norm_dist).astype(np.uint8)
    
    arr = np.stack([r, g, b], axis=-1)
    return Image.fromarray(arr, mode="RGB")

def fit_contain(img, target_w, target_h, scale_factor=0.85):
    """Fit image centered into target canvas preserving aspect ratio."""
    iw, ih = img.size
    ratio = min((target_w * scale_factor) / iw, (target_h * scale_factor) / ih)
    nw, nh = int(iw * ratio), int(ih * ratio)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    return resized

# -----------------------------------------------------------------------------
# SHOT BUILDERS (KEYFRAME STILLS)
# -----------------------------------------------------------------------------

def build_shot_01(w, h, light_offset=0.0):
    """Shot 01 — THE DARKNESS: Architectural obsidian void with champagne rim light."""
    canvas = Image.new("RGB", (w, h), (7, 7, 8))
    draw = ImageDraw.Draw(canvas)
    
    plinth_y = int(h * 0.72)
    draw.rectangle([0, plinth_y, w, h], fill=(12, 12, 14))
    draw.line([0, plinth_y, w, plinth_y], fill=(28, 27, 26), width=2)
    
    # Light beam with offset
    cx = int(w * (0.65 - light_offset * 0.15))
    cy = int(h * 0.5)
    light_grad = create_gradient_radial(
        w, h,
        center=(cx, cy),
        radius=int(max(w, h) * 0.6),
        color_inner=(38, 32, 25),
        color_outer=(7, 7, 8)
    )
    canvas = Image.blend(canvas, light_grad, 0.45)
    
    # Faint vertical edge reflection
    draw = ImageDraw.Draw(canvas)
    edge_x = int(w * (0.52 - light_offset * 0.05))
    for offset in range(-2, 3):
        draw.line([edge_x + offset, int(h * 0.35), edge_x + offset, plinth_y], fill=(45, 38, 28), width=1)
        
    return canvas

def build_shot_02(w, h, reveal_progress=1.0):
    """Shot 02 — THE REVEAL: NOIR ÉCLAT bottle emerging from shadow with light sweep."""
    canvas = build_shot_01(w, h, light_offset=0.5)
    
    ref_img = Image.open(REF_HERO).convert("RGBA")
    scaled_ref = fit_contain(ref_img, w, h, scale_factor=0.68)
    rw, rh = scaled_ref.size
    
    pos_x = (w - rw) // 2
    pos_y = int(h * 0.72) - rh + int(rh * 0.08)
    
    # Shadow mask for emergence modulated by reveal_progress
    shadow_mask = Image.new("L", (rw, rh), 0)
    for y in range(rh):
        for x in range(rw):
            factor = (x / rw * 0.7 + (1 - y / rh) * 0.5) * 1.3 - (1.0 - reveal_progress) * 0.8
            val = int(255 * min(1.0, max(0.0, factor)))
            shadow_mask.putpixel((x, y), val)
            
    revealed_bottle = scaled_ref.copy()
    r_a = revealed_bottle.split()[3]
    combined_a = Image.fromarray(np.minimum(np.array(r_a), np.array(shadow_mask)))
    revealed_bottle.putalpha(combined_a)
    
    canvas.paste(revealed_bottle, (pos_x, pos_y), revealed_bottle)
    
    # Amber caustic reflection on plinth
    draw = ImageDraw.Draw(canvas)
    refl_y = int(h * 0.72)
    refl_alpha = int(255 * min(1.0, reveal_progress))
    draw.ellipse([pos_x + int(rw * 0.2), refl_y - 8, pos_x + int(rw * 0.8), refl_y + int(h * 0.08)],
                 fill=(28, 20, 12))
    
    return canvas

def build_shot_03(w, h, pulse=0.0):
    """Shot 03 — THE HERO MOMENT: Fully revealed hero bottle in monumental majesty."""
    canvas = Image.new("RGB", (w, h), (8, 8, 10))
    
    inner_val = int(42 + pulse * 10)
    glow = create_gradient_radial(
        w, h,
        center=(int(w * 0.5), int(h * 0.48)),
        radius=int(max(w, h) * 0.55),
        color_inner=(inner_val, int(inner_val * 0.8), int(inner_val * 0.5)),
        color_outer=(8, 8, 10)
    )
    canvas = Image.blend(canvas, glow, 0.6)
    
    plinth_y = int(h * 0.74)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, plinth_y, w, h], fill=(13, 13, 16))
    draw.line([0, plinth_y, w, plinth_y], fill=(36, 32, 28), width=2)
    
    ref_img = Image.open(REF_HERO).convert("RGBA")
    scaled_ref = fit_contain(ref_img, w, h, scale_factor=0.72)
    rw, rh = scaled_ref.size
    pos_x = (w - rw) // 2
    pos_y = plinth_y - rh + int(rh * 0.06)
    
    # Reflection
    refl = scaled_ref.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    refl_alpha = np.array(refl.split()[3], dtype=np.float32)
    fade = np.linspace(0.25, 0.0, rh).reshape(-1, 1)
    new_alpha = Image.fromarray((refl_alpha * fade).astype(np.uint8))
    refl.putalpha(new_alpha)
    canvas.paste(refl, (pos_x, plinth_y + 2), refl)
    
    canvas.paste(scaled_ref, (pos_x, pos_y), scaled_ref)
    
    return canvas

def build_shot_04(w, h, text_alpha=1.0, halo_pulse=0.0):
    """Shot 04 — FINAL BRAND FRAME: Clean luxury print aesthetic with canonical typography."""
    canvas = Image.new("RGB", (w, h), (6, 6, 7))
    
    halo_inner = int(26 + halo_pulse * 8)
    halo = create_gradient_radial(
        w, h,
        center=(int(w * 0.5), int(h * 0.42)),
        radius=int(max(w, h) * 0.4),
        color_inner=(halo_inner, int(halo_inner * 0.8), int(halo_inner * 0.55)),
        color_outer=(6, 6, 7)
    )
    canvas = Image.blend(canvas, halo, 0.55)
    
    ref_img = Image.open(REF_HERO).convert("RGBA")
    scaled_ref = fit_contain(ref_img, w, h, scale_factor=0.48)
    rw, rh = scaled_ref.size
    pos_x = (w - rw) // 2
    pos_y = int(h * 0.22)
    canvas.paste(scaled_ref, (pos_x, pos_y), scaled_ref)
    
    draw = ImageDraw.Draw(canvas)
    
    title_size = max(18, int(min(w, h) * 0.045))
    sub_size = max(11, int(min(w, h) * 0.022))
    tag_size = max(9, int(min(w, h) * 0.016))
    
    font_brand = get_font(FONT_SERIF, title_size)
    font_product = get_font(FONT_SERIF, int(title_size * 0.75))
    font_sub = get_font(FONT_SANS, sub_size)
    font_tag = get_font(FONT_SERIF, tag_size)
    
    text_y = pos_y + rh + int(h * 0.04)
    
    c_brand = tuple(int(c * text_alpha) for c in (200, 169, 110))
    c_prod = tuple(int(c * text_alpha) for c in (240, 237, 230))
    c_sub = tuple(int(c * text_alpha) for c in (168, 162, 153))
    c_tag = tuple(int(c * text_alpha) for c in (140, 134, 125))
    c_div = tuple(int(c * text_alpha) for c in (64, 56, 42))
    
    draw_letterspaced_text(draw, w // 2, text_y, "A U R E L I S", font_brand, c_brand, spacing=title_size // 3)
    text_y += int(title_size * 1.5)
    draw_letterspaced_text(draw, w // 2, text_y, "NOIR ÉCLAT", font_product, c_prod, spacing=title_size // 4)
    text_y += int(sub_size * 1.8)
    draw_letterspaced_text(draw, w // 2, text_y, "THE ART OF SCENT", font_sub, c_sub, spacing=sub_size // 2)
    text_y += int(sub_size * 1.6)
    divider_w = int(w * 0.18)
    draw.line([w // 2 - divider_w // 2, text_y, w // 2 + divider_w // 2, text_y], fill=c_div, width=1)
    text_y += int(sub_size * 1.2)
    draw_letterspaced_text(draw, w // 2, text_y, "“Leave an impression without saying a word.”", font_tag, c_tag, spacing=2)
    
    return canvas

# -----------------------------------------------------------------------------
# MASTER STORYBOARD PRESENTATION BOARD (2400 × 1500)
# -----------------------------------------------------------------------------
def build_storyboard_board(shot_images):
    """Builds a 2400 × 1500 presentation board showcasing all 4 shots."""
    bw, bh = 2400, 1500
    board = Image.new("RGB", (bw, bh), (10, 10, 11))
    draw = ImageDraw.Draw(board)
    
    draw.rectangle([24, 24, bw - 25, bh - 25], outline=(36, 33, 28), width=1)
    draw.rectangle([28, 28, bw - 29, bh - 29], outline=(20, 19, 18), width=1)
    
    font_hdr_sub = get_font(FONT_SANS, 14)
    font_hdr_title = get_font(FONT_SERIF, 32)
    font_hdr_desc = get_font(FONT_SANS, 13)
    
    draw.text((64, 60), "STAGE 3.3 — AI-ASSISTED COMMERCIAL FILM PRODUCTION", font=font_hdr_sub, fill=(200, 169, 110))
    draw.text((64, 88), "AURELIS · NOIR ÉCLAT — CINEMATIC STORYBOARD", font=font_hdr_title, fill=(245, 242, 235))
    draw.text((64, 136), "12-SECOND LUXURY ADVERTISEMENT · MASTER TIME-CODED SHOT PROGRESSION", font=font_hdr_desc, fill=(140, 135, 126))
    
    meta_text = "CLIENT: SELF-INITIATED CONCEPT\nAGENCY: PIXIVO FLAGSHIP STUDIO\nPRIMARY: 9:16 VERTICAL & 16:9 1080P MASTER\nCOLOR: OBSIDIAN / CHAMPAGNE / AMBER"
    draw.multiline_text((bw - 420, 65), meta_text, font=font_hdr_sub, fill=(140, 135, 126), spacing=4)
    draw.line([64, 175, bw - 64, 175], fill=(42, 38, 32), width=1)
    
    card_w = 480
    card_h = 853  # 9:16
    start_y = 240
    gap = (bw - 128 - (card_w * 4)) // 3
    
    shot_meta = [
        {
            "num": "SHOT 01",
            "time": "00:00 — 00:03",
            "title": "THE DARKNESS",
            "camera": "Slow macro push-in (f/2.8, 85mm)",
            "lighting": "Low-key directional, edge silhouette",
            "audio": "Subtle 40Hz room drone, tactile stillness"
        },
        {
            "num": "SHOT 02",
            "time": "00:03 — 00:06",
            "title": "THE REVEAL",
            "camera": "Dynamic diagonal orbit (f/2.0, 50mm)",
            "lighting": "Warm champagne light sweep across bottle",
            "audio": "Soft metallic resonance, rising harmonic swell"
        },
        {
            "num": "SHOT 03",
            "time": "00:06 — 00:09",
            "title": "THE HERO MOMENT",
            "camera": "Monumental locked hero frame (f/4.0, 50mm)",
            "lighting": "Full chiaroscuro, amber caustic refraction",
            "audio": "Rich harmonic resolution, glass ring clarity"
        },
        {
            "num": "SHOT 04",
            "time": "00:09 — 00:12",
            "title": "FINAL BRAND FRAME",
            "camera": "Static locked editorial print frame",
            "lighting": "Subtle golden ambient halo",
            "audio": "Decaying warm reverb into quiet luxury"
        }
    ]
    
    font_card_num = get_font(FONT_SANS, 12)
    font_card_time = get_font(FONT_SANS, 12)
    font_card_title = get_font(FONT_SERIF, 18)
    font_spec = get_font(FONT_SANS, 11)
    
    for i, meta in enumerate(shot_meta):
        cx = 64 + i * (card_w + gap)
        draw.text((cx, start_y - 35), meta["num"], font=font_card_num, fill=(200, 169, 110))
        draw.text((cx + card_w - 95, start_y - 35), meta["time"], font=font_card_time, fill=(160, 155, 145))
        draw.rectangle([cx - 2, start_y - 2, cx + card_w + 1, start_y + card_h + 1], outline=(40, 36, 30), width=1)
        shot_img = shot_images[i].resize((card_w, card_h), Image.Resampling.LANCZOS)
        board.paste(shot_img, (cx, start_y))
        
        desc_y = start_y + card_h + 20
        draw.text((cx, desc_y), meta["title"], font=font_card_title, fill=(245, 242, 235))
        desc_y += 30
        draw.text((cx, desc_y), f"CAMERA: {meta['camera']}", font=font_spec, fill=(160, 155, 145))
        desc_y += 20
        draw.text((cx, desc_y), f"LIGHT:  {meta['lighting']}", font=font_spec, fill=(140, 135, 125))
        desc_y += 20
        draw.text((cx, desc_y), f"AUDIO:  {meta['audio']}", font=font_spec, fill=(200, 169, 110))
    
    draw.line([64, bh - 90, bw - 64, bh - 90], fill=(42, 38, 32), width=1)
    font_ftr = get_font(FONT_SANS, 12)
    draw.text((64, bh - 65), "AURELIS NOIR ÉCLAT · LUXURY FRAGRANCE CAMPAIGN SYSTEM · PIXIVO CREATIVE DIRECTION", font=font_ftr, fill=(140, 135, 126))
    draw.text((bw - 460, bh - 65), "AI-ASSISTED CONCEPT PRODUCTION · STRICT PRODUCT CONSISTENCY LOCKED", font=font_ftr, fill=(200, 169, 110))
    
    return board

# -----------------------------------------------------------------------------
# AUDIO SYNTHESIS (BESPOKE 48kHz STEREO LUXURY SOUNDSCAPE)
# -----------------------------------------------------------------------------
def synthesize_commercial_audio(duration=12.0, sr=48000):
    """
    Synthesizes a 12.0s luxury acoustic soundtrack in C minor:
    - 42Hz low-frequency room drone + warm analog body
    - 3.0s: soft brushed brass metallic ping & tactile glass click
    - 6.0s: low sub boom (50Hz damped) + warm C minor pad (C3, Eb3, G3, Bb3)
    - 9.0s: crystalline harmonic chime (E7 2637Hz) with reverb decay into silence
    """
    total_samples = int(duration * sr)
    t = np.linspace(0, duration, total_samples, endpoint=False)
    
    # 1. Sub-bass & atmospheric room drone (0 to 12s)
    drone = 0.22 * np.sin(2 * np.pi * 42.0 * t) + 0.12 * np.sin(2 * np.pi * 84.0 * t)
    # Slow LFO breathing
    lfo = 0.75 + 0.25 * np.sin(2 * np.pi * 0.18 * t)
    drone *= lfo
    
    # Fade in / out envelope for drone
    env_drone = np.ones_like(t)
    fade_in_len = int(0.8 * sr)
    env_drone[:fade_in_len] = np.linspace(0.0, 1.0, fade_in_len)
    fade_out_len = int(1.2 * sr)
    env_drone[-fade_out_len:] = np.linspace(1.0, 0.0, fade_out_len)
    drone *= env_drone
    
    # 2. Metal/glass tactile ping at 3.0s (Shot 02 Reveal)
    ping = np.zeros_like(t)
    start_3s = int(3.0 * sr)
    len_ping = int(2.5 * sr)
    t_ping = np.linspace(0, 2.5, len_ping, endpoint=False)
    decay_ping = np.exp(-t_ping * 3.5)
    ping_sig = (0.15 * np.sin(2 * np.pi * 1320.0 * t_ping) +
                0.10 * np.sin(2 * np.pi * 1760.0 * t_ping) +
                0.08 * np.sin(2 * np.pi * 880.0 * t_ping)) * decay_ping
    ping[start_3s:start_3s + len_ping] += ping_sig
    
    # 3. Low-end impact pulse & warm C minor pad at 6.0s (Shot 03 Hero Moment)
    hero = np.zeros_like(t)
    start_6s = int(6.0 * sr)
    len_hero = int(4.0 * sr)
    t_hero = np.linspace(0, 4.0, len_hero, endpoint=False)
    # Sub boom
    boom = 0.35 * np.sin(2 * np.pi * 50.0 * t_hero) * np.exp(-t_hero * 1.8)
    # C minor warm harmonic pad (C3=130.8, Eb3=155.6, G3=196.0, Bb3=233.1)
    pad_env = np.sin(np.pi * t_hero / 4.0) ** 0.8
    pad = (0.10 * np.sin(2 * np.pi * 130.8 * t_hero) +
           0.09 * np.sin(2 * np.pi * 155.6 * t_hero) +
           0.08 * np.sin(2 * np.pi * 196.0 * t_hero) +
           0.06 * np.sin(2 * np.pi * 233.1 * t_hero)) * pad_env
    hero[start_6s:start_6s + len_hero] += (boom + pad)
    
    # 4. Crystalline high chime at 9.0s (Shot 04 Brand Frame)
    chime = np.zeros_like(t)
    start_9s = int(9.0 * sr)
    len_chime = int(3.0 * sr)
    t_chime = np.linspace(0, 3.0, len_chime, endpoint=False)
    decay_chime = np.exp(-t_chime * 1.2)
    chime_sig = (0.08 * np.sin(2 * np.pi * 2637.0 * t_chime) +
                 0.05 * np.sin(2 * np.pi * 3951.0 * t_chime)) * decay_chime
    chime[start_9s:start_9s + len_chime] += chime_sig
    
    # Master mix
    left = drone + ping * 0.9 + hero * 0.95 + chime * 0.85
    right = drone + ping * 1.1 + hero * 1.05 + chime * 1.15
    
    # Normalize to -1.5 dBFS
    max_val = max(np.max(np.abs(left)), np.max(np.abs(right)))
    if max_val > 0:
        norm_factor = 0.85 / max_val
        left *= norm_factor
        right *= norm_factor
        
    left_16 = (left * 32767).astype(np.int16)
    right_16 = (right * 32767).astype(np.int16)
    stereo = np.column_stack([left_16, right_16])
    
    wav_path = os.path.join(AUDIO_DIR, "aurelis-commercial-audio.wav")
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(stereo.tobytes())
        
    return wav_path

# -----------------------------------------------------------------------------
# CINEMATIC VIDEO FRAME INTERPOLATION & MOTION ENGINE
# -----------------------------------------------------------------------------
def render_motion_frame(frame_idx, total_frames, width, height):
    """
    Renders an individual video frame at frame_idx (30 fps):
    - Frames 0 to 89 (0-3s): Shot 01 (Darkness & Light Sweep)
    - Frames 90 to 179 (3-6s): Shot 02 (The Reveal)
    - Frames 180 to 269 (6-9s): Shot 03 (The Hero Moment)
    - Frames 270 to 359 (9-12s): Shot 04 (Final Brand Frame)
    """
    t = frame_idx / 30.0  # Time in seconds
    
    if t < 3.0:
        # Shot 01
        u = t / 3.0
        # Light sweeps horizontally
        img = build_shot_01(width, height, light_offset=u)
        # Slow camera push (scale 1.00 -> 1.035)
        zoom = 1.0 + 0.035 * u
        zw, zh = int(width * zoom), int(height * zoom)
        img_zoomed = img.resize((zw, zh), Image.Resampling.BILINEAR)
        crop_x = (zw - width) // 2
        crop_y = (zh - height) // 2
        frame = img_zoomed.crop((crop_x, crop_y, crop_x + width, crop_y + height))
        
        # Crossfade into Shot 02 at end of shot (last 0.35s = ~10 frames)
        if t >= 2.65:
            alpha = (t - 2.65) / 0.35
            next_shot = build_shot_02(width, height, reveal_progress=0.1)
            frame = Image.blend(frame, next_shot, alpha * 0.8)
            
    elif t < 6.0:
        # Shot 02
        u = (t - 3.0) / 3.0
        reveal_p = min(1.0, u * 1.15)
        img = build_shot_02(width, height, reveal_progress=reveal_p)
        zoom = 1.0 + 0.035 * u
        zw, zh = int(width * zoom), int(height * zoom)
        img_zoomed = img.resize((zw, zh), Image.Resampling.BILINEAR)
        crop_x = (zw - width) // 2
        crop_y = (zh - height) // 2
        frame = img_zoomed.crop((crop_x, crop_y, crop_x + width, crop_y + height))
        
        # Crossfade into Shot 03
        if t >= 5.65:
            alpha = (t - 5.65) / 0.35
            next_shot = build_shot_03(width, height, pulse=0.0)
            frame = Image.blend(frame, next_shot, alpha * 0.85)
            
    elif t < 9.0:
        # Shot 03
        u = (t - 6.0) / 3.0
        pulse = math.sin(u * math.pi * 2.0) * 0.4
        img = build_shot_03(width, height, pulse=pulse)
        zoom = 1.0 + 0.025 * u
        zw, zh = int(width * zoom), int(height * zoom)
        img_zoomed = img.resize((zw, zh), Image.Resampling.BILINEAR)
        crop_x = (zw - width) // 2
        crop_y = (zh - height) // 2
        frame = img_zoomed.crop((crop_x, crop_y, crop_x + width, crop_y + height))
        
        # Crossfade into Shot 04
        if t >= 8.65:
            alpha = (t - 8.65) / 0.35
            next_shot = build_shot_04(width, height, text_alpha=alpha)
            frame = Image.blend(frame, next_shot, alpha * 0.9)
            
    else:
        # Shot 04
        u = (t - 9.0) / 3.0
        text_alpha = min(1.0, (t - 9.0) / 0.6)
        halo_pulse = math.sin(u * math.pi * 3.0) * 0.3
        frame = build_shot_04(width, height, text_alpha=text_alpha, halo_pulse=halo_pulse)
        
        # Fade out in last 0.4s to pure obsidian
        if t >= 11.6:
            fade = 1.0 - (t - 11.6) / 0.4
            black = Image.new("RGB", (width, height), (5, 5, 6))
            frame = Image.blend(black, frame, max(0.0, fade))
            
    return frame

# -----------------------------------------------------------------------------
# VIDEO COMPILER (H.264 MP4 PIPELINE)
# -----------------------------------------------------------------------------
def compile_video_mp4(out_path, width=1920, height=1080, fps=30, duration=12.0, audio_wav=None):
    """
    Compiles 12.0s of motion frames and muxes with audio directly via FFmpeg pipe.
    Produces web-optimized H.264 / yuv420p / +faststart MP4.
    """
    total_frames = int(duration * fps)
    print(f"  Encoding {out_path} ({width}x{height} @ {fps}fps, {total_frames} frames)...")
    
    cmd = [
        FFMPEG_BIN, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{width}x{height}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-"
    ]
    
    if audio_wav and os.path.exists(audio_wav):
        cmd.extend(["-i", audio_wav])
        
    cmd.extend([
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-crf", "19",
        "-r", str(fps),
        "-t", str(duration)
    ])
    
    if audio_wav and os.path.exists(audio_wav):
        cmd.extend(["-c:a", "aac", "-b:a", "192k"])
    else:
        cmd.extend(["-an"])
        
    cmd.extend(["-movflags", "+faststart", out_path])
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    
    for idx in range(total_frames):
        frame = render_motion_frame(idx, total_frames, width, height)
        proc.stdin.write(frame.tobytes())
        if idx % 60 == 0 or idx == total_frames - 1:
            print(f"    Progress: frame {idx + 1}/{total_frames} ({int((idx + 1) / total_frames * 100)}%)")
            
    proc.stdin.close()
    stderr = proc.stderr.read()
    proc.wait()
    
    if proc.returncode != 0:
        print(f"FFmpeg error: {stderr.decode()}", file=sys.stderr)
        raise RuntimeError(f"FFmpeg failed with code {proc.returncode}")
        
    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"  Successfully encoded: {out_path} ({size_mb:.2f} MB)")

# -----------------------------------------------------------------------------
# MAIN GENERATOR PIPELINE
# -----------------------------------------------------------------------------
def main():
    print("=================================================================")
    print("STAGE 3.3 — AURELIS AI COMMERCIAL FILM FULL PRODUCTION PIPELINE")
    print("=================================================================")
    
    resolutions = {
        "9x16": (1080, 1920),
        "16x9": (1920, 1080),
        "4x5":  (1080, 1350)
    }
    
    shot_funcs = [
        ("darkness", build_shot_01),
        ("reveal",   build_shot_02),
        ("hero",     build_shot_03),
        ("brand-frame", build_shot_04)
    ]
    
    shot_9x16_images = []
    
    # 1. Generate Stills
    print("\n[1/5] Generating High-Resolution Shot Stills...")
    for shot_idx, (shot_slug, func) in enumerate(shot_funcs, 1):
        sub_dir = os.path.join(SHOTS_DIR, f"shot-0{shot_idx}")
        for res_name, (rw, rh) in resolutions.items():
            img = func(rw, rh)
            filename = f"aurelis-shot-0{shot_idx}-{shot_slug}-{res_name}.webp"
            out_path = os.path.join(sub_dir, filename)
            img.save(out_path, "WEBP", quality=92, method=6)
            if res_name == "9x16":
                shot_9x16_images.append(img)
    print("  All 12 shot stills generated.")
    
    # 2. Posters & Storyboard
    print("\n[2/5] Generating Posters and Consolidated Storyboard Board...")
    poster_16x9 = build_shot_03(1920, 1080)
    poster_16x9.save(os.path.join(POSTERS_DIR, "aurelis-commercial-poster-16x9.webp"), "WEBP", quality=92, method=6)
    poster_16x9.save(os.path.join(VIDEO_DIR, "aurelis-commercial-poster.webp"), "WEBP", quality=92, method=6)
    
    poster_9x16 = build_shot_03(1080, 1920)
    poster_9x16.save(os.path.join(POSTERS_DIR, "aurelis-commercial-poster-9x16.webp"), "WEBP", quality=92, method=6)
    
    board = build_storyboard_board(shot_9x16_images)
    board.save(os.path.join(MASTERS_DIR, "aurelis-commercial-storyboard-board.webp"), "WEBP", quality=92, method=6)
    print("  Posters and Master Storyboard Board generated.")
    
    # 3. Animated WebP Previews
    print("\n[3/5] Generating Animated WebP Previews...")
    s1 = build_shot_01(960, 540)
    s2 = build_shot_02(960, 540)
    s3 = build_shot_03(960, 540)
    s4 = build_shot_04(960, 540)
    frames_16x9 = [
        s1, s1, Image.blend(s1, s2, 0.5),
        s2, s2, Image.blend(s2, s3, 0.5),
        s3, s3, Image.blend(s3, s4, 0.5),
        s4, s4, s4
    ]
    frames_16x9[0].save(
        os.path.join(PREVIEWS_DIR, "aurelis-commercial-preview-16x9.webp"),
        "WEBP",
        save_all=True,
        append_images=frames_16x9[1:],
        duration=1000,
        loop=0
    )
    
    s1_v = build_shot_01(540, 960)
    s2_v = build_shot_02(540, 960)
    s3_v = build_shot_03(540, 960)
    s4_v = build_shot_04(540, 960)
    frames_9x16 = [
        s1_v, s1_v, Image.blend(s1_v, s2_v, 0.5),
        s2_v, s2_v, Image.blend(s2_v, s3_v, 0.5),
        s3_v, s3_v, Image.blend(s3_v, s4_v, 0.5),
        s4_v, s4_v, s4_v
    ]
    frames_9x16[0].save(
        os.path.join(PREVIEWS_DIR, "aurelis-commercial-preview-9x16.webp"),
        "WEBP",
        save_all=True,
        append_images=frames_9x16[1:],
        duration=1000,
        loop=0
    )
    print("  Animated previews generated.")
    
    # 4. Audio Synthesis
    print("\n[4/5] Synthesizing Luxury Acoustic Soundtrack...")
    audio_wav = synthesize_commercial_audio(duration=12.0, sr=48000)
    print(f"  Acoustic soundtrack generated: {audio_wav}")
    
    # 5. Compile Real MP4 Videos
    print("\n[5/5] Compiling REAL Playable H.264 MP4 Films...")
    # A. Mandatory Website Ready Video
    website_mp4 = os.path.join(VIDEO_DIR, "aurelis-commercial.mp4")
    compile_video_mp4(website_mp4, width=1920, height=1080, fps=30, duration=12.0, audio_wav=audio_wav)
    
    # B. Master Archive Copy
    master_mp4 = os.path.join(FINAL_DIR, "aurelis-noir-eclat-commercial-master.mp4")
    # Copy or hardlink
    import shutil
    shutil.copyfile(website_mp4, master_mp4)
    print(f"  Master archive saved: {master_mp4}")
    
    # C. Vertical Master (9:16)
    vertical_mp4 = os.path.join(FINAL_DIR, "aurelis-noir-eclat-commercial-vertical.mp4")
    compile_video_mp4(vertical_mp4, width=1080, height=1920, fps=30, duration=12.0, audio_wav=audio_wav)
    
    print("\n=================================================================")
    print(">>> STAGE 3.3 REAL PLAYABLE COMMERCIAL FILM CREATED SUCCESSFULLY!")
    print(f">>> Website Playable File: {website_mp4} ({os.path.getsize(website_mp4)} bytes)")
    print("=================================================================")

if __name__ == "__main__":
    main()
