"""
AURELIS — STAGE 3.1: FINAL PRODUCT MASTER & PREMIUM PRODUCT PHOTOGRAPHY SYSTEM
Generates the canonical NOIR ÉCLAT bottle master, controlled angles, macro details,
luxury packaging suite, master reference sheet board, and the 8-image hero photography collection.

All assets adhere strictly to the Stage 1 & Stage 2 AURELIS Master Design Specifications:
- Monolithic rectangular smoked obsidian flint glass flacon with 45° micro-chamfers
- 70mm solid crystal foundation base
- Brushed champagne brass (#CBB99F) cylindrical cap with engraved monogram
- 320gsm unbleached warm ivory cotton rag label with letterpress debossed typography
- Translucent cognac/amber liquid core (#5A3C20)
- Deep obsidian chiaroscuro atmosphere (#0B0B0C)
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
MASTER_DIR = os.path.join(ASSETS_DIR, 'product-master')
PHOTO_DIR = os.path.join(ASSETS_DIR, 'photography')

HERO_DIR = os.path.join(PHOTO_DIR, 'hero')
ARCH_DIR = os.path.join(PHOTO_DIR, 'architectural')
AMBER_DIR = os.path.join(PHOTO_DIR, 'amber')
MACRO_DIR = os.path.join(PHOTO_DIR, 'macro')
EDIT_DIR = os.path.join(PHOTO_DIR, 'editorial')
CINE_DIR = os.path.join(PHOTO_DIR, 'cinematic')
TACTILE_DIR = os.path.join(PHOTO_DIR, 'tactile')
CAMP_DIR = os.path.join(PHOTO_DIR, 'campaign-master')

for d in [MASTER_DIR, HERO_DIR, ARCH_DIR, AMBER_DIR, MACRO_DIR, EDIT_DIR, CINE_DIR, TACTILE_DIR, CAMP_DIR]:
    os.makedirs(d, exist_ok=True)

# System Font Paths
DIDOT = '/System/Library/Fonts/Supplemental/Didot.ttc'
HELV = '/System/Library/Fonts/HelveticaNeue.ttc'

# Canonical Palette Constants
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
AMBER_CORE = (55, 36, 22)
AMBER_GLOW = (140, 80, 35)


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


def draw_plinth_and_caustics(draw, bx, plinth_y, plinth_w=1100, plinth_h=24, caustics_int=1.0):
    """Draws a heavy black granite pedestal with specular top reflection and amber caustic pools."""
    # Top surface highlight
    draw.rectangle([bx - plinth_w // 2, plinth_y, bx + plinth_w // 2, plinth_y + plinth_h],
                   fill=(20, 19, 20), outline=(52, 48, 44), width=1)
    
    # Subsurface falloff
    for i in range(160):
        alpha = int(55 * (1.0 - i / 160.0))
        draw.line([(bx - plinth_w // 2 + i * 3, plinth_y + plinth_h + i),
                   (bx + plinth_w // 2 - i * 3, plinth_y + plinth_h + i)],
                  fill=(18 + alpha // 3, 17 + alpha // 3, 18 + alpha // 4))

    # Amber caustics reflection on granite
    caustic_w = int(280 * caustics_int)
    for cx_offset in range(-caustic_w, caustic_w):
        t = abs(cx_offset) / caustic_w
        intensity = math.exp(-((t * 2.2) ** 2)) * caustics_int
        r = min(255, int(20 + 90 * intensity))
        g = min(255, int(19 + 50 * intensity))
        b = min(255, int(20 + 20 * intensity))
        draw.point((bx + cx_offset, plinth_y + 1), fill=(r, g, b))
        draw.point((bx + cx_offset, plinth_y + 2), fill=(r, g, b))


def draw_canonical_bottle_front(draw, bx, by, bw, bh, f_brand, f_name, f_sub,
                                light_side='left', amber_boost=1.0, show_label=True):
    """
    Renders the locked canonical AURELIS NOIR ÉCLAT bottle in straight-on elevation.
    """
    # 1. Cap (Solid brushed champagne brass cylinder)
    cap_w = int(bw * 0.52)
    cap_h = int(bh * 0.21)
    cap_top = by

    draw.rectangle([bx - cap_w // 2, cap_top, bx + cap_w // 2, cap_top + cap_h],
                   fill=CHAMPAGNE, outline=CHAMPAGNE_LIGHT, width=1)
    
    # Cap radial brushed brass grain & specular highlights
    hl_pos = 0.28 if light_side == 'left' else 0.72
    for px in range(bx - cap_w // 2, bx + cap_w // 2):
        t = (px - (bx - cap_w // 2)) / cap_w
        hl = math.exp(-((t - hl_pos) ** 2) / 0.015)
        r = int(203 * (0.75 + 0.25 * t) + 48 * hl)
        g = int(185 * (0.75 + 0.25 * t) + 48 * hl)
        b = int(159 * (0.75 + 0.25 * t) + 48 * hl)
        draw.line([(px, cap_top + 1), (px, cap_top + cap_h - 1)], fill=(min(255, r), min(255, g), min(255, b)))

    # Engraved Monogram Medallion on Cap apex
    med_r = int(cap_w * 0.16)
    med_cy = cap_top + cap_h // 2
    draw.ellipse([bx - med_r, med_cy - med_r, bx + med_r, med_cy + med_r], outline=CHAMPAGNE_DARK, width=1)
    draw_tracking_text(draw, 'A', (bx, med_cy - int(med_r * 0.55)), f_name, CHAMPAGNE_DARK, spacing=0, anchor='center')

    # 2. Neck Collar
    neck_w = int(bw * 0.24)
    neck_h = int(bh * 0.05)
    neck_top = cap_top + cap_h
    draw.rectangle([bx - neck_w // 2, neck_top, bx + neck_w // 2, neck_top + neck_h],
                   fill=(42, 39, 36), outline=CHAMPAGNE, width=1)

    # 3. Monolithic Glass Body
    body_top = neck_top + neck_h
    body_w = bw
    body_h = bh - (cap_h + neck_h)
    draw.rectangle([bx - body_w // 2, body_top, bx + body_w // 2, body_top + body_h],
                   fill=(15, 14, 15), outline=CHAMPAGNE, width=1)

    # 4. Solid Crystal Foundation Base (70mm thick equivalent)
    base_h = int(body_h * 0.18)
    base_top = body_top + body_h - base_h
    draw.rectangle([bx - body_w // 2, base_top, bx + body_w // 2, body_top + body_h],
                   fill=(22, 21, 23), outline=(48, 44, 40), width=1)

    # 5. Liquid Reservoir & Amber Resonance
    res_w = body_w - 52
    res_top = body_top + 28
    res_bottom = base_top - 8

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

    # 6. Glass Edge Specular Highlights & Corner Chamfers
    edge_hl = (130, 120, 110) if light_side == 'left' else (60, 55, 50)
    edge_sh = (60, 55, 50) if light_side == 'left' else (130, 120, 110)
    draw.line([(bx - body_w // 2 + 8, body_top + 10), (bx - body_w // 2 + 8, body_top + body_h - 10)], fill=edge_hl, width=2)
    draw.line([(bx + body_w // 2 - 8, body_top + 10), (bx + body_w // 2 - 8, body_top + body_h - 10)], fill=edge_sh, width=1)

    draw.line([(bx - body_w // 2 + 2, body_top + 2), (bx - body_w // 2 + 10, body_top + 10)], fill=(155, 145, 135), width=1)
    draw.line([(bx + body_w // 2 - 2, body_top + 2), (bx + body_w // 2 - 10, body_top + 10)], fill=(85, 80, 75), width=1)

    # 7. Unbleached Cotton Rag Label
    if show_label:
        lw = int(body_w * 0.58)
        lh = int(body_h * 0.52)
        lt = body_top + (body_h - base_h) // 2 - lh // 2 + 20
        label_box = [bx - lw // 2, lt, bx + lw // 2, lt + lh]

        draw.rectangle(label_box, fill=IVORY, outline=CHAMPAGNE, width=1)
        draw.rectangle([label_box[0] + 6, label_box[1] + 6, label_box[2] - 6, label_box[3] - 6],
                       outline=(222, 218, 208), width=1)

        ly = lt + int(lh * 0.16)
        draw_tracking_text(draw, 'AURELIS', (bx, ly), f_brand, OBSIDIAN, spacing=4, anchor='center')
        ly += int(lh * 0.18)
        draw.line([(bx - 36, ly), (bx + 36, ly)], fill=CHAMPAGNE, width=1)
        ly += int(lh * 0.12)
        draw_tracking_text(draw, 'NOIR ÉCLAT', (bx, ly), f_name, (40, 38, 36), spacing=3, anchor='center')
        ly += int(lh * 0.14)
        draw_tracking_text(draw, 'EAU DE PARFUM', (bx, ly), f_sub, STONE, spacing=2, anchor='center')
        ly += int(lh * 0.11)
        draw_tracking_text(draw, '100 ML · 3.4 FL. OZ.', (bx, ly), f_sub, STONE, spacing=2, anchor='center')
        ly += int(lh * 0.16)
        draw_tracking_text(draw, 'PARIS', (bx, ly), f_sub, CHAMPAGNE_DARK, spacing=4, anchor='center')


# ==============================================================================
# 1. CANONICAL PRODUCT MASTER SUITE
# ==============================================================================

def generate_front_master():
    """Generates the primary canonical front elevation product master."""
    W, H = 1800, 2400
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    f_header = ImageFont.truetype(DIDOT, 44, index=0)
    f_sub_hd = ImageFont.truetype(HELV, 14, index=0)
    f_brand = ImageFont.truetype(DIDOT, 28, index=0)
    f_name = ImageFont.truetype(HELV, 16, index=1)
    f_sub = ImageFont.truetype(HELV, 11, index=0)
    f_footer_title = ImageFont.truetype(DIDOT, 36, index=0)

    # Chiaroscuro radial ambient background
    cx, cy = W // 2, 1100
    for r in range(1250, 0, -10):
        t = 1.0 - r / 1250.0
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(int(11 + 18 * t), int(11 + 16 * t), int(12 + 14 * t)))

    m = 65
    draw.rectangle([m, m, W - m, H - m], outline=CHAMPAGNE, width=1)
    draw_tracking_text(draw, 'AURELIS', (W // 2, 115), f_header, IVORY, spacing=16, anchor='center')
    draw_tracking_text(draw, 'CANONICAL PRODUCT MASTER · DIRECT FRONT ELEVATION', (W // 2, 175), f_sub_hd, CHAMPAGNE, spacing=5, anchor='center')
    draw.line([(m + 50, 210), (W - m - 50, 210)], fill=(48, 44, 40), width=1)

    # Bottle Placement
    bx = W // 2
    by = 520
    bw = 430
    bh = 880
    plinth_y = by + bh + 40

    draw_plinth_and_caustics(draw, bx, plinth_y, plinth_w=1100, plinth_h=22, caustics_int=1.0)
    draw_canonical_bottle_front(draw, bx, by, bw, bh, f_brand, f_name, f_sub, light_side='left', amber_boost=1.0)

    # Bottom Specs Strip
    by_foot = H - 200
    draw.line([(m + 50, by_foot), (W - m - 50, by_foot)], fill=(48, 44, 40), width=1)
    draw_tracking_text(draw, '"THE ART OF SCENT"', (W // 2, by_foot + 35), f_footer_title, IVORY, spacing=10, anchor='center')
    draw_tracking_text(draw, 'NOIR ÉCLAT · 100 ML EAU DE PARFUM · MONOLITHIC OBSIDIAN GLASS · PARIS',
                       (W // 2, by_foot + 105), f_sub_hd, STONE, spacing=3, anchor='center')

    out_path = os.path.join(MASTER_DIR, 'aurelis-noir-eclat-front-master.webp')
    img.save(out_path, 'WEBP', quality=96)
    print(f'[MASTER] Wrote: {out_path}')


def generate_perspective_angle(side='left'):
    """Generates the 3/4 perspective views (Angle Left / Angle Right) of the exact master bottle."""
    W, H = 1800, 2400
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    f_header = ImageFont.truetype(DIDOT, 44, index=0)
    f_sub_hd = ImageFont.truetype(HELV, 14, index=0)
    f_brand = ImageFont.truetype(DIDOT, 28, index=0)
    f_name = ImageFont.truetype(HELV, 16, index=1)
    f_sub = ImageFont.truetype(HELV, 11, index=0)
    f_footer_title = ImageFont.truetype(DIDOT, 36, index=0)

    # Lighting biased toward active side
    cx = W // 2 - 120 if side == 'left' else W // 2 + 120
    cy = 1100
    for r in range(1250, 0, -10):
        t = 1.0 - r / 1250.0
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(int(11 + 22 * t), int(11 + 18 * t), int(12 + 15 * t)))

    m = 65
    draw.rectangle([m, m, W - m, H - m], outline=CHAMPAGNE, width=1)
    title_sub = '3/4 PERSPECTIVE LEFT VIEW' if side == 'left' else '3/4 PERSPECTIVE RIGHT VIEW'
    draw_tracking_text(draw, 'AURELIS', (W // 2, 115), f_header, IVORY, spacing=16, anchor='center')
    draw_tracking_text(draw, f'CANONICAL PRODUCT MASTER · {title_sub}', (W // 2, 175), f_sub_hd, CHAMPAGNE, spacing=5, anchor='center')
    draw.line([(m + 50, 210), (W - m - 50, 210)], fill=(48, 44, 40), width=1)

    bx = W // 2
    by = 520
    bw = 430
    bh = 880
    plinth_y = by + bh + 40

    draw_plinth_and_caustics(draw, bx, plinth_y, plinth_w=1100, plinth_h=22, caustics_int=1.1)

    # 3/4 Perspective Offset: front face is shifted, side face extruded
    offset_x = -35 if side == 'left' else 35
    side_depth = 55

    # Side plane (depth extrusion)
    side_dir = -1 if side == 'left' else 1
    face_bx = bx + offset_x

    # Render main bottle face
    draw_canonical_bottle_front(draw, face_bx, by, bw - side_depth, bh, f_brand, f_name, f_sub,
                                light_side=side, amber_boost=1.1)

    # Render side thickness panel to show 3D volume
    cap_w = int((bw - side_depth) * 0.52)
    cap_h = int(bh * 0.21)
    neck_w = int((bw - side_depth) * 0.24)
    neck_h = int(bh * 0.05)
    body_top = by + cap_h + neck_h
    body_h = bh - (cap_h + neck_h)
    base_h = int(body_h * 0.18)

    if side == 'left':
        sx1 = face_bx - (bw - side_depth) // 2 - side_depth
        sx2 = face_bx - (bw - side_depth) // 2
        draw.rectangle([sx1, body_top, sx2, body_top + body_h], fill=(24, 22, 24), outline=(60, 56, 52), width=1)
        # Crystal base side profile
        draw.rectangle([sx1, body_top + body_h - base_h, sx2, body_top + body_h], fill=(32, 30, 32), outline=(70, 65, 60), width=1)
        # Subtle internal amber side scatter
        draw.rectangle([sx1 + 10, body_top + 35, sx2 - 5, body_top + body_h - base_h - 10], fill=(50, 32, 18))
    else:
        sx1 = face_bx + (bw - side_depth) // 2
        sx2 = face_bx + (bw - side_depth) // 2 + side_depth
        draw.rectangle([sx1, body_top, sx2, body_top + body_h], fill=(20, 19, 20), outline=(48, 44, 40), width=1)
        draw.rectangle([sx1, body_top + body_h - base_h, sx2, body_top + body_h], fill=(28, 26, 28), outline=(55, 50, 46), width=1)
        draw.rectangle([sx1 + 5, body_top + 35, sx2 - 10, body_top + body_h - base_h - 10], fill=(42, 28, 16))

    by_foot = H - 200
    draw.line([(m + 50, by_foot), (W - m - 50, by_foot)], fill=(48, 44, 40), width=1)
    draw_tracking_text(draw, '"THE ART OF SCENT"', (W // 2, by_foot + 35), f_footer_title, IVORY, spacing=10, anchor='center')
    draw_tracking_text(draw, f'NOIR ÉCLAT · CONTROLLED ANGLE REFERENCE ({side.upper()}) · PARIS',
                       (W // 2, by_foot + 105), f_sub_hd, STONE, spacing=3, anchor='center')

    filename = f'aurelis-noir-eclat-angle-{side}.webp'
    out_path = os.path.join(MASTER_DIR, filename)
    img.save(out_path, 'WEBP', quality=96)
    print(f'[MASTER] Wrote: {out_path}')


def generate_side_view():
    """Generates the direct profile 90-degree side elevation showing glass depth and base thickness."""
    W, H = 1800, 2400
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    f_header = ImageFont.truetype(DIDOT, 44, index=0)
    f_sub_hd = ImageFont.truetype(HELV, 14, index=0)
    f_brand = ImageFont.truetype(DIDOT, 24, index=0)
    f_name = ImageFont.truetype(HELV, 14, index=1)
    f_sub = ImageFont.truetype(HELV, 11, index=0)
    f_footer_title = ImageFont.truetype(DIDOT, 36, index=0)

    cx, cy = W // 2, 1100
    for r in range(1250, 0, -10):
        t = 1.0 - r / 1250.0
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(int(11 + 18 * t), int(11 + 16 * t), int(12 + 14 * t)))

    m = 65
    draw.rectangle([m, m, W - m, H - m], outline=CHAMPAGNE, width=1)
    draw_tracking_text(draw, 'AURELIS', (W // 2, 115), f_header, IVORY, spacing=16, anchor='center')
    draw_tracking_text(draw, 'CANONICAL PRODUCT MASTER · PROFILE SIDE ELEVATION', (W // 2, 175), f_sub_hd, CHAMPAGNE, spacing=5, anchor='center')
    draw.line([(m + 50, 210), (W - m - 50, 210)], fill=(48, 44, 40), width=1)

    bx = W // 2
    by = 520
    bw = 250  # Narrow side profile
    bh = 880
    plinth_y = by + bh + 40

    draw_plinth_and_caustics(draw, bx, plinth_y, plinth_w=900, plinth_h=22, caustics_int=0.9)

    # Cap (Cylindrical side view)
    cap_w = 210
    cap_h = int(bh * 0.21)
    draw.rectangle([bx - cap_w // 2, by, bx + cap_w // 2, by + cap_h], fill=CHAMPAGNE, outline=CHAMPAGNE_LIGHT, width=1)
    for px in range(bx - cap_w // 2, bx + cap_w // 2):
        t = (px - (bx - cap_w // 2)) / cap_w
        hl = math.exp(-((t - 0.3) ** 2) / 0.02)
        r = int(203 * (0.75 + 0.25 * t) + 48 * hl)
        g = int(185 * (0.75 + 0.25 * t) + 48 * hl)
        b = int(159 * (0.75 + 0.25 * t) + 48 * hl)
        draw.line([(px, by + 1), (px, by + cap_h - 1)], fill=(min(255, r), min(255, g), min(255, b)))

    # Neck
    neck_w = 90
    neck_h = int(bh * 0.05)
    neck_top = by + cap_h
    draw.rectangle([bx - neck_w // 2, neck_top, bx + neck_w // 2, neck_top + neck_h], fill=(42, 39, 36), outline=CHAMPAGNE, width=1)

    # Body (Side depth profile)
    body_top = neck_top + neck_h
    body_w = bw
    body_h = bh - (cap_h + neck_h)
    draw.rectangle([bx - body_w // 2, body_top, bx + body_w // 2, body_top + body_h], fill=(16, 15, 16), outline=CHAMPAGNE, width=1)

    # Solid Glass Foundation (visible optical depth)
    base_h = int(body_h * 0.18)
    base_top = body_top + body_h - base_h
    draw.rectangle([bx - body_w // 2, base_top, bx + body_w // 2, body_top + body_h], fill=(25, 24, 26), outline=(50, 46, 42), width=1)

    # Liquid interior profile
    res_w = body_w - 46
    res_top = body_top + 28
    res_bottom = base_top - 8
    draw.rectangle([bx - res_w // 2, res_top, bx + res_w // 2, res_bottom], fill=(50, 32, 18))
    for lx in range(bx - res_w // 2, bx + res_w // 2):
        t = (lx - (bx - res_w // 2)) / res_w
        hl = math.exp(-((t - 0.3) ** 2) / 0.03)
        r = int(55 + 75 * hl)
        g = int(36 + 50 * hl)
        b = int(22 + 28 * hl)
        draw.line([(lx, res_top), (lx, res_bottom)], fill=(r, g, b))

    # Specular rim highlights
    draw.line([(bx - body_w // 2 + 5, body_top + 10), (bx - body_w // 2 + 5, body_top + body_h - 10)], fill=(140, 130, 120), width=2)
    draw.line([(bx + body_w // 2 - 5, body_top + 10), (bx + body_w // 2 - 5, body_top + body_h - 10)], fill=(60, 55, 50), width=1)

    by_foot = H - 200
    draw.line([(m + 50, by_foot), (W - m - 50, by_foot)], fill=(48, 44, 40), width=1)
    draw_tracking_text(draw, '"THE ART OF SCENT"', (W // 2, by_foot + 35), f_footer_title, IVORY, spacing=10, anchor='center')
    draw_tracking_text(draw, 'NOIR ÉCLAT · PROFILE SIDE ELEVATION · 70MM CRYSTAL BASE FOUNDATION',
                       (W // 2, by_foot + 105), f_sub_hd, STONE, spacing=3, anchor='center')

    out_path = os.path.join(MASTER_DIR, 'aurelis-noir-eclat-side.webp')
    img.save(out_path, 'WEBP', quality=96)
    print(f'[MASTER] Wrote: {out_path}')


def generate_macro_details():
    """Generates the 3 macro craftsmanship plates: Shoulder/Glass Macro, Cap Detail, and Label Detail."""
    W, H = 1800, 2400
    f_header = ImageFont.truetype(DIDOT, 44, index=0)
    f_sub_hd = ImageFont.truetype(HELV, 14, index=0)
    f_brand_lg = ImageFont.truetype(DIDOT, 42, index=0)
    f_name_lg = ImageFont.truetype(HELV, 22, index=1)
    f_sub_lg = ImageFont.truetype(HELV, 15, index=0)
    f_footer_title = ImageFont.truetype(DIDOT, 36, index=0)
    m = 65

    # --------------------------------------------------------------------------
    # Macro 1: Cap Detail
    # --------------------------------------------------------------------------
    img_cap = Image.new('RGB', (W, H), OBSIDIAN)
    draw_cap = ImageDraw.Draw(img_cap)
    for y in range(H):
        dist = abs(y - 950) / 1000.0
        draw_cap.line([(0, y), (W, y)], fill=(int(11 + 22 * (1.0 - dist)), int(11 + 18 * (1.0 - dist)), int(12 + 15 * (1.0 - dist))))
    draw_cap.rectangle([m, m, W - m, H - m], outline=CHAMPAGNE, width=1)
    draw_tracking_text(draw_cap, 'AURELIS', (W // 2, 115), f_header, IVORY, spacing=16, anchor='center')
    draw_tracking_text(draw_cap, 'MACRO CRAFTSMANSHIP · BRUSHED CHAMPAGNE BRASS CAP', (W // 2, 175), f_sub_hd, CHAMPAGNE, spacing=5, anchor='center')
    draw_cap.line([(m + 50, 210), (W - m - 50, 210)], fill=(48, 44, 40), width=1)

    # Oversized Cap Section
    cap_x, cap_y = W // 2, 500
    cw, ch = 700, 520
    draw_cap.rectangle([cap_x - cw // 2, cap_y, cap_x + cw // 2, cap_y + ch], fill=CHAMPAGNE, outline=CHAMPAGNE_LIGHT, width=2)
    for px in range(cap_x - cw // 2, cap_x + cw // 2):
        t = (px - (cap_x - cw // 2)) / cw
        hl = math.exp(-((t - 0.28) ** 2) / 0.015)
        r = int(203 * (0.7 + 0.3 * t) + 48 * hl)
        g = int(185 * (0.7 + 0.3 * t) + 48 * hl)
        b = int(159 * (0.7 + 0.3 * t) + 48 * hl)
        draw_cap.line([(px, cap_y + 1), (px, cap_y + ch - 1)], fill=(min(255, r), min(255, g), min(255, b)))

    # Precision Engraved Monogram Medallion
    med_r = 110
    med_cy = cap_y + ch // 2
    draw_cap.ellipse([cap_x - med_r, med_cy - med_r, cap_x + med_r, med_cy + med_r], outline=CHAMPAGNE_DARK, width=2)
    draw_tracking_text(draw_cap, 'A', (cap_x, med_cy - 48), f_brand_lg, CHAMPAGNE_DARK, spacing=0, anchor='center')
    draw_tracking_text(draw_cap, 'MAGNETIC DUAL-ACTION CLOSURE', (cap_x, cap_y + ch + 45), f_sub_hd, STONE, spacing=3, anchor='center')

    # Collar & Shoulder visible below
    neck_w, neck_h = 320, 80
    draw_cap.rectangle([cap_x - neck_w // 2, cap_y + ch, cap_x + neck_w // 2, cap_y + ch + neck_h], fill=(42, 39, 36), outline=CHAMPAGNE, width=1)
    draw_cap.rectangle([cap_x - 550, cap_y + ch + neck_h, cap_x + 550, cap_y + ch + neck_h + 300], fill=(16, 15, 16), outline=CHAMPAGNE, width=2)

    by_foot = H - 200
    draw_cap.line([(m + 50, by_foot), (W - m - 50, by_foot)], fill=(48, 44, 40), width=1)
    draw_tracking_text(draw_cap, '"THE ART OF SCENT"', (W // 2, by_foot + 35), f_footer_title, IVORY, spacing=10, anchor='center')
    draw_tracking_text(draw_cap, 'CHAMPAGNE BRASS CYLINDER · RADIAL MICRO-GRAIN · MONOGRAM APEX',
                       (W // 2, by_foot + 105), f_sub_hd, STONE, spacing=3, anchor='center')

    out_cap = os.path.join(MASTER_DIR, 'aurelis-noir-eclat-cap-detail.webp')
    img_cap.save(out_cap, 'WEBP', quality=96)
    print(f'[MASTER] Wrote: {out_cap}')

    # --------------------------------------------------------------------------
    # Macro 2: Label Detail
    # --------------------------------------------------------------------------
    img_lbl = Image.new('RGB', (W, H), OBSIDIAN)
    draw_lbl = ImageDraw.Draw(img_lbl)
    for y in range(H):
        dist = abs(y - 1100) / 1000.0
        draw_lbl.line([(0, y), (W, y)], fill=(int(11 + 20 * (1.0 - dist)), int(11 + 17 * (1.0 - dist)), int(12 + 14 * (1.0 - dist))))
    draw_lbl.rectangle([m, m, W - m, H - m], outline=CHAMPAGNE, width=1)
    draw_tracking_text(draw_lbl, 'AURELIS', (W // 2, 115), f_header, IVORY, spacing=16, anchor='center')
    draw_tracking_text(draw_lbl, 'MACRO CRAFTSMANSHIP · 320GSM COTTON RAG LABEL', (W // 2, 175), f_sub_hd, CHAMPAGNE, spacing=5, anchor='center')
    draw_lbl.line([(m + 50, 210), (W - m - 50, 210)], fill=(48, 44, 40), width=1)

    # Large Macro Label Display
    lx, ly = W // 2, 480
    lw, lh = 750, 1050
    draw_lbl.rectangle([lx - lw // 2, ly, lx + lw // 2, ly + lh], fill=IVORY, outline=CHAMPAGNE, width=2)
    draw_lbl.rectangle([lx - lw // 2 + 18, ly + 18, lx + lw // 2 - 18, ly + lh - 18], outline=(220, 215, 205), width=1)

    # Debossed typography
    ty = ly + 140
    draw_tracking_text(draw_lbl, 'AURELIS', (lx, ty), ImageFont.truetype(DIDOT, 68, index=0), OBSIDIAN, spacing=14, anchor='center')
    ty += 140
    draw_lbl.line([(lx - 110, ty), (lx + 110, ty)], fill=CHAMPAGNE, width=2)
    ty += 80
    draw_tracking_text(draw_lbl, 'NOIR ÉCLAT', (lx, ty), ImageFont.truetype(HELV, 36, index=1), (40, 38, 36), spacing=6, anchor='center')
    ty += 90
    draw_tracking_text(draw_lbl, 'EAU DE PARFUM', (lx, ty), ImageFont.truetype(HELV, 24, index=0), STONE, spacing=5, anchor='center')
    ty += 70
    draw_tracking_text(draw_lbl, '100 ML · 3.4 FL. OZ.', (lx, ty), ImageFont.truetype(HELV, 24, index=0), STONE, spacing=5, anchor='center')
    ty += 110
    draw_tracking_text(draw_lbl, 'PARIS', (lx, ty), ImageFont.truetype(HELV, 26, index=0), CHAMPAGNE_DARK, spacing=8, anchor='center')

    by_foot = H - 200
    draw_lbl.line([(m + 50, by_foot), (W - m - 50, by_foot)], fill=(48, 44, 40), width=1)
    draw_tracking_text(draw_lbl, '"THE ART OF SCENT"', (W // 2, by_foot + 35), f_footer_title, IVORY, spacing=10, anchor='center')
    draw_tracking_text(draw_lbl, 'BLIND LETTERPRESS DEBOSS · UNBLEACHED FIBER · HOT-STAMPED HAIRLINE',
                       (W // 2, by_foot + 105), f_sub_hd, STONE, spacing=3, anchor='center')

    out_lbl = os.path.join(MASTER_DIR, 'aurelis-noir-eclat-label-detail.webp')
    img_lbl.save(out_lbl, 'WEBP', quality=96)
    print(f'[MASTER] Wrote: {out_lbl}')

    # --------------------------------------------------------------------------
    # Macro 3: Glass, Liquid & Shoulder Macro
    # --------------------------------------------------------------------------
    img_gl = Image.new('RGB', (W, H), OBSIDIAN)
    draw_gl = ImageDraw.Draw(img_gl)
    for y in range(H):
        dist = abs(y - 1000) / 1000.0
        draw_gl.line([(0, y), (W, y)], fill=(int(11 + 24 * (1.0 - dist)), int(11 + 19 * (1.0 - dist)), int(12 + 15 * (1.0 - dist))))
    draw_gl.rectangle([m, m, W - m, H - m], outline=CHAMPAGNE, width=1)
    draw_tracking_text(draw_gl, 'AURELIS', (W // 2, 115), f_header, IVORY, spacing=16, anchor='center')
    draw_tracking_text(draw_gl, 'MACRO CRAFTSMANSHIP · SMOKED FLINT GLASS & AMBER CORE', (W // 2, 175), f_sub_hd, CHAMPAGNE, spacing=5, anchor='center')
    draw_gl.line([(m + 50, 210), (W - m - 50, 210)], fill=(48, 44, 40), width=1)

    # Massive macro view of glass shoulder & radiant cognac liquid
    bx, by_gl = W // 2, 380
    bw_gl, bh_gl = 840, 1100
    draw_gl.rectangle([bx - bw_gl // 2, by_gl, bx + bw_gl // 2, by_gl + bh_gl], fill=(16, 15, 16), outline=CHAMPAGNE, width=2)
    # Amber reservoir with luminous gradient
    res_w = bw_gl - 100
    res_top = by_gl + 60
    draw_gl.rectangle([bx - res_w // 2, res_top, bx + res_w // 2, by_gl + bh_gl], fill=(50, 32, 18))
    for lx in range(bx - res_w // 2, bx + res_w // 2):
        t = (lx - (bx - res_w // 2)) / res_w
        hl = math.exp(-((t - 0.28) ** 2) / 0.035)
        r = int(60 + 95 * hl)
        g = int(38 + 65 * hl)
        b = int(22 + 35 * hl)
        draw_gl.line([(lx, res_top), (lx, by_gl + bh_gl)], fill=(min(255, r), min(255, g), min(255, b)))

    # Chamfered specular reflection
    draw_gl.line([(bx - bw_gl // 2 + 16, by_gl + 14), (bx - bw_gl // 2 + 16, by_gl + bh_gl)], fill=(160, 150, 135), width=3)
    draw_gl.line([(bx + bw_gl // 2 - 16, by_gl + 14), (bx + bw_gl // 2 - 16, by_gl + bh_gl)], fill=(65, 60, 55), width=2)

    # Upper label corner entering frame
    draw_gl.rectangle([bx - 260, by_gl + 360, bx + 260, by_gl + bh_gl], fill=IVORY, outline=CHAMPAGNE, width=2)
    draw_tracking_text(draw_gl, 'AURELIS', (bx, by_gl + 420), f_brand_lg, OBSIDIAN, spacing=8, anchor='center')
    draw_gl.line([(bx - 70, by_gl + 500), (bx + 70, by_gl + 500)], fill=CHAMPAGNE, width=2)
    draw_tracking_text(draw_gl, 'NOIR ÉCLAT', (bx, by_gl + 540), f_name_lg, (40, 38, 36), spacing=4, anchor='center')

    by_foot = H - 200
    draw_gl.line([(m + 50, by_foot), (W - m - 50, by_foot)], fill=(48, 44, 40), width=1)
    draw_tracking_text(draw_gl, '"THE ART OF SCENT"', (W // 2, by_foot + 35), f_footer_title, IVORY, spacing=10, anchor='center')
    draw_tracking_text(draw_gl, '45° MICRO-CHAMFERED CORNERS · RADIANT AMBER LUMINESCENCE · 8K MACRO',
                       (W // 2, by_foot + 105), f_sub_hd, STONE, spacing=3, anchor='center')

    out_gl = os.path.join(MASTER_DIR, 'aurelis-noir-eclat-macro.webp')
    img_gl.save(out_gl, 'WEBP', quality=96)
    print(f'[MASTER] Wrote: {out_gl}')


def generate_packaging():
    """Generates the canonical packaging presentation box beside the master bottle."""
    W, H = 2000, 1500
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(DIDOT, 52, index=0)
    f_box_brand = ImageFont.truetype(DIDOT, 38, index=0)
    f_box_name = ImageFont.truetype(HELV, 20, index=1)
    f_box_sub = ImageFont.truetype(HELV, 14, index=0)
    f_caption = ImageFont.truetype(HELV, 14, index=0)
    f_brand = ImageFont.truetype(DIDOT, 24, index=0)
    f_name = ImageFont.truetype(HELV, 14, index=1)
    f_sub = ImageFont.truetype(HELV, 10, index=0)

    for y in range(H):
        dist = abs(y - 750) / 750.0
        draw.line([(0, y), (W, y)], fill=(int(11 + 16 * (1.0 - dist)), int(11 + 14 * (1.0 - dist)), int(12 + 12 * (1.0 - dist))))

    m = 70
    draw.rectangle([m, m, W - m, H - m], outline=CHAMPAGNE, width=1)
    draw_tracking_text(draw, 'AURELIS', (W // 2, 110), f_title, IVORY, spacing=16, anchor='center')
    draw_tracking_text(draw, 'CANONICAL PACKAGING & PRESENTATION SUITE · NOIR ÉCLAT', (W // 2, 175), f_caption, CHAMPAGNE, spacing=5, anchor='center')
    draw.line([(m + 40, 215), (W - m - 40, 215)], fill=(45, 42, 38), width=1)

    ground_y = 1080
    draw.line([(m + 60, ground_y), (W - m - 60, ground_y)], fill=(42, 38, 34), width=2)
    for i in range(80):
        alpha = int(45 * (1.0 - i / 80.0))
        draw.line([(m + 80 + i * 4, ground_y + i), (W - m - 80 - i * 4, ground_y + i)],
                  fill=(20 + alpha // 3, 19 + alpha // 3, 20 + alpha // 4))

    # 1. Rigid Presentation Box (Left)
    box_w = 520
    box_h = 760
    box_x = 540
    box_y = ground_y - box_h

    draw.rectangle([box_x - box_w // 2, box_y, box_x + box_w // 2, box_y + box_h], fill=CHARCOAL, outline=(60, 56, 52), width=2)
    draw.rectangle([box_x - box_w // 2 + 14, box_y + 14, box_x + box_w // 2 - 14, box_y + box_h - 14], outline=(40, 38, 36), width=1)

    # Box hot-foil lettering
    by_text = box_y + 220
    draw_tracking_text(draw, 'AURELIS', (box_x, by_text), f_box_brand, CHAMPAGNE, spacing=10, anchor='center')
    by_text += 65
    draw.line([(box_x - 60, by_text), (box_x + 60, by_text)], fill=CHAMPAGNE, width=2)
    by_text += 35
    draw_tracking_text(draw, 'NOIR ÉCLAT', (box_x, by_text), f_box_name, IVORY, spacing=5, anchor='center')
    by_text += 45
    draw_tracking_text(draw, 'EAU DE PARFUM', (box_x, by_text), f_box_sub, STONE, spacing=3, anchor='center')
    by_text += 32
    draw_tracking_text(draw, '100 ML · 3.4 FL. OZ.', (box_x, by_text), f_box_sub, STONE, spacing=2, anchor='center')

    # Monogram medallion at bottom of box
    by_text += 180
    draw.ellipse([box_x - 30, by_text, box_x + 30, by_text + 60], outline=(60, 55, 50), width=1)
    draw_tracking_text(draw, 'A', (box_x, by_text + 15), f_box_sub, (80, 75, 70), spacing=0, anchor='center')

    # 2. Canonical Bottle (Right)
    bot_x = 1380
    bot_w = 340
    bot_h = 700
    bot_y = ground_y - bot_h
    draw_canonical_bottle_front(draw, bot_x, bot_y, bot_w, bot_h, f_brand, f_name, f_sub, light_side='left', amber_boost=1.0)

    out_path = os.path.join(MASTER_DIR, 'aurelis-noir-eclat-packaging.webp')
    img.save(out_path, 'WEBP', quality=96)
    print(f'[MASTER] Wrote: {out_path}')


def generate_master_reference_board():
    """Generates the master visual reference sheet / specification board documenting the single source of truth."""
    W, H = 2400, 1600
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    f_main = ImageFont.truetype(DIDOT, 56, index=0)
    f_sub_main = ImageFont.truetype(HELV, 16, index=0)
    f_panel_title = ImageFont.truetype(DIDOT, 24, index=0)
    f_meta_label = ImageFont.truetype(HELV, 13, index=1)
    f_meta_val = ImageFont.truetype(HELV, 13, index=0)
    f_body = ImageFont.truetype(HELV, 12, index=0)

    # Border
    m = 50
    draw.rectangle([m, m, W - m, H - m], outline=CHAMPAGNE, width=1)
    draw.rectangle([m + 8, m + 8, W - m - 8, H - m - 8], outline=(40, 38, 36), width=1)

    # Header Lockup
    draw_tracking_text(draw, 'AURELIS', (W // 2, 90), f_main, IVORY, spacing=18, anchor='center')
    draw_tracking_text(draw, 'CANONICAL PRODUCT MASTER SPECIFICATION BOARD · NOIR ÉCLAT (STAGE 3.1)',
                       (W // 2, 160), f_sub_main, CHAMPAGNE, spacing=5, anchor='center')
    draw.line([(m + 40, 195), (W - m - 40, 195)], fill=(48, 44, 40), width=1)

    # 4 Main Panels Layout
    # Panel 1: Canonical Elevation (Left 1/3)
    p1_x1, p1_y1, p1_x2, p1_y2 = m + 30, 220, m + 720, H - m - 30
    draw.rectangle([p1_x1, p1_y1, p1_x2, p1_y2], fill=(16, 15, 16), outline=CHAMPAGNE, width=1)
    draw_tracking_text(draw, 'CANONICAL ELEVATION', ((p1_x1 + p1_x2) // 2, p1_y1 + 25), f_panel_title, IVORY, spacing=4, anchor='center')
    draw.line([(p1_x1 + 30, p1_y1 + 60), (p1_x2 - 30, p1_y1 + 60)], fill=(48, 44, 40), width=1)

    # Draw mini bottle inside Panel 1
    mini_bx = (p1_x1 + p1_x2) // 2
    mini_by = p1_y1 + 120
    mini_bw = 280
    mini_bh = 580
    draw_plinth_and_caustics(draw, mini_bx, mini_by + mini_bh + 30, plinth_w=580, plinth_h=18, caustics_int=0.9)
    draw_canonical_bottle_front(draw, mini_bx, mini_by, mini_bw, mini_bh,
                                ImageFont.truetype(DIDOT, 20, index=0),
                                ImageFont.truetype(HELV, 11, index=1),
                                ImageFont.truetype(HELV, 9, index=0))

    # Panel 1 Bottom Annotations
    ann_y = mini_by + mini_bh + 90
    draw_tracking_text(draw, 'DIMENSIONS: 430px × 880px (Proportion 1:2.05)', (mini_bx, ann_y), f_meta_val, STONE, spacing=2, anchor='center')
    draw_tracking_text(draw, 'MATERIAL: Smoked Obsidian Flint Glass + Brass Cap', (mini_bx, ann_y + 24), f_meta_val, STONE, spacing=2, anchor='center')
    draw_tracking_text(draw, 'LIQUID: Warm Cognac / Amber Core (#5A3C20)', (mini_bx, ann_y + 48), f_meta_val, CHAMPAGNE, spacing=2, anchor='center')

    # Panel 2: Physical & Material Directives (Middle Upper)
    p2_x1, p2_y1, p2_x2, p2_y2 = m + 750, 220, m + 1550, 840
    draw.rectangle([p2_x1, p2_y1, p2_x2, p2_y2], fill=(16, 15, 16), outline=(48, 44, 40), width=1)
    draw_tracking_text(draw, 'MATERIAL & GEOMETRIC ARCHITECTURE', ((p2_x1 + p2_x2) // 2, p2_y1 + 25), f_panel_title, IVORY, spacing=4, anchor='center')
    draw.line([(p2_x1 + 30, p2_y1 + 60), (p2_x2 - 30, p2_y1 + 60)], fill=(48, 44, 40), width=1)

    specs = [
        ('SILHOUETTE', 'Monolithic rectangular geometry with 45° micro-chamfered corners.'),
        ('CAP ARCHITECTURE', 'Solid cylindrical brushed champagne brass with radial micro-grain.'),
        ('APEX ENGRAVING', 'Architectural monogram medallion engraved on cap apex.'),
        ('CRYSTAL BASE', 'Weighted 70mm solid glass foundation casting warm cognac caustics.'),
        ('LABEL SUBSTRATE', '320gsm unbleached warm ivory fine cotton rag paper.'),
        ('TYPOGRAPHY SYSTEM', 'Didot serif wordmark debossed; clean grotesque metadata.'),
        ('CLOSURE INTENT', 'Dual-action magnetic snap mechanism fit.'),
    ]
    sy = p2_y1 + 85
    for label, desc in specs:
        draw.text((p2_x1 + 30, sy), label, font=f_meta_label, fill=CHAMPAGNE)
        draw.text((p2_x1 + 200, sy), desc, font=f_meta_val, fill=IVORY_MUTED)
        sy += 40

    # Panel 3: Color Palette & Swatches (Middle Lower)
    p3_x1, p3_y1, p3_x2, p3_y2 = m + 750, 870, m + 1550, H - m - 30
    draw.rectangle([p3_x1, p3_y1, p3_x2, p3_y2], fill=(16, 15, 16), outline=(48, 44, 40), width=1)
    draw_tracking_text(draw, 'CORE COLOR SPECIFICATION', ((p3_x1 + p3_x2) // 2, p3_y1 + 25), f_panel_title, IVORY, spacing=4, anchor='center')
    draw.line([(p3_x1 + 30, p3_y1 + 60), (p3_x2 - 30, p3_y1 + 60)], fill=(48, 44, 40), width=1)

    swatches = [
        ('OBSIDIAN', '#0B0B0C', OBSIDIAN, 'Primary void & background canvas'),
        ('CHARCOAL', '#1A1918', CHARCOAL, 'Packaging box & depth shadow'),
        ('CHAMPAGNE', '#CBB99F', CHAMPAGNE, 'Brushed cap & hot-stamped hairline'),
        ('WARM IVORY', '#F7F5F0', IVORY, '320gsm cotton rag label & text'),
        ('COGNAC AMBER', '#5A3C20', (90, 60, 32), 'Translucent glowing liquid core'),
    ]
    sw_y = p3_y1 + 80
    for name, hex_code, col, desc in swatches:
        draw.rectangle([p3_x1 + 30, sw_y, p3_x1 + 100, sw_y + 40], fill=col, outline=CHAMPAGNE, width=1)
        draw.text((p3_x1 + 120, sw_y + 5), name, font=f_meta_label, fill=IVORY)
        draw.text((p3_x1 + 120, sw_y + 22), hex_code, font=f_meta_val, fill=CHAMPAGNE)
        draw.text((p3_x1 + 290, sw_y + 12), desc, font=f_meta_val, fill=STONE)
        sw_y += 55

    # Panel 4: Strict Do-Not-Change Rules (Right 1/3)
    p4_x1, p4_y1, p4_x2, p4_y2 = m + 1580, 220, W - m - 30, H - m - 30
    draw.rectangle([p4_x1, p4_y1, p4_x2, p4_y2], fill=(16, 15, 16), outline=CHAMPAGNE, width=1)
    draw_tracking_text(draw, 'IMMUTABLE SOURCE RULES', ((p4_x1 + p4_x2) // 2, p4_y1 + 25), f_panel_title, IVORY, spacing=4, anchor='center')
    draw.line([(p4_x1 + 30, p4_y1 + 60), (p4_x2 - 30, p4_y1 + 60)], fill=(48, 44, 40), width=1)

    rules = [
        '1. SINGLE MASTER TRUTH',
        'Every future asset (social, commercial, case study) must be derived from this exact geometry.',
        '',
        '2. NO GEOMETRY DRIFT',
        'Do not alter rectangular proportions, chamfer angles, cap cylinder diameter, or label height.',
        '',
        '3. NO SATURATED GOLD',
        'Use muted Champagne (#CBB99F). Never introduce brassy, yellow, or garish gold.',
        '',
        '4. NO PROP CLUTTER',
        'Forbidden: loose flowers, smoke clouds, generic crystals, flying droplets, and marble clichés.',
        '',
        '5. CHIAROSCURO DISCIPLINE',
        'Maintain minimum 50% deep obsidian shadow in every composition to preserve quiet luxury.',
        '',
        '6. LOCKED TYPOGRAPHY',
        'Label text is strictly locked: AURELIS / NOIR ÉCLAT / EAU DE PARFUM / 100 ML / PARIS.',
    ]
    ry = p4_y1 + 85
    for line in rules:
        if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.')):
            draw.text((p4_x1 + 30, ry), line, font=f_meta_label, fill=CHAMPAGNE)
            ry += 22
        elif line == '':
            ry += 15
        else:
            draw.text((p4_x1 + 30, ry), line, font=f_body, fill=IVORY_MUTED)
            ry += 32

    out_path = os.path.join(MASTER_DIR, 'aurelis-product-master-board.webp')
    img.save(out_path, 'WEBP', quality=96)
    print(f'[MASTER] Wrote: {out_path}')


# ==============================================================================
# 2. PREMIUM PRODUCT PHOTOGRAPHY SUITE (8 IMAGES)
# ==============================================================================

def generate_photo_01_hero_portrait():
    """Image 01 — Hero Portrait: Monolithic bottle standing alone, subtle amber glow, vast negative space."""
    W, H = 1600, 2000
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    # Ambient radial backlight centered behind bottle
    cx, cy = W // 2, 1050
    for r in range(1100, 0, -10):
        t = 1.0 - r / 1100.0
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(int(11 + 25 * t), int(11 + 18 * t), int(12 + 15 * t)))

    bx = W // 2
    by = 460
    bw = 420
    bh = 860
    plinth_y = by + bh + 45

    draw_plinth_and_caustics(draw, bx, plinth_y, plinth_w=1050, plinth_h=22, caustics_int=1.2)
    draw_canonical_bottle_front(draw, bx, by, bw, bh,
                                ImageFont.truetype(DIDOT, 28, index=0),
                                ImageFont.truetype(HELV, 16, index=1),
                                ImageFont.truetype(HELV, 11, index=0),
                                light_side='left', amber_boost=1.1)

    out_path = os.path.join(HERO_DIR, 'aurelis-noir-eclat-hero-portrait.webp')
    img.save(out_path, 'WEBP', quality=96)
    print(f'[PHOTO 01] Wrote: {out_path}')


def generate_photo_02_architectural_studio():
    """Image 02 — Architectural Studio: Bottle on stepped monolithic dark granite blocks with sharp orthogonal shadows."""
    W, H = 1600, 2000
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    # Diagonal directional shadow pattern in background
    for x in range(0, W, 4):
        t = x / W
        draw.line([(x, 0), (x - 300, H)], fill=(int(11 + 15 * (1.0 - t)), int(11 + 13 * (1.0 - t)), int(12 + 12 * (1.0 - t))))

    # Stepped Basalt Block 1 (Lower)
    draw.rectangle([100, 1420, 1500, 1650], fill=(18, 17, 18), outline=(48, 44, 40), width=1)
    # Stepped Basalt Block 2 (Main Pedestal)
    bx = W // 2
    by = 440
    bw = 420
    bh = 860
    plinth_y = by + bh + 40
    draw.rectangle([bx - 460, plinth_y, bx + 460, 1420], fill=(22, 21, 23), outline=(55, 50, 46), width=1)

    draw_plinth_and_caustics(draw, bx, plinth_y, plinth_w=920, plinth_h=20, caustics_int=1.0)
    draw_canonical_bottle_front(draw, bx, by, bw, bh,
                                ImageFont.truetype(DIDOT, 28, index=0),
                                ImageFont.truetype(HELV, 16, index=1),
                                ImageFont.truetype(HELV, 11, index=0),
                                light_side='left', amber_boost=1.0)

    out_path = os.path.join(ARCH_DIR, 'aurelis-noir-eclat-architectural-studio.webp')
    img.save(out_path, 'WEBP', quality=96)
    print(f'[PHOTO 02] Wrote: {out_path}')


def generate_photo_03_warm_amber():
    """Image 03 — Warm Amber: Controlled warm amber/cognac illumination radiating from the fragrance liquid."""
    W, H = 1600, 2000
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    # Intimate warm amber radial aura
    cx, cy = W // 2, 980
    for r in range(1000, 0, -8):
        t = 1.0 - r / 1000.0
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(int(11 + 45 * t), int(11 + 25 * t), int(12 + 10 * t)))

    bx = W // 2
    by = 450
    bw = 420
    bh = 860
    plinth_y = by + bh + 45

    draw_plinth_and_caustics(draw, bx, plinth_y, plinth_w=1050, plinth_h=22, caustics_int=1.8)
    draw_canonical_bottle_front(draw, bx, by, bw, bh,
                                ImageFont.truetype(DIDOT, 28, index=0),
                                ImageFont.truetype(HELV, 16, index=1),
                                ImageFont.truetype(HELV, 11, index=0),
                                light_side='left', amber_boost=1.6)

    out_path = os.path.join(AMBER_DIR, 'aurelis-noir-eclat-warm-amber.webp')
    img.save(out_path, 'WEBP', quality=96)
    print(f'[PHOTO 03] Wrote: {out_path}')


def generate_photo_04_macro_detail():
    """Image 04 — Macro Detail: Shallow depth-of-field close-up of the champagne cap and glass shoulder."""
    W, H = 1600, 2000
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    # Radial lighting focused on upper third
    for y in range(H):
        dist = abs(y - 750) / 900.0
        draw.line([(0, y), (W, y)], fill=(int(11 + 24 * (1.0 - dist)), int(11 + 19 * (1.0 - dist)), int(12 + 15 * (1.0 - dist))))

    bx = W // 2
    by = 280

    # Macro Cap
    cw, ch = 560, 420
    draw.rectangle([bx - cw // 2, by, bx + cw // 2, by + ch], fill=CHAMPAGNE, outline=CHAMPAGNE_LIGHT, width=2)
    for px in range(bx - cw // 2, bx + cw // 2):
        t = (px - (bx - cw // 2)) / cw
        hl = math.exp(-((t - 0.28) ** 2) / 0.015)
        r = int(203 * (0.7 + 0.3 * t) + 48 * hl)
        g = int(185 * (0.7 + 0.3 * t) + 48 * hl)
        b = int(159 * (0.7 + 0.3 * t) + 48 * hl)
        draw.line([(px, by + 1), (px, by + ch - 1)], fill=(min(255, r), min(255, g), min(255, b)))

    # Medallion
    med_r = 90
    med_cy = by + ch // 2
    draw.ellipse([bx - med_r, med_cy - med_r, bx + med_r, med_cy + med_r], outline=CHAMPAGNE_DARK, width=2)
    draw_tracking_text(draw, 'A', (bx, med_cy - 40), ImageFont.truetype(DIDOT, 36, index=0), CHAMPAGNE_DARK, spacing=0, anchor='center')

    # Neck
    neck_w, neck_h = 260, 70
    draw.rectangle([bx - neck_w // 2, by + ch, bx + neck_w // 2, by + ch + neck_h], fill=(42, 39, 36), outline=CHAMPAGNE, width=1)

    # Massive Shoulder & Glass
    sw, sh = 960, 800
    st = by + ch + neck_h
    draw.rectangle([bx - sw // 2, st, bx + sw // 2, st + sh], fill=(16, 15, 16), outline=CHAMPAGNE, width=2)

    # Amber core
    draw.rectangle([bx - sw // 2 + 50, st + 45, bx + sw // 2 - 50, st + sh], fill=(50, 32, 18))
    for lx in range(bx - sw // 2 + 50, bx + sw // 2 - 50):
        t = (lx - (bx - sw // 2 + 50)) / (sw - 100)
        hl = math.exp(-((t - 0.28) ** 2) / 0.035)
        r = int(60 + 90 * hl)
        g = int(38 + 60 * hl)
        b = int(22 + 32 * hl)
        draw.line([(lx, st + 45), (lx, st + sh)], fill=(min(255, r), min(255, g), min(255, b)))

    # Bevel highlight
    draw.line([(bx - sw // 2 + 18, st + 14), (bx - sw // 2 + 18, st + sh)], fill=(160, 150, 135), width=3)
    draw.line([(bx + sw // 2 - 18, st + 14), (bx + sw // 2 - 18, st + sh)], fill=(65, 60, 55), width=2)

    # Macro label top edge
    lw, lh = 560, 450
    draw.rectangle([bx - lw // 2, st + 220, bx + lw // 2, st + sh], fill=IVORY, outline=CHAMPAGNE, width=2)
    draw_tracking_text(draw, 'AURELIS', (bx, st + 290), ImageFont.truetype(DIDOT, 48, index=0), OBSIDIAN, spacing=8, anchor='center')
    draw.line([(bx - 80, st + 370), (bx + 80, st + 370)], fill=CHAMPAGNE, width=2)
    draw_tracking_text(draw, 'NOIR ÉCLAT', (bx, st + 410), ImageFont.truetype(HELV, 26, index=1), (40, 38, 36), spacing=5, anchor='center')

    out_path = os.path.join(MACRO_DIR, 'aurelis-noir-eclat-macro-craftsmanship.webp')
    img.save(out_path, 'WEBP', quality=96)
    print(f'[PHOTO 04] Wrote: {out_path}')


def generate_photo_05_editorial_side():
    """Image 05 — Editorial Side Composition: Asymmetrical composition with bottle on right third and vast negative space."""
    W, H = 1600, 2000
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    # Subtle horizontal light gradient falling off from right to left
    for x in range(W):
        t = x / W
        draw.line([(x, 0), (x, H)], fill=(int(11 + 18 * t), int(11 + 16 * t), int(12 + 14 * t)))

    # Bottle positioned on right third
    bx = int(W * 0.68)
    by = 480
    bw = 380
    bh = 780
    plinth_y = by + bh + 40

    draw_plinth_and_caustics(draw, bx, plinth_y, plinth_w=750, plinth_h=20, caustics_int=1.1)
    draw_canonical_bottle_front(draw, bx, by, bw, bh,
                                ImageFont.truetype(DIDOT, 24, index=0),
                                ImageFont.truetype(HELV, 14, index=1),
                                ImageFont.truetype(HELV, 10, index=0),
                                light_side='left', amber_boost=1.0)

    # Left Side Elegant Editorial Typography
    tx = int(W * 0.12)
    draw_tracking_text(draw, 'AURELIS', (tx, 800), ImageFont.truetype(DIDOT, 44, index=0), IVORY, spacing=14, anchor='left')
    draw_tracking_text(draw, 'NOIR ÉCLAT', (tx, 860), ImageFont.truetype(HELV, 16, index=1), CHAMPAGNE, spacing=6, anchor='left')
    draw.line([(tx, 910), (tx + 80, 910)], fill=CHAMPAGNE, width=1)
    draw_tracking_text(draw, '"Fragrance, composed as an experience."', (tx, 940),
                       ImageFont.truetype(DIDOT, 20, index=0), IVORY_MUTED, spacing=2, anchor='left')
    draw_tracking_text(draw, 'EAU DE PARFUM · 100 ML · PARIS', (tx, 990),
                       ImageFont.truetype(HELV, 12, index=0), STONE, spacing=3, anchor='left')

    out_path = os.path.join(EDIT_DIR, 'aurelis-noir-eclat-editorial-side.webp')
    img.save(out_path, 'WEBP', quality=96)
    print(f'[PHOTO 05] Wrote: {out_path}')


def generate_photo_06_dark_cinematic():
    """Image 06 — Dark Cinematic: Bottle emerging subtly from deep obsidian shadow with a high-contrast rim light."""
    W, H = 1600, 2000
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    # Dramatic high-side rim light beam cutting across darkness
    for y in range(H):
        dist = abs(y - 850) / 900.0
        draw.line([(0, y), (W, y)], fill=(int(11 + 12 * (1.0 - dist)), int(11 + 10 * (1.0 - dist)), int(12 + 8 * (1.0 - dist))))

    bx = W // 2
    by = 460
    bw = 420
    bh = 860
    plinth_y = by + bh + 45

    # Deep low-key plinth
    draw.rectangle([bx - 500, plinth_y, bx + 500, plinth_y + 16], fill=(16, 15, 16), outline=(40, 36, 32), width=1)
    draw_canonical_bottle_front(draw, bx, by, bw, bh,
                                ImageFont.truetype(DIDOT, 28, index=0),
                                ImageFont.truetype(HELV, 16, index=1),
                                ImageFont.truetype(HELV, 11, index=0),
                                light_side='left', amber_boost=1.4)

    # Sculpted negative fill shadow across the right flank to create extreme chiaroscuro
    shadow_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_overlay)
    for x in range(bx, bx + bw // 2 + 100):
        t = (x - bx) / (bw // 2 + 100)
        alpha = int(175 * t)
        s_draw.line([(x, by), (x, plinth_y + 60)], fill=(11, 11, 12, alpha))
    img.paste(Image.alpha_composite(img.convert('RGBA'), shadow_overlay).convert('RGB'))

    out_path = os.path.join(CINE_DIR, 'aurelis-noir-eclat-dark-cinematic.webp')
    img.save(out_path, 'WEBP', quality=96)
    print(f'[PHOTO 06] Wrote: {out_path}')


def generate_photo_07_tactile_material():
    """Image 07 — Tactile Material: Juxtaposition of the smooth glass bottle against volcanic stone/charcoal mineral texture."""
    W, H = 1600, 2000
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    # Honed mineral stone texture pattern in background
    for y in range(0, H, 8):
        grain = int(4 * math.sin(y * 0.15))
        draw.line([(0, y), (W, y)], fill=(15 + grain, 14 + grain, 15 + grain))

    bx = W // 2
    by = 460
    bw = 420
    bh = 860
    plinth_y = by + bh + 45

    # Heavy textured volcanic rock slab pedestal
    draw.rectangle([bx - 520, plinth_y, bx + 520, plinth_y + 36], fill=(22, 20, 21), outline=(55, 50, 46), width=2)
    for i in range(120):
        draw.line([(bx - 500 + i * 4, plinth_y + 36 + i), (bx + 500 - i * 4, plinth_y + 36 + i)],
                  fill=(18, 17, 18))

    draw_canonical_bottle_front(draw, bx, by, bw, bh,
                                ImageFont.truetype(DIDOT, 28, index=0),
                                ImageFont.truetype(HELV, 16, index=1),
                                ImageFont.truetype(HELV, 11, index=0),
                                light_side='left', amber_boost=1.1)

    out_path = os.path.join(TACTILE_DIR, 'aurelis-noir-eclat-tactile-material.webp')
    img.save(out_path, 'WEBP', quality=96)
    print(f'[PHOTO 07] Wrote: {out_path}')


def generate_photo_08_campaign_master():
    """Image 08 — Campaign Master: The definitive flagship key visual uniting cinematic lighting, caustics, and branding."""
    W, H = 1600, 2000
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    # Luxurious atmospheric chiaroscuro with champagne caustics
    cx, cy = W // 2, 950
    for r in range(1150, 0, -10):
        t = 1.0 - r / 1150.0
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(int(11 + 30 * t), int(11 + 22 * t), int(12 + 16 * t)))

    bx = W // 2
    by = 440
    bw = 430
    bh = 880
    plinth_y = by + bh + 45

    draw_plinth_and_caustics(draw, bx, plinth_y, plinth_w=1100, plinth_h=24, caustics_int=1.4)
    draw_canonical_bottle_front(draw, bx, by, bw, bh,
                                ImageFont.truetype(DIDOT, 28, index=0),
                                ImageFont.truetype(HELV, 16, index=1),
                                ImageFont.truetype(HELV, 11, index=0),
                                light_side='left', amber_boost=1.3)

    # Overhead Overhead Brand Lockup
    draw_tracking_text(draw, 'AURELIS', (W // 2, 140), ImageFont.truetype(DIDOT, 56, index=0), IVORY, spacing=18, anchor='center')
    draw_tracking_text(draw, 'THE ART OF SCENT', (W // 2, 215), ImageFont.truetype(HELV, 14, index=0), CHAMPAGNE, spacing=6, anchor='center')

    # Bottom Campaign Slogan
    draw_tracking_text(draw, '"LEAVE AN IMPRESSION WITHOUT SAYING A WORD."', (W // 2, H - 180),
                       ImageFont.truetype(DIDOT, 22, index=0), IVORY_MUTED, spacing=4, anchor='center')
    draw_tracking_text(draw, 'NOIR ÉCLAT · EAU DE PARFUM · 100 ML · PARIS', (W // 2, H - 130),
                       ImageFont.truetype(HELV, 12, index=0), STONE, spacing=3, anchor='center')

    out_path = os.path.join(CAMP_DIR, 'aurelis-noir-eclat-campaign-master.webp')
    img.save(out_path, 'WEBP', quality=96)
    print(f'[PHOTO 08] Wrote: {out_path}')


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == '__main__':
    print('======================================================================')
    print('STARTING STAGE 3.1: AURELIS PRODUCT MASTER & PHOTOGRAPHY SUITE GENERATION')
    print('======================================================================')

    # 1. Canonical Product Master Suite
    generate_front_master()
    generate_perspective_angle(side='left')
    generate_perspective_angle(side='right')
    generate_side_view()
    generate_macro_details()
    generate_packaging()
    generate_master_reference_board()

    # 2. Premium Product Photography Suite (8 Hero Images)
    generate_photo_01_hero_portrait()
    generate_photo_02_architectural_studio()
    generate_photo_03_warm_amber()
    generate_photo_04_macro_detail()
    generate_photo_05_editorial_side()
    generate_photo_06_dark_cinematic()
    generate_photo_07_tactile_material()
    generate_photo_08_campaign_master()

    print('======================================================================')
    print('STAGE 3.1 ASSET GENERATION COMPLETE!')
    print('======================================================================')
