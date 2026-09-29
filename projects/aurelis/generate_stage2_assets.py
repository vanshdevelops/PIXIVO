"""
AURELIS — Stage 2 Dedicated Web Asset Generator
Produces clean, web-optimized product renders, hero compositions, and macro craftsmanship visuals
strictly adhering to the Stage 1 Canonical Master Specification.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
PRODUCT_DIR = os.path.join(ASSETS_DIR, 'product')
EDITORIAL_DIR = os.path.join(ASSETS_DIR, 'editorial')
VIDEO_DIR = os.path.join(ASSETS_DIR, 'video')

os.makedirs(PRODUCT_DIR, exist_ok=True)
os.makedirs(EDITORIAL_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

# System Font Paths
DIDOT = '/System/Library/Fonts/Supplemental/Didot.ttc'
HELV = '/System/Library/Fonts/HelveticaNeue.ttc'

# Palette Constants
OBSIDIAN = (11, 11, 12)
CHARCOAL = (26, 25, 24)
STONE = (140, 133, 123)
CHAMPAGNE = (203, 185, 159)
CHAMPAGNE_LIGHT = (225, 212, 192)
CHAMPAGNE_DARK = (150, 130, 105)
IVORY = (247, 245, 240)


def draw_tracking_text(draw, text, pos, font, fill, spacing=6, anchor='center'):
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


def draw_bottle(draw, bx, by, bw, bh, frag_name='NOIR ÉCLAT', liquid_type='noir', f_name=None, f_sub=None, f_brand=None):
    """
    Renders the canonical AURELIS bottle with exact geometry, cap, label, and liquid.
    """
    # Polished Pedestal
    plinth_y = by + bh + 30
    draw.rectangle([bx - int(bw * 1.3), plinth_y, bx + int(bw * 1.3), plinth_y + 16], fill=(18, 17, 18), outline=(48, 44, 40), width=1)
    for i in range(120):
        alpha = int(50 * (1.0 - i / 120.0))
        draw.line([(bx - int(bw * 1.25) + i * 2, plinth_y + 16 + i), (bx + int(bw * 1.25) - i * 2, plinth_y + 16 + i)],
                  fill=(16 + alpha // 3, 15 + alpha // 3, 16 + alpha // 4))

    # Cap
    cap_w = int(bw * 0.52)
    cap_h = int(bh * 0.21)
    cap_top = by
    draw.rectangle([bx - cap_w // 2, cap_top, bx + cap_w // 2, cap_top + cap_h], fill=CHAMPAGNE, outline=CHAMPAGNE_LIGHT, width=1)
    for px in range(bx - cap_w // 2, bx + cap_w // 2):
        t = (px - (bx - cap_w // 2)) / cap_w
        hl = math.exp(-((t - 0.28) ** 2) / 0.015)
        r = int(203 * (0.75 + 0.25 * t) + 45 * hl)
        g = int(185 * (0.75 + 0.25 * t) + 45 * hl)
        b = int(159 * (0.75 + 0.25 * t) + 45 * hl)
        draw.line([(px, cap_top + 1), (px, cap_top + cap_h - 1)], fill=(min(255, r), min(255, g), min(255, b)))

    # Monogram medallion on cap
    med_r = int(cap_w * 0.16)
    med_cy = cap_top + cap_h // 2
    draw.ellipse([bx - med_r, med_cy - med_r, bx + med_r, med_cy + med_r], outline=CHAMPAGNE_DARK, width=1)
    if f_name:
        draw_tracking_text(draw, 'A', (bx, med_cy - 10), f_name, CHAMPAGNE_DARK, spacing=0, anchor='center')

    # Neck
    neck_w = int(bw * 0.24)
    neck_h = int(bh * 0.05)
    neck_top = cap_top + cap_h
    draw.rectangle([bx - neck_w // 2, neck_top, bx + neck_w // 2, neck_top + neck_h], fill=(42, 39, 36), outline=CHAMPAGNE, width=1)

    # Body
    body_top = neck_top + neck_h
    body_w = bw
    body_h = bh - (cap_h + neck_h)
    draw.rectangle([bx - body_w // 2, body_top, bx + body_w // 2, body_top + body_h], fill=(15, 14, 15), outline=CHAMPAGNE, width=1)

    # Base (solid 70mm thick crystal foundation)
    base_h = int(body_h * 0.18)
    base_top = body_top + body_h - base_h
    draw.rectangle([bx - body_w // 2, base_top, bx + body_w // 2, body_top + body_h], fill=(22, 21, 23), outline=(48, 44, 40), width=1)

    # Liquid reservoir
    res_w = body_w - 52
    res_top = body_top + 28
    res_bottom = base_top - 8

    # Liquid palettes
    if liquid_type == 'noir':
        base_col = (45, 30, 18)
        hl_r, hl_g, hl_b = 85, 55, 30
        rgb_base = (55, 36, 22)
    elif liquid_type == 'eclat':
        base_col = (65, 55, 38)
        hl_r, hl_g, hl_b = 135, 115, 75
        rgb_base = (80, 70, 48)
    else:  # ambre
        base_col = (70, 32, 14)
        hl_r, hl_g, hl_b = 130, 65, 25
        rgb_base = (85, 42, 18)

    draw.rectangle([bx - res_w // 2, res_top, bx + res_w // 2, res_bottom], fill=base_col)
    for lx in range(bx - res_w // 2, bx + res_w // 2):
        t = (lx - (bx - res_w // 2)) / res_w
        hl = math.exp(-((t - 0.26) ** 2) / 0.025)
        r = int(rgb_base[0] + hl_r * hl)
        g = int(rgb_base[1] + hl_g * hl)
        b = int(rgb_base[2] + hl_b * hl)
        draw.line([(lx, res_top), (lx, res_bottom)], fill=(min(255, r), min(255, g), min(255, b)))

    # Glass edge vertical specular reflections
    draw.line([(bx - body_w // 2 + 8, body_top + 10), (bx - body_w // 2 + 8, body_top + body_h - 10)], fill=(125, 115, 105), width=2)
    draw.line([(bx + body_w // 2 - 8, body_top + 10), (bx + body_w // 2 - 8, body_top + body_h - 10)], fill=(55, 50, 46), width=1)

    # Chamfered corner highlights
    draw.line([(bx - body_w // 2 + 2, body_top + 2), (bx - body_w // 2 + 10, body_top + 10)], fill=(150, 140, 130), width=1)
    draw.line([(bx + body_w // 2 - 2, body_top + 2), (bx + body_w // 2 - 10, body_top + 10)], fill=(80, 75, 70), width=1)

    # Cotton Rag Paper Label
    lw = int(body_w * 0.58)
    lh = int(body_h * 0.52)
    lt = body_top + (body_h - base_h) // 2 - lh // 2 + 20
    label_box = [bx - lw // 2, lt, bx + lw // 2, lt + lh]
    draw.rectangle(label_box, fill=IVORY, outline=CHAMPAGNE, width=1)
    draw.rectangle([label_box[0] + 6, label_box[1] + 6, label_box[2] - 6, label_box[3] - 6], outline=(222, 218, 208), width=1)

    if f_brand and f_name and f_sub:
        ly = lt + int(lh * 0.16)
        draw_tracking_text(draw, 'AURELIS', (bx, ly), f_brand, OBSIDIAN, spacing=4, anchor='center')
        ly += int(lh * 0.18)
        draw.line([(bx - 36, ly), (bx + 36, ly)], fill=CHAMPAGNE, width=1)
        ly += int(lh * 0.12)
        draw_tracking_text(draw, frag_name, (bx, ly), f_name, (40, 38, 36), spacing=3, anchor='center')
        ly += int(lh * 0.14)
        draw_tracking_text(draw, 'EAU DE PARFUM', (bx, ly), f_sub, STONE, spacing=2, anchor='center')
        ly += int(lh * 0.11)
        draw_tracking_text(draw, '100 ML · 3.4 FL. OZ.', (bx, ly), f_sub, STONE, spacing=2, anchor='center')
        ly += int(lh * 0.16)
        draw_tracking_text(draw, 'PARIS', (bx, ly), f_sub, CHAMPAGNE_DARK, spacing=4, anchor='center')


# ==============================================================================
# 1. STANDALONE BOTTLES (Clean Studio Elevation for Collection Switcher)
# ==============================================================================
def generate_collection_bottles():
    W, H = 1200, 1600
    f_brand = ImageFont.truetype(DIDOT, 24, index=0)
    f_name = ImageFont.truetype(HELV, 14, index=1)
    f_sub = ImageFont.truetype(HELV, 10, index=0)

    fragrances = [
        ('noir-eclat-bottle.webp', 'NOIR ÉCLAT', 'noir'),
        ('eclat-bottle.webp', 'ÉCLAT', 'eclat'),
        ('ambre-bottle.webp', 'AMBRE', 'ambre'),
    ]

    for fname, frag_title, ltype in fragrances:
        img = Image.new('RGB', (W, H), OBSIDIAN)
        draw = ImageDraw.Draw(img)

        # Subtle radial ambient light
        cx, cy = W // 2, H // 2 - 20
        for r in range(700, 0, -10):
            factor = (1.0 - r / 700.0)
            if ltype == 'noir':
                c = (int(11 + 16 * factor), int(11 + 14 * factor), int(12 + 12 * factor))
            elif ltype == 'eclat':
                c = (int(11 + 22 * factor), int(11 + 20 * factor), int(12 + 15 * factor))
            else:
                c = (int(11 + 24 * factor), int(11 + 15 * factor), int(12 + 10 * factor))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

        # Draw Bottle
        bw = 360
        bh = 760
        bx = W // 2
        by = (H - bh) // 2 - 40
        draw_bottle(draw, bx, by, bw, bh, frag_name=frag_title, liquid_type=ltype, f_name=f_name, f_sub=f_sub, f_brand=f_brand)

        out_path = os.path.join(PRODUCT_DIR, fname)
        img.save(out_path, 'WEBP', quality=95)
        print(f"Generated collection bottle: {out_path}")


# ==============================================================================
# 2. HERO COMPOSITION (NOIR-ECLAT-HERO.WEBP)
# ==============================================================================
def generate_hero_image():
    W, H = 1600, 2000
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    f_brand = ImageFont.truetype(DIDOT, 28, index=0)
    f_name = ImageFont.truetype(HELV, 16, index=1)
    f_sub = ImageFont.truetype(HELV, 12, index=0)

    # Dramatic volumetric light ray cutting diagonally
    cx, cy = W // 2, 950
    for r in range(1000, 0, -6):
        factor = (1.0 - r / 1000.0)
        c_r = int(11 + 22 * factor)
        c_g = int(11 + 18 * factor)
        c_b = int(12 + 14 * factor)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(c_r, c_g, c_b))

    # Diagonal atmospheric light beam
    for y in range(H):
        t = y / H
        x_center = int(W * 0.35 + t * W * 0.3)
        width = int(240 + 180 * math.sin(t * math.pi))
        alpha = int(18 * math.sin(t * math.pi))
        draw.line([(x_center - width // 2, y), (x_center + width // 2, y)], fill=(11 + alpha, 11 + alpha - 1, 12 + alpha - 2))

    # Caustic reflection under plinth
    ped_y = 1540
    for rx in range(W // 2 - 420, W // 2 + 420, 2):
        dist = abs(rx - W // 2) / 420.0
        caust = math.exp(-((dist - 0.25) ** 2) / 0.04) * (1.0 - dist)
        g_val = int(35 * caust)
        draw.line([(rx, ped_y), (rx, ped_y + 90)], fill=(int(11 + g_val * 1.3), int(11 + g_val), 12))

    # Canonical Bottle
    bw = 440
    bh = 920
    bx = W // 2
    by = 620
    draw_bottle(draw, bx, by, bw, bh, frag_name='NOIR ÉCLAT', liquid_type='noir', f_name=f_name, f_sub=f_sub, f_brand=f_brand)

    out_path = os.path.join(PRODUCT_DIR, 'noir-eclat-hero.webp')
    img.save(out_path, 'WEBP', quality=95)
    print(f"Generated hero image: {out_path}")


# ==============================================================================
# 3. CAMPAIGN VIDEO POSTER (16:9 CINEMATIC)
# ==============================================================================
def generate_campaign_poster():
    W, H = 1920, 1080
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(DIDOT, 46, index=0)
    f_caption = ImageFont.truetype(HELV, 14, index=0)
    f_brand = ImageFont.truetype(DIDOT, 20, index=0)
    f_name = ImageFont.truetype(HELV, 12, index=1)
    f_sub = ImageFont.truetype(HELV, 9, index=0)

    # Wide cinematic chiaroscuro
    cx, cy = int(W * 0.65), H // 2
    for r in range(800, 0, -8):
        factor = (1.0 - r / 800.0)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(int(11 + 25 * factor), int(11 + 20 * factor), int(12 + 15 * factor)))

    # Left typography anchor
    draw_tracking_text(draw, 'AURELIS', (int(W * 0.22), H // 2 - 70), f_title, IVORY, spacing=16, anchor='center')
    draw.line([(int(W * 0.12), H // 2), (int(W * 0.32), H // 2)], fill=CHAMPAGNE, width=1)
    draw_tracking_text(draw, 'THE ART OF SCENT · OFFICIAL CAMPAIGN FILM', (int(W * 0.22), H // 2 + 25), f_caption, CHAMPAGNE, spacing=4, anchor='center')
    draw_tracking_text(draw, 'DIRECTED FOR PIXIVO FLAGSHIP EXHIBITION', (int(W * 0.22), H // 2 + 65), f_caption, STONE, spacing=3, anchor='center')

    # Right Bottle
    bw = 300
    bh = 640
    bx = int(W * 0.68)
    by = (H - bh) // 2
    draw_bottle(draw, bx, by, bw, bh, frag_name='NOIR ÉCLAT', liquid_type='noir', f_name=f_name, f_sub=f_sub, f_brand=f_brand)

    # Border frame
    m = 35
    draw.rectangle([m, m, W - m, H - m], outline=(40, 38, 36), width=1)
    draw.line([(m + 15, m + 15), (m + 45, m + 15)], fill=CHAMPAGNE, width=1)
    draw.line([(m + 15, m + 15), (m + 15, m + 45)], fill=CHAMPAGNE, width=1)

    out_path = os.path.join(VIDEO_DIR, 'aurelis-commercial-poster.webp')
    img.save(out_path, 'WEBP', quality=95)
    print(f"Generated video poster: {out_path}")


# ==============================================================================
# 4. EDITORIAL MACRO CRAFTSMANSHIP STILLS
# ==============================================================================
def generate_editorial_macros():
    W, H = 1000, 1300
    f_title = ImageFont.truetype(DIDOT, 30, index=0)
    f_caption = ImageFont.truetype(HELV, 13, index=0)
    f_detail = ImageFont.truetype(HELV, 11, index=0)

    # Macro 1: Cap Monogram Detail
    img1 = Image.new('RGB', (W, H), OBSIDIAN)
    d1 = ImageDraw.Draw(img1)
    cx, cy = W // 2, H // 2 - 40
    for r in range(480, 0, -4):
        f = 1.0 - r / 480.0
        d1.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(int(11 + 26 * f), int(11 + 22 * f), int(12 + 18 * f)))
    # Cap disk
    cr = 260
    d1.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=CHAMPAGNE, outline=CHAMPAGNE_LIGHT, width=2)
    # Radial brush texture
    for a in range(0, 360, 2):
        rad = math.radians(a)
        x1 = cx + int((cr - 30) * math.cos(rad))
        y1 = cy + int((cr - 30) * math.sin(rad))
        x2 = cx + int((cr - 4) * math.cos(rad))
        y2 = cy + int((cr - 4) * math.sin(rad))
        d1.line([(x1, y1), (x2, y2)], fill=(min(255, CHAMPAGNE[0] + 20), min(255, CHAMPAGNE[1] + 15), min(255, CHAMPAGNE[2] + 10)))
    # Engraved Monogram circle
    d1.ellipse([cx - 100, cy - 100, cx + 100, cy + 100], outline=CHAMPAGNE_DARK, width=2)
    d1.ellipse([cx - 88, cy - 88, cx + 88, cy + 88], outline=(170, 150, 125), width=1)
    f_mono = ImageFont.truetype(DIDOT, 72, index=0)
    draw_tracking_text(d1, 'A', (cx, cy - 44), f_mono, CHAMPAGNE_DARK, spacing=0, anchor='center')
    # Metadata footer
    d1.line([(80, H - 120), (W - 80, H - 120)], fill=(45, 42, 38), width=1)
    draw_tracking_text(d1, '01 · BRUSHED BRASS ARCHITECTURE', (W // 2, H - 90), f_title, IVORY, spacing=4, anchor='center')
    draw_tracking_text(d1, 'RADIAL BRUSHED FINISH · NEODYMIUM MAGNETIC FIT', (W // 2, H - 50), f_caption, CHAMPAGNE, spacing=3, anchor='center')
    img1.save(os.path.join(EDITORIAL_DIR, 'editorial-01.webp'), 'WEBP', quality=95)

    # Macro 2: Label Letterpress Deboss
    img2 = Image.new('RGB', (W, H), OBSIDIAN)
    d2 = ImageDraw.Draw(img2)
    # Warm cotton rag slab
    rw, rh = 640, 720
    rx = (W - rw) // 2
    ry = (H - rh) // 2 - 40
    d2.rectangle([rx, ry, rx + rw, ry + rh], fill=IVORY, outline=CHAMPAGNE, width=1)
    d2.rectangle([rx + 12, ry + 12, rx + rw - 12, ry + rh - 12], outline=(225, 220, 210), width=1)
    f_l_brand = ImageFont.truetype(DIDOT, 48, index=0)
    f_l_name = ImageFont.truetype(HELV, 22, index=1)
    f_l_sub = ImageFont.truetype(HELV, 14, index=0)
    ly = ry + 140
    draw_tracking_text(d2, 'AURELIS', (W // 2, ly), f_l_brand, OBSIDIAN, spacing=10, anchor='center')
    ly += 90
    d2.line([(W // 2 - 80, ly), (W // 2 + 80, ly)], fill=CHAMPAGNE, width=2)
    ly += 50
    draw_tracking_text(d2, 'NOIR ÉCLAT', (W // 2, ly), f_l_name, (40, 38, 36), spacing=5, anchor='center')
    ly += 55
    draw_tracking_text(d2, 'EAU DE PARFUM · 100 ML', (W // 2, ly), f_l_sub, STONE, spacing=3, anchor='center')
    ly += 40
    draw_tracking_text(d2, 'PARIS', (W // 2, ly), f_l_sub, CHAMPAGNE_DARK, spacing=5, anchor='center')
    # Metadata footer
    d2.line([(80, H - 120), (W - 80, H - 120)], fill=(45, 42, 38), width=1)
    draw_tracking_text(d2, '02 · 320GSM COTTON RAG LABEL', (W // 2, H - 90), f_title, IVORY, spacing=4, anchor='center')
    draw_tracking_text(d2, 'BLIND LETTERPRESS DEBOSS · HOT-STAMPED CHAMPAGNE FOIL', (W // 2, H - 50), f_caption, CHAMPAGNE, spacing=3, anchor='center')
    img2.save(os.path.join(EDITORIAL_DIR, 'editorial-02.webp'), 'WEBP', quality=95)

    # Macro 3: 70mm Solid Crystal Glass Floor
    img3 = Image.new('RGB', (W, H), OBSIDIAN)
    d3 = ImageDraw.Draw(img3)
    # Heavy glass base zoom
    gw, gh = 700, 500
    gx = (W - gw) // 2
    gy = (H - gh) // 2 - 30
    d3.rectangle([gx, gy, gx + gw, gy + gh], fill=(22, 21, 23), outline=(55, 50, 46), width=2)
    # Specular caustic bands
    for i in range(12):
        by = gy + 30 + i * 35
        d3.line([(gx + 15, by), (gx + gw - 15, by)], fill=(40 + i * 4, 34 + i * 3, 24 + i * 2), width=2)
    # Chamfer corner bevels
    d3.line([(gx + 4, gy + 4), (gx + 40, gy + 40)], fill=(160, 150, 135), width=2)
    d3.line([(gx + gw - 4, gy + 4), (gx + gw - 40, gy + 40)], fill=(90, 80, 70), width=2)
    # Polished plinth contact line
    d3.line([(gx - 60, gy + gh), (gx + gw + 60, gy + gh)], fill=CHAMPAGNE, width=1)
    # Metadata footer
    d3.line([(80, H - 120), (W - 80, H - 120)], fill=(45, 42, 38), width=1)
    draw_tracking_text(d3, '03 · 70MM MONOLITHIC CRYSTAL BASE', (W // 2, H - 90), f_title, IVORY, spacing=4, anchor='center')
    draw_tracking_text(d3, 'LEAD-FREE SOLID FLINT GLASS · CAUSTIC LIGHT REFRACTION', (W // 2, H - 50), f_caption, CHAMPAGNE, spacing=3, anchor='center')
    img3.save(os.path.join(EDITORIAL_DIR, 'editorial-03.webp'), 'WEBP', quality=95)

    # Macro 4: Rigid Presentation Box Packaging
    img4 = Image.new('RGB', (W, H), OBSIDIAN)
    d4 = ImageDraw.Draw(img4)
    # Box rectangle
    bx, by = (W - 580) // 2, (H - 740) // 2 - 40
    bw, bh = 580, 740
    d4.rectangle([bx, by, bx + bw, by + bh], fill=CHARCOAL, outline=(55, 52, 48), width=1)
    d4.rectangle([bx + 14, by + 14, bx + bw - 14, by + bh - 14], outline=(40, 38, 35), width=1)
    draw_tracking_text(d4, 'AURELIS', (W // 2, by + 220), f_title, IVORY, spacing=14, anchor='center')
    d4.line([(W // 2 - 50, by + 280), (W // 2 + 50, by + 280)], fill=CHAMPAGNE, width=1)
    draw_tracking_text(d4, 'NOIR ÉCLAT', (W // 2, by + 320), f_caption, CHAMPAGNE, spacing=5, anchor='center')
    draw_tracking_text(d4, 'EAU DE PARFUM · 100 ML', (W // 2, by + 360), f_detail, STONE, spacing=3, anchor='center')
    d4.ellipse([W // 2 - 25, by + 480, W // 2 + 25, by + 530], outline=(70, 65, 60), width=1)
    draw_tracking_text(d4, 'A', (W // 2, by + 495), f_detail, (110, 100, 90), spacing=0, anchor='center')
    # Metadata footer
    d4.line([(80, H - 120), (W - 80, H - 120)], fill=(45, 42, 38), width=1)
    draw_tracking_text(d4, '04 · BESPOKE RIGID PRESENTATION BOX', (W // 2, H - 90), f_title, IVORY, spacing=4, anchor='center')
    draw_tracking_text(d4, '1800GSM FSC-CERTIFIED SOFT-TOUCH CHARCOAL GREYBOARD', (W // 2, H - 50), f_caption, CHAMPAGNE, spacing=3, anchor='center')
    img4.save(os.path.join(EDITORIAL_DIR, 'editorial-04.webp'), 'WEBP', quality=95)

    print("Generated 4 editorial macro images in assets/editorial/")


if __name__ == '__main__':
    print("Generating dedicated Stage 2 web assets...")
    generate_collection_bottles()
    generate_hero_image()
    generate_campaign_poster()
    generate_editorial_macros()
    print("All dedicated Stage 2 web assets generated successfully!")
