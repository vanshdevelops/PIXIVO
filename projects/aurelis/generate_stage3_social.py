"""
AURELIS — STAGE 3.2: SOCIAL CREATIVE CAMPAIGN SYSTEM
Generates the complete 5-piece luxury social media campaign in 4:5 (1080x1350) and 1:1 (1080x1080),
plus the master campaign presentation board (2400x1500).

Creatives:
01 — Brand Introduction ("Fragrance, composed as an experience")
02 — Product Reveal (Hero NOIR ÉCLAT bottle on obsidian plinth)
03 — Fragrance Notes (Calabrian Bergamot, Pink Pepper, Iris, Violet Leaf, Vetiver, Cedar, Amber)
04 — Campaign Mood ("Leave an impression without saying a word")
05 — Launch Creative (Flagship key visual with restrained "EXPLORE THE COLLECTION" CTA)
"""

import os
import math
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
SOCIAL_DIR = os.path.join(ASSETS_DIR, 'social')
CAMP_DIR = os.path.join(SOCIAL_DIR, 'campaign')
MASTERS_DIR = os.path.join(SOCIAL_DIR, 'masters')
PREVIEWS_DIR = os.path.join(SOCIAL_DIR, 'previews')

DIR_01 = os.path.join(CAMP_DIR, '01-brand-introduction')
DIR_02 = os.path.join(CAMP_DIR, '02-product-reveal')
DIR_03 = os.path.join(CAMP_DIR, '03-fragrance-notes')
DIR_04 = os.path.join(CAMP_DIR, '04-campaign-mood')
DIR_05 = os.path.join(CAMP_DIR, '05-launch')

for d in [DIR_01, DIR_02, DIR_03, DIR_04, DIR_05, MASTERS_DIR, PREVIEWS_DIR]:
    os.makedirs(d, exist_ok=True)

# System Fonts
DIDOT = '/System/Library/Fonts/Supplemental/Didot.ttc'
HELV = '/System/Library/Fonts/HelveticaNeue.ttc'

# Canonical Palette
OBSIDIAN = (11, 11, 12)
CHARCOAL = (26, 25, 24)
CHARCOAL_LIGHT = (37, 36, 34)
STONE = (140, 133, 123)
STONE_MUTED = (94, 88, 81)
CHAMPAGNE = (203, 185, 159)
CHAMPAGNE_LIGHT = (225, 212, 192)
CHAMPAGNE_DARK = (150, 130, 105)
IVORY = (247, 245, 240)
IVORY_MUTED = (200, 196, 188)


def draw_tracking_text(draw, text, pos, font, fill, spacing=6, anchor='center'):
    """Renders text with custom letter-spacing and anchoring."""
    widths = [font.getbbox(c)[2] - font.getbbox(c)[0] for c in text]
    tot = sum(widths) + spacing * (len(text) - 1)
    if anchor == 'center':
        cx = pos[0] - tot // 2
    elif anchor == 'right':
        cx = pos[0] - tot
    else:
        cx = pos[0]
    for i, c in enumerate(text):
        draw.text((cx, pos[1]), c, font=font, fill=fill)
        cx += widths[i] + spacing


def draw_plinth_and_caustics(draw, bx, plinth_y, plinth_w=800, plinth_h=18, caustics_int=1.0):
    """Renders the canonical black granite plinth with caustics for social formats."""
    draw.rectangle([bx - plinth_w // 2, plinth_y, bx + plinth_w // 2, plinth_y + plinth_h],
                   fill=(20, 19, 20), outline=(52, 48, 44), width=1)
    for i in range(100):
        alpha = int(45 * (1.0 - i / 100.0))
        draw.line([(bx - plinth_w // 2 + i * 3, plinth_y + plinth_h + i),
                   (bx + plinth_w // 2 - i * 3, plinth_y + plinth_h + i)],
                  fill=(18 + alpha // 3, 17 + alpha // 3, 18 + alpha // 4))

    caustic_w = int(220 * caustics_int)
    for cx_offset in range(-caustic_w, caustic_w):
        t = abs(cx_offset) / caustic_w
        intensity = math.exp(-((t * 2.2) ** 2)) * caustics_int
        r = min(255, int(20 + 85 * intensity))
        g = min(255, int(19 + 48 * intensity))
        b = min(255, int(20 + 18 * intensity))
        draw.point((bx + cx_offset, plinth_y + 1), fill=(r, g, b))
        draw.point((bx + cx_offset, plinth_y + 2), fill=(r, g, b))


def draw_canonical_bottle(draw, bx, by, bw, bh, f_brand, f_name, f_sub,
                          light_side='left', amber_boost=1.0, show_label=True):
    """
    Renders the locked canonical AURELIS NOIR ÉCLAT bottle with exact Stage 3.1 geometry.
    """
    cap_w = int(bw * 0.52)
    cap_h = int(bh * 0.21)
    cap_top = by

    # Cap
    draw.rectangle([bx - cap_w // 2, cap_top, bx + cap_w // 2, cap_top + cap_h],
                   fill=CHAMPAGNE, outline=CHAMPAGNE_LIGHT, width=1)
    hl_pos = 0.28 if light_side == 'left' else 0.72
    for px in range(bx - cap_w // 2, bx + cap_w // 2):
        t = (px - (bx - cap_w // 2)) / cap_w
        hl = math.exp(-((t - hl_pos) ** 2) / 0.015)
        r = int(203 * (0.75 + 0.25 * t) + 48 * hl)
        g = int(185 * (0.75 + 0.25 * t) + 48 * hl)
        b = int(159 * (0.75 + 0.25 * t) + 48 * hl)
        draw.line([(px, cap_top + 1), (px, cap_top + cap_h - 1)], fill=(min(255, r), min(255, g), min(255, b)))

    med_r = int(cap_w * 0.16)
    med_cy = cap_top + cap_h // 2
    draw.ellipse([bx - med_r, med_cy - med_r, bx + med_r, med_cy + med_r], outline=CHAMPAGNE_DARK, width=1)
    draw_tracking_text(draw, 'A', (bx, med_cy - int(med_r * 0.55)), f_name, CHAMPAGNE_DARK, spacing=0, anchor='center')

    # Neck
    neck_w = int(bw * 0.24)
    neck_h = int(bh * 0.05)
    neck_top = cap_top + cap_h
    draw.rectangle([bx - neck_w // 2, neck_top, bx + neck_w // 2, neck_top + neck_h],
                   fill=(42, 39, 36), outline=CHAMPAGNE, width=1)

    # Body
    body_top = neck_top + neck_h
    body_w = bw
    body_h = bh - (cap_h + neck_h)
    draw.rectangle([bx - body_w // 2, body_top, bx + body_w // 2, body_top + body_h],
                   fill=(15, 14, 15), outline=CHAMPAGNE, width=1)

    # 70mm Solid Crystal Base
    base_h = int(body_h * 0.18)
    base_top = body_top + body_h - base_h
    draw.rectangle([bx - body_w // 2, base_top, bx + body_w // 2, body_top + body_h],
                   fill=(22, 21, 23), outline=(48, 44, 40), width=1)

    # Amber Liquid Reservoir
    res_w = body_w - int(bw * 0.12)
    res_top = body_top + int(body_h * 0.04)
    res_bottom = base_top - 6
    rgb_base = (55, 36, 22)
    hl_r, hl_g, hl_b = int(85 * amber_boost), int(55 * amber_boost), int(30 * amber_boost)
    draw.rectangle([bx - res_w // 2, res_top, bx + res_w // 2, res_bottom], fill=(45, 30, 18))
    for lx in range(bx - res_w // 2, bx + res_w // 2):
        t = (lx - (bx - res_w // 2)) / res_w
        hl = math.exp(-((t - hl_pos) ** 2) / 0.025)
        r = int(rgb_base[0] + hl_r * hl)
        g = int(rgb_base[1] + hl_g * hl)
        b = int(rgb_base[2] + hl_b * hl)
        draw.line([(lx, res_top), (lx, res_bottom)], fill=(min(255, r), min(255, g), min(255, b)))

    # Edge Highlights
    edge_hl = (130, 120, 110) if light_side == 'left' else (60, 55, 50)
    edge_sh = (60, 55, 50) if light_side == 'left' else (130, 120, 110)
    draw.line([(bx - body_w // 2 + 6, body_top + 8), (bx - body_w // 2 + 6, body_top + body_h - 8)], fill=edge_hl, width=2)
    draw.line([(bx + body_w // 2 - 6, body_top + 8), (bx + body_w // 2 - 6, body_top + body_h - 8)], fill=edge_sh, width=1)
    draw.line([(bx - body_w // 2 + 2, body_top + 2), (bx - body_w // 2 + 8, body_top + 8)], fill=(155, 145, 135), width=1)
    draw.line([(bx + body_w // 2 - 2, body_top + 2), (bx + body_w // 2 - 8, body_top + 8)], fill=(85, 80, 75), width=1)

    # Label
    if show_label:
        lw = int(body_w * 0.58)
        lh = int(body_h * 0.52)
        lt = body_top + (body_h - base_h) // 2 - lh // 2 + int(body_h * 0.03)
        label_box = [bx - lw // 2, lt, bx + lw // 2, lt + lh]

        draw.rectangle(label_box, fill=IVORY, outline=CHAMPAGNE, width=1)
        draw.rectangle([label_box[0] + 5, label_box[1] + 5, label_box[2] - 5, label_box[3] - 5],
                       outline=(222, 218, 208), width=1)

        ly = lt + int(lh * 0.16)
        draw_tracking_text(draw, 'AURELIS', (bx, ly), f_brand, OBSIDIAN, spacing=3, anchor='center')
        ly += int(lh * 0.18)
        draw.line([(bx - 28, ly), (bx + 28, ly)], fill=CHAMPAGNE, width=1)
        ly += int(lh * 0.12)
        draw_tracking_text(draw, 'NOIR ÉCLAT', (bx, ly), f_name, (40, 38, 36), spacing=2, anchor='center')
        ly += int(lh * 0.14)
        draw_tracking_text(draw, 'EAU DE PARFUM', (bx, ly), f_sub, STONE, spacing=2, anchor='center')
        ly += int(lh * 0.11)
        draw_tracking_text(draw, '100 ML · 3.4 FL. OZ.', (bx, ly), f_sub, STONE, spacing=1, anchor='center')
        ly += int(lh * 0.15)
        draw_tracking_text(draw, 'PARIS', (bx, ly), f_sub, CHAMPAGNE_DARK, spacing=3, anchor='center')


# ==============================================================================
# CREATIVE 01: BRAND INTRODUCTION
# ==============================================================================
def render_creative_01(width=1080, height=1350):
    img = Image.new('RGB', (width, height), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    # Ambient radial depth
    cx, cy = width // 2, height // 2
    max_r = int(width * 0.7)
    for r in range(max_r, 0, -8):
        t = 1.0 - r / max_r
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(int(11 + 22 * t), int(11 + 17 * t), int(12 + 14 * t)))

    # Thin editorial outer hairline border (inside 60px padding)
    pad = 60
    draw.rectangle([pad, pad, width - pad, height - pad], outline=CHAMPAGNE, width=1)
    draw.rectangle([pad + 6, pad + 6, width - pad - 6, height - pad - 6], outline=(38, 35, 32), width=1)

    # Architectural Monogram & Concentric Medallion (Center Upper)
    med_cy = int(height * 0.36)
    med_r = 75
    draw.ellipse([cx - med_r, med_cy - med_r, cx + med_r, med_cy + med_r], outline=CHAMPAGNE, width=1)
    draw.ellipse([cx - med_r + 10, med_cy - med_r + 10, cx + med_r - 10, med_cy + med_r - 10], outline=(55, 50, 44), width=1)
    draw_tracking_text(draw, 'A', (cx, med_cy - 45), ImageFont.truetype(DIDOT, 68, index=0), CHAMPAGNE, spacing=0, anchor='center')

    # Brand Title Lockup
    draw_tracking_text(draw, 'AURELIS', (cx, med_cy + 135), ImageFont.truetype(DIDOT, 52, index=0), IVORY, spacing=16, anchor='center')
    draw_tracking_text(draw, 'THE ART OF SCENT', (cx, med_cy + 210), ImageFont.truetype(HELV, 14, index=0), CHAMPAGNE, spacing=6, anchor='center')

    # Delicate Hairline Divider
    draw.line([(cx - 45, med_cy + 250), (cx + 45, med_cy + 250)], fill=CHAMPAGNE, width=1)

    # Poetic Supporting Thought
    draw_tracking_text(draw, '"Fragrance, composed as an experience."', (cx, med_cy + 295),
                       ImageFont.truetype(DIDOT, 20, index=0), IVORY_MUTED, spacing=3, anchor='center')
    draw_tracking_text(draw, 'HAUTE PARFUMERIE · PARIS', (cx, med_cy + 345),
                       ImageFont.truetype(HELV, 11, index=0), STONE, spacing=4, anchor='center')

    # Safe Footer Stamp
    draw_tracking_text(draw, 'SELF-INITIATED CONCEPT · PIXIVO ARCHIVE', (cx, height - pad - 35),
                       ImageFont.truetype(HELV, 9, index=0), (60, 56, 52), spacing=3, anchor='center')

    return img


# ==============================================================================
# CREATIVE 02: PRODUCT REVEAL
# ==============================================================================
def render_creative_02(width=1080, height=1350):
    img = Image.new('RGB', (width, height), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    cx, cy = width // 2, int(height * 0.52)
    max_r = int(width * 0.65)
    for r in range(max_r, 0, -8):
        t = 1.0 - r / max_r
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(int(11 + 28 * t), int(11 + 20 * t), int(12 + 15 * t)))

    pad = 60
    draw.rectangle([pad, pad, width - pad, height - pad], outline=CHAMPAGNE, width=1)

    # Overhead Reveal Header
    draw_tracking_text(draw, 'AURELIS', (cx, pad + 55), ImageFont.truetype(DIDOT, 24, index=0), CHAMPAGNE, spacing=10, anchor='center')
    draw_tracking_text(draw, 'THE FLAGSHIP FRAGRANCE', (cx, pad + 95), ImageFont.truetype(HELV, 10, index=0), STONE, spacing=4, anchor='center')

    # Canonical Bottle Centered
    bw = 310
    bh = 635
    by = int(height * 0.22)
    plinth_y = by + bh + 30

    draw_plinth_and_caustics(draw, cx, plinth_y, plinth_w=680, plinth_h=16, caustics_int=1.2)
    draw_canonical_bottle(draw, cx, by, bw, bh,
                          ImageFont.truetype(DIDOT, 20, index=0),
                          ImageFont.truetype(HELV, 12, index=1),
                          ImageFont.truetype(HELV, 8, index=0),
                          light_side='left', amber_boost=1.15)

    # Lower Product Reveal Typography
    ty = plinth_y + 65
    draw_tracking_text(draw, 'NOIR ÉCLAT', (cx, ty), ImageFont.truetype(DIDOT, 38, index=0), IVORY, spacing=8, anchor='center')
    ty += 50
    draw.line([(cx - 30, ty), (cx + 30, ty)], fill=CHAMPAGNE, width=1)
    ty += 25
    draw_tracking_text(draw, 'EAU DE PARFUM · 100 ML · PARIS', (cx, ty),
                       ImageFont.truetype(HELV, 12, index=0), CHAMPAGNE, spacing=4, anchor='center')
    ty += 30
    draw_tracking_text(draw, 'Smoked Obsidian Glass · Cognac Amber Core · Brushed Champagne Brass',
                       (cx, ty), ImageFont.truetype(HELV, 10, index=0), STONE, spacing=2, anchor='center')

    return img


# ==============================================================================
# CREATIVE 03: FRAGRANCE NOTES
# ==============================================================================
def render_creative_03(width=1080, height=1350):
    img = Image.new('RGB', (width, height), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    cx = width // 2
    pad = 60
    draw.rectangle([pad, pad, width - pad, height - pad], outline=CHAMPAGNE, width=1)
    draw.rectangle([pad + 6, pad + 6, width - pad - 6, height - pad - 6], outline=(38, 35, 32), width=1)

    # Header
    draw_tracking_text(draw, 'AURELIS', (cx, pad + 55), ImageFont.truetype(DIDOT, 26, index=0), CHAMPAGNE, spacing=10, anchor='center')
    draw_tracking_text(draw, 'OLFACTORY ARCHITECTURE · NOIR ÉCLAT', (cx, pad + 98), ImageFont.truetype(HELV, 11, index=0), STONE, spacing=4, anchor='center')
    draw.line([(cx - 40, pad + 130), (cx + 40, pad + 130)], fill=CHAMPAGNE, width=1)

    # 3-Tier Olfactory Pyramid Layout
    tiers = [
        ('01 / TOP NOTES', 'Calabrian Bergamot · Madagascar Pink Pepper',
         'Immediate cold citrus illumination piercing velvety dark shadows.'),
        ('02 / HEART NOTES', 'Florentine Iris Concrete · Mineral Violet Leaf',
         'Powdery couture elegance grounded by damp, dewy verdancy.'),
        ('03 / BASE NOTES', 'Smoked Haitian Vetiver · Atlas Cedar · Golden Amber',
         'Enduring subterranean sillage radiating warm resinous resonance.'),
    ]

    tier_y = pad + 175
    tier_spacing = int((height - 2 * pad - 260) / 3)

    for i, (title, notes, desc) in enumerate(tiers):
        # Card Box
        bx1, bx2 = pad + 45, width - pad - 45
        by1, by2 = tier_y, tier_y + tier_spacing - 25
        draw.rectangle([bx1, by1, bx2, by2], fill=(16, 15, 16), outline=(45, 42, 38), width=1)

        # Subtle Amber Aura on Left
        for r in range(70, 0, -5):
            t = 1.0 - r / 70.0
            draw.ellipse([bx1 + 35 - r, (by1 + by2) // 2 - r, bx1 + 35 + r, (by1 + by2) // 2 + r],
                         fill=(int(16 + 25 * t), int(15 + 16 * t), int(16 + 8 * t)))

        draw_tracking_text(draw, title, (bx1 + 45, by1 + 25), ImageFont.truetype(HELV, 11, index=1), CHAMPAGNE, spacing=3, anchor='left')
        draw_tracking_text(draw, notes, (bx1 + 45, by1 + 60), ImageFont.truetype(DIDOT, 21, index=0), IVORY, spacing=2, anchor='left')
        draw.line([(bx1 + 45, by1 + 95), (bx1 + 105, by1 + 95)], fill=(60, 56, 50), width=1)
        draw_tracking_text(draw, desc, (bx1 + 45, by1 + 115), ImageFont.truetype(HELV, 11, index=0), STONE, spacing=1, anchor='left')

        tier_y += tier_spacing

    # Footer
    draw_tracking_text(draw, 'FORMULATED IN CONTRAST · HIGH-EXTRAIT PROFILE', (cx, height - pad - 40),
                       ImageFont.truetype(HELV, 10, index=0), CHAMPAGNE_DARK, spacing=3, anchor='center')

    return img


# ==============================================================================
# CREATIVE 04: CAMPAIGN / MOOD CREATIVE
# ==============================================================================
def render_creative_04(width=1080, height=1350):
    img = Image.new('RGB', (width, height), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    # Dramatic chiaroscuro beam cutting across obsidian void
    for y in range(height):
        dist = abs(y - int(height * 0.48)) / (height * 0.6)
        draw.line([(0, y), (width, y)], fill=(int(11 + 16 * (1.0 - dist)), int(11 + 13 * (1.0 - dist)), int(12 + 10 * (1.0 - dist))))

    pad = 60
    draw.rectangle([pad, pad, width - pad, height - pad], outline=CHAMPAGNE, width=1)

    # Top Brand Stamp
    cx = width // 2
    draw_tracking_text(draw, 'AURELIS', (cx, pad + 55), ImageFont.truetype(DIDOT, 24, index=0), CHAMPAGNE, spacing=10, anchor='center')

    # Bottle partially sculpted by shadow
    bw = 310
    bh = 635
    by = int(height * 0.22)
    plinth_y = by + bh + 30

    # Low-key plinth
    draw.rectangle([cx - 380, plinth_y, cx + 380, plinth_y + 16], fill=(18, 17, 18), outline=(42, 38, 34), width=1)
    draw_canonical_bottle(draw, cx, by, bw, bh,
                          ImageFont.truetype(DIDOT, 20, index=0),
                          ImageFont.truetype(HELV, 12, index=1),
                          ImageFont.truetype(HELV, 8, index=0),
                          light_side='left', amber_boost=1.35)

    # Sculpt heavy shadow across right half to create cinematic mystery
    shadow_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_overlay)
    for x in range(cx - 20, cx + bw // 2 + 80):
        t = (x - (cx - 20)) / (bw // 2 + 100)
        alpha = int(185 * t)
        s_draw.line([(x, by), (x, plinth_y + 40)], fill=(11, 11, 12, alpha))
    img.paste(Image.alpha_composite(img.convert('RGBA'), shadow_overlay).convert('RGB'))
    draw = ImageDraw.Draw(img)

    # Campaign Statement Below
    ty = plinth_y + 65
    draw_tracking_text(draw, '"Leave an impression', (cx, ty), ImageFont.truetype(DIDOT, 28, index=0), IVORY, spacing=3, anchor='center')
    ty += 42
    draw_tracking_text(draw, 'without saying a word."', (cx, ty), ImageFont.truetype(DIDOT, 28, index=0), IVORY, spacing=3, anchor='center')
    ty += 50
    draw.line([(cx - 35, ty), (cx + 35, ty)], fill=CHAMPAGNE, width=1)
    ty += 26
    draw_tracking_text(draw, 'NOIR ÉCLAT · THE ART OF SCENT', (cx, ty),
                       ImageFont.truetype(HELV, 11, index=0), STONE, spacing=4, anchor='center')

    return img


# ==============================================================================
# CREATIVE 05: LAUNCH CREATIVE
# ==============================================================================
def render_creative_05(width=1080, height=1350):
    img = Image.new('RGB', (width, height), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    cx = width // 2
    cy = int(height * 0.48)
    max_r = int(width * 0.68)
    for r in range(max_r, 0, -8):
        t = 1.0 - r / max_r
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(int(11 + 32 * t), int(11 + 22 * t), int(12 + 16 * t)))

    pad = 60
    draw.rectangle([pad, pad, width - pad, height - pad], outline=CHAMPAGNE, width=1)
    draw.rectangle([pad + 6, pad + 6, width - pad - 6, height - pad - 6], outline=(38, 35, 32), width=1)

    # Launch Header
    draw_tracking_text(draw, 'AURELIS', (cx, pad + 55), ImageFont.truetype(DIDOT, 42, index=0), IVORY, spacing=16, anchor='center')
    draw_tracking_text(draw, 'THE ART OF SCENT', (cx, pad + 115), ImageFont.truetype(HELV, 12, index=0), CHAMPAGNE, spacing=6, anchor='center')
    draw.line([(cx - 35, pad + 140), (cx + 35, pad + 140)], fill=CHAMPAGNE, width=1)

    # Bottle
    bw = 320
    bh = 650
    by = int(height * 0.22)
    plinth_y = by + bh + 30

    draw_plinth_and_caustics(draw, cx, plinth_y, plinth_w=720, plinth_h=16, caustics_int=1.35)
    draw_canonical_bottle(draw, cx, by, bw, bh,
                          ImageFont.truetype(DIDOT, 20, index=0),
                          ImageFont.truetype(HELV, 12, index=1),
                          ImageFont.truetype(HELV, 8, index=0),
                          light_side='left', amber_boost=1.25)

    # Launch Action Area
    ty = plinth_y + 55
    draw_tracking_text(draw, 'NOIR ÉCLAT', (cx, ty), ImageFont.truetype(DIDOT, 36, index=0), IVORY, spacing=8, anchor='center')
    ty += 42
    draw_tracking_text(draw, 'EAU DE PARFUM · 100 ML', (cx, ty), ImageFont.truetype(HELV, 11, index=0), STONE, spacing=4, anchor='center')

    # Restrained Luxury CTA Pill Button
    ty += 45
    btn_w, btn_h = 290, 48
    draw.rectangle([cx - btn_w // 2, ty, cx + btn_w // 2, ty + btn_h], fill=(24, 22, 24), outline=CHAMPAGNE, width=1)
    draw_tracking_text(draw, 'EXPLORE THE COLLECTION', (cx, ty + 18),
                       ImageFont.truetype(HELV, 10, index=1), CHAMPAGNE, spacing=3, anchor='center')

    draw_tracking_text(draw, 'PARIS · CONCEPT PRESENTATION', (cx, height - pad - 35),
                       ImageFont.truetype(HELV, 9, index=0), (65, 60, 55), spacing=3, anchor='center')

    return img


# ==============================================================================
# CONSOLIDATED MASTER PRESENTATION BOARD (2400 x 1500)
# ==============================================================================
def render_campaign_presentation_board():
    W, H = 2400, 1500
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(DIDOT, 52, index=0)
    f_sub = ImageFont.truetype(HELV, 15, index=0)
    f_num = ImageFont.truetype(HELV, 12, index=1)
    f_name = ImageFont.truetype(DIDOT, 18, index=0)

    m = 50
    draw.rectangle([m, m, W - m, H - m], outline=CHAMPAGNE, width=1)
    draw.rectangle([m + 8, m + 8, W - m - 8, H - m - 8], outline=(40, 38, 36), width=1)

    # Header
    draw_tracking_text(draw, 'AURELIS', (W // 2, 90), f_title, IVORY, spacing=18, anchor='center')
    draw_tracking_text(draw, 'SOCIAL CAMPAIGN SUITE · FIVE-PIECE LUXURY BRAND ARCHIVE (STAGE 3.2)',
                       (W // 2, 160), f_sub, CHAMPAGNE, spacing=5, anchor='center')
    draw.line([(m + 40, 195), (W - m - 40, 195)], fill=(48, 44, 40), width=1)

    # 5 Creatives Strip: 5 thumbnails side by side
    card_w = 410
    card_h = int(card_w * (1350 / 1080))  # 512px
    total_w = card_w * 5 + 40 * 4
    start_x = (W - total_w) // 2
    card_y = 260

    creatives_meta = [
        ('01', 'BRAND INTRODUCTION', render_creative_01()),
        ('02', 'PRODUCT REVEAL', render_creative_02()),
        ('03', 'FRAGRANCE NOTES', render_creative_03()),
        ('04', 'CAMPAIGN MOOD', render_creative_04()),
        ('05', 'LAUNCH KEY VISUAL', render_creative_05()),
    ]

    for i, (num, name, c_img) in enumerate(creatives_meta):
        x = start_x + i * (card_w + 40)
        thumb = c_img.resize((card_w, card_h), Image.Resampling.LANCZOS)
        img.paste(thumb, (x, card_y))
        draw.rectangle([x, card_y, x + card_w, card_y + card_h], outline=CHAMPAGNE, width=1)

        # Labels below each thumbnail
        label_y = card_y + card_h + 25
        draw_tracking_text(draw, f'CREATIVE {num}', (x + card_w // 2, label_y), f_num, CHAMPAGNE, spacing=3, anchor='center')
        draw_tracking_text(draw, name, (x + card_w // 2, label_y + 24), f_name, IVORY, spacing=2, anchor='center')

    # Footer note
    by_foot = H - 120
    draw.line([(m + 40, by_foot), (W - m - 40, by_foot)], fill=(48, 44, 40), width=1)
    draw_tracking_text(draw, 'SELF-INITIATED CONCEPT PROJECT · CREATIVE DIRECTION BY PIXIVO · CANONICAL STAGE 3.2 ARCHIVE',
                       (W // 2, by_foot + 45), f_sub, STONE, spacing=3, anchor='center')

    out_p = os.path.join(MASTERS_DIR, 'aurelis-social-campaign-board.webp')
    img.save(out_p, 'WEBP', quality=96)
    print(f'[MASTER BOARD] Wrote: {out_p}')


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == '__main__':
    print('======================================================================')
    print('STARTING STAGE 3.2: AURELIS SOCIAL CREATIVE CAMPAIGN GENERATION')
    print('======================================================================')

    creatives = [
        ('01-brand-introduction', 'aurelis-social-01-brand-introduction', render_creative_01, DIR_01),
        ('02-product-reveal', 'aurelis-social-02-product-reveal', render_creative_02, DIR_02),
        ('03-fragrance-notes', 'aurelis-social-03-fragrance-notes', render_creative_03, DIR_03),
        ('04-campaign-mood', 'aurelis-social-04-campaign-mood', render_creative_04, DIR_04),
        ('05-launch', 'aurelis-social-05-launch', render_creative_05, DIR_05),
    ]

    for folder_name, base_name, render_func, target_dir in creatives:
        # 1. Primary 4:5 Format (1080 x 1350)
        img_4x5 = render_func(1080, 1350)
        p_4x5 = os.path.join(target_dir, f'{base_name}-4x5.webp')
        img_4x5.save(p_4x5, 'WEBP', quality=95)
        print(f'[SOCIAL 4:5] Wrote: {p_4x5}')

        # Copy to previews for fast website integration
        p_preview = os.path.join(PREVIEWS_DIR, f'{base_name}.webp')
        shutil.copy2(p_4x5, p_preview)

        # 2. Reusable 1:1 Square Format (1080 x 1080)
        img_1x1 = render_func(1080, 1080)
        p_1x1 = os.path.join(target_dir, f'{base_name}-1x1.webp')
        img_1x1.save(p_1x1, 'WEBP', quality=95)
        print(f'[SOCIAL 1:1] Wrote: {p_1x1}')

    # 3. Master Consolidated Showcase Board (2400 x 1500)
    render_campaign_presentation_board()

    print('======================================================================')
    print('STAGE 3.2 SOCIAL CAMPAIGN GENERATION COMPLETE!')
    print('======================================================================')
