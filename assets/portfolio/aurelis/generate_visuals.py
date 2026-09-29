"""
AURELIS — Visual Assets Generator
Generates high-resolution, magazine-editorial brand, product, and art direction visuals for Stage 1.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BRAND_DIR = os.path.join(BASE_DIR, 'brand')
PRODUCT_DIR = os.path.join(BASE_DIR, 'product')
DIRECTION_DIR = os.path.join(BASE_DIR, 'direction')

os.makedirs(BRAND_DIR, exist_ok=True)
os.makedirs(PRODUCT_DIR, exist_ok=True)
os.makedirs(DIRECTION_DIR, exist_ok=True)

# System Font Paths
DIDOT = '/System/Library/Fonts/Supplemental/Didot.ttc'
HELV = '/System/Library/Fonts/HelveticaNeue.ttc'
BODONI = '/System/Library/Fonts/Supplemental/Bodoni 72.ttc'

# Palette Constants
OBSIDIAN = (11, 11, 12)
CHARCOAL = (26, 25, 24)
STONE = (140, 133, 123)
CHAMPAGNE = (203, 185, 159)
CHAMPAGNE_LIGHT = (225, 212, 192)
CHAMPAGNE_DARK = (150, 130, 105)
IVORY = (247, 245, 240)
AMBER = (45, 30, 18)
AMBER_LIGHT = (90, 60, 32)

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

# ==============================================================================
# 1. BRAND / COLOR-PALETTE.WEBP
# ==============================================================================
def generate_color_palette():
    W, H = 2000, 1250
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(DIDOT, 64, index=0)
    f_swatch_name = ImageFont.truetype(DIDOT, 28, index=0)
    f_body_bold = ImageFont.truetype(HELV, 19, index=1)
    f_body = ImageFont.truetype(HELV, 17, index=0)
    f_caption = ImageFont.truetype(HELV, 14, index=0)
    f_micro = ImageFont.truetype(HELV, 12, index=0)

    margin = 70
    draw.rectangle([margin, margin, W - margin, H - margin], outline=CHAMPAGNE, width=1)
    draw.rectangle([margin + 10, margin + 10, W - margin - 10, H - margin - 10], outline=(40, 38, 36), width=1)

    draw_tracking_text(draw, 'AURELIS', (W // 2, 110), f_title, IVORY, spacing=16, anchor='center')
    draw_tracking_text(draw, 'LUXURY COLOR ARCHITECTURE & MATERIAL HARMONY', (W // 2, 190), f_caption, CHAMPAGNE, spacing=6, anchor='center')
    draw.line([(margin + 50, 235), (W - margin - 50, 235)], fill=(50, 47, 44), width=1)

    swatches = [
        {
            'name': 'OBSIDIAN',
            'role': 'PRIMARY BACKGROUND & VOID',
            'hex': '#0B0B0C',
            'rgb': 'RGB(11, 11, 12)',
            'hsl': 'HSL(240°, 4%, 5%)',
            'cmyk': 'CMYK(75, 68, 65, 90)',
            'fill': (11, 11, 12),
            'border': (60, 56, 52),
            'material': 'Polished black granite plinth & smoked flacon exterior',
            'usage': 'Primary digital canvas, packaging body, shadow anchor'
        },
        {
            'name': 'DEEP CHARCOAL',
            'role': 'SECONDARY DARK & DEPTH',
            'hex': '#1A1918',
            'rgb': 'RGB(26, 25, 24)',
            'hsl': 'HSL(30°, 4%, 10%)',
            'cmyk': 'CMYK(68, 62, 63, 78)',
            'fill': (26, 25, 24),
            'border': (70, 66, 60),
            'material': 'Architectural slate & debossed matte rigid cardbox',
            'usage': 'Card surfaces, elevation layers, subtle secondary depth'
        },
        {
            'name': 'WARM TAUPE',
            'role': 'SUPPORTING NEUTRAL & STRUCTURE',
            'hex': '#8C857B',
            'rgb': 'RGB(140, 133, 123)',
            'hsl': 'HSL(35°, 6%, 52%)',
            'cmyk': 'CMYK(40, 36, 42, 12)',
            'fill': (140, 133, 123),
            'border': (160, 152, 142),
            'material': 'Honed limestone, secondary borders & subdued body text',
            'usage': 'Descriptive metadata, dividers, secondary UI typography'
        },
        {
            'name': 'CHAMPAGNE',
            'role': 'SUBTLE METALLIC ACCENT',
            'hex': '#CBB99F',
            'rgb': 'RGB(203, 185, 159)',
            'hsl': 'HSL(35°, 30%, 71%)',
            'cmyk': 'CMYK(20, 24, 38, 0)',
            'fill': (203, 185, 159),
            'border': (223, 205, 180),
            'material': 'Brushed matte metallic cap, micro hot-foil debossing',
            'usage': 'Restrained accents, monograms, hairline dividers, badges'
        },
        {
            'name': 'WARM IVORY',
            'role': 'PRIMARY LIGHT & EDITORIAL',
            'hex': '#F7F5F0',
            'rgb': 'RGB(247, 245, 240)',
            'hsl': 'HSL(43°, 37%, 97%)',
            'cmyk': 'CMYK(2, 2, 4, 0)',
            'fill': (247, 245, 240),
            'border': (200, 195, 185),
            'material': 'Heavy textured unbleached cotton rag paper label',
            'usage': 'Headlines, logo on dark, editorial label face, focal points'
        }
    ]

    total_swatches = len(swatches)
    gap = 24
    swatch_w = (W - 2 * margin - 80 - (total_swatches - 1) * gap) // total_swatches
    swatch_top = 270
    swatch_h = 360

    for idx, s in enumerate(swatches):
        sx = margin + 40 + idx * (swatch_w + gap)
        draw.rectangle([sx, swatch_top, sx + swatch_w, swatch_top + swatch_h], fill=s['fill'], outline=s['border'], width=1)
        if s['name'] == 'CHAMPAGNE':
            draw.line([(sx + 10, swatch_top + 10), (sx + swatch_w - 10, swatch_top + swatch_h - 10)], fill=(235, 220, 195), width=2)
        elif s['name'] == 'OBSIDIAN':
            draw.line([(sx + 10, swatch_top + 10), (sx + swatch_w - 10, swatch_top + swatch_h - 10)], fill=(30, 30, 34), width=1)
            
        ty = swatch_top + swatch_h + 24
        draw.text((sx, ty), s['name'], font=f_swatch_name, fill=IVORY)
        ty += 38
        draw.text((sx, ty), s['role'], font=f_caption, fill=CHAMPAGNE)
        ty += 30
        
        draw.text((sx, ty), s['hex'], font=f_body_bold, fill=IVORY)
        ty += 24
        draw.text((sx, ty), s['rgb'], font=f_caption, fill=STONE)
        ty += 20
        draw.text((sx, ty), s['hsl'], font=f_caption, fill=STONE)
        ty += 20
        draw.text((sx, ty), s['cmyk'], font=f_caption, fill=STONE)
        ty += 32
        
        draw.line([(sx, ty - 8), (sx + swatch_w, ty - 8)], fill=(45, 42, 38), width=1)
        draw.text((sx, ty), 'Material Reference:', font=f_micro, fill=CHAMPAGNE)
        ty += 18
        words = s['material'].split()
        line = ''
        for w in words:
            if len(line + w) > 28:
                draw.text((sx, ty), line, font=f_micro, fill=STONE)
                ty += 16
                line = w + ' '
            else:
                line += w + ' '
        if line:
            draw.text((sx, ty), line, font=f_micro, fill=STONE)
            ty += 24

        draw.text((sx, ty), 'Primary Usage:', font=f_micro, fill=CHAMPAGNE)
        ty += 18
        words = s['usage'].split()
        line = ''
        for w in words:
            if len(line + w) > 28:
                draw.text((sx, ty), line, font=f_micro, fill=STONE)
                ty += 16
                line = w + ' '
            else:
                line += w + ' '
        if line:
            draw.text((sx, ty), line, font=f_micro, fill=STONE)

    by = H - margin - 75
    draw.line([(margin + 50, by), (W - margin - 50, by)], fill=(50, 47, 44), width=1)
    draw_tracking_text(draw, 'LUXURY THROUGH RESTRAINT · NO BRIGHT YELLOW GOLD · WCAG AAA CONTRAST CERTIFIED', (W // 2, by + 28), f_caption, CHAMPAGNE, spacing=4, anchor='center')

    out_p = os.path.join(BRAND_DIR, 'color-palette.webp')
    img.save(out_p, 'WEBP', quality=95)
    print(f'Wrote: {out_p}')


# ==============================================================================
# 2. BRAND / TYPOGRAPHY.WEBP
# ==============================================================================
def generate_typography_specimen():
    W, H = 2000, 1350
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(DIDOT, 64, index=0)
    f_h1 = ImageFont.truetype(DIDOT, 56, index=0)
    f_h2 = ImageFont.truetype(DIDOT, 40, index=0)
    f_h3 = ImageFont.truetype(DIDOT, 28, index=0)
    f_body = ImageFont.truetype(HELV, 20, index=0)
    f_body_bold = ImageFont.truetype(HELV, 20, index=1)
    f_small = ImageFont.truetype(HELV, 16, index=0)
    f_caption = ImageFont.truetype(HELV, 13, index=0)
    f_nav = ImageFont.truetype(HELV, 14, index=0)

    margin = 70
    draw.rectangle([margin, margin, W - margin, H - margin], outline=CHAMPAGNE, width=1)
    draw.rectangle([margin + 10, margin + 10, W - margin - 10, H - margin - 10], outline=(40, 38, 36), width=1)

    draw_tracking_text(draw, 'AURELIS', (W // 2, 110), f_title, IVORY, spacing=16, anchor='center')
    draw_tracking_text(draw, 'TYPOGRAPHIC ARCHITECTURE & EDITORIAL HIERARCHY', (W // 2, 190), f_caption, CHAMPAGNE, spacing=6, anchor='center')
    draw.line([(margin + 50, 235), (W - margin - 50, 235)], fill=(50, 47, 44), width=1)

    # 2 Main Columns
    col_w = (W - 2 * margin - 100) // 2
    c1_x = margin + 50
    c2_x = c1_x + col_w + 40
    draw.line([(c2_x - 20, 260), (c2_x - 20, H - margin - 80)], fill=(45, 42, 38), width=1)

    # Column 1: Primary Display Serif
    y = 265
    draw_tracking_text(draw, 'PRIMARY DISPLAY SERIF', (c1_x, y), f_caption, CHAMPAGNE, spacing=4, anchor='left')
    y += 32
    draw.text((c1_x, y), 'Didot / Cinzel Display', font=f_h2, fill=IVORY)
    y += 50
    draw.text((c1_x, y), 'Designed for high-fashion editorial gravitas, high stroke contrast, and sharp delicate serifs.', font=f_small, fill=STONE)
    y += 45

    # Alphabet specimen
    specimen_box = [c1_x, y, c1_x + col_w - 20, y + 140]
    draw.rectangle(specimen_box, fill=CHARCOAL, outline=(55, 52, 48), width=1)
    draw_tracking_text(draw, 'A B C D E F G H I J K L M', ((specimen_box[0] + specimen_box[2]) // 2, y + 22), f_h3, IVORY, spacing=8, anchor='center')
    draw_tracking_text(draw, 'N O P Q R S T U V W X Y Z', ((specimen_box[0] + specimen_box[2]) // 2, y + 60), f_h3, IVORY, spacing=8, anchor='center')
    draw_tracking_text(draw, '0 1 2 3 4 5 6 7 8 9 &amp; — ·', ((specimen_box[0] + specimen_box[2]) // 2, y + 98), f_caption, CHAMPAGNE, spacing=6, anchor='center')
    y += 170

    # Scale in Display
    draw.text((c1_x, y), 'H1 / HERO STATEMENT (64px · 0.15em tracking)', font=f_caption, fill=CHAMPAGNE)
    y += 24
    draw.text((c1_x, y), 'The Art of Scent', font=f_h1, fill=IVORY)
    y += 75

    draw.text((c1_x, y), 'H2 / SECTION HEADLINE (42px · 0.12em tracking)', font=f_caption, fill=CHAMPAGNE)
    y += 24
    draw.text((c1_x, y), 'Crafted for Presence', font=f_h2, fill=IVORY)
    y += 65

    draw.text((c1_x, y), 'H3 / SUBHEADING (28px · 0.08em tracking)', font=f_caption, fill=CHAMPAGNE)
    y += 24
    draw.text((c1_x, y), 'Defined by Detail and Quiet Restraint', font=f_h3, fill=IVORY)
    y += 65

    # Column 2: Supporting Grotesque
    y = 265
    draw_tracking_text(draw, 'SUPPORTING MODERN GROTESQUE', (c2_x, y), f_caption, CHAMPAGNE, spacing=4, anchor='left')
    y += 32
    draw.text((c2_x, y), 'Helvetica Neue / Inter', font=f_h2, fill=IVORY)
    y += 50
    draw.text((c2_x, y), 'Clean, geometric rhythm providing authoritative legibility for body, UI, and technical notes.', font=f_small, fill=STONE)
    y += 45

    spec_box2 = [c2_x, y, c2_x + col_w - 20, y + 140]
    draw.rectangle(spec_box2, fill=CHARCOAL, outline=(55, 52, 48), width=1)
    draw_tracking_text(draw, 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z', ((spec_box2[0] + spec_box2[2]) // 2, y + 26), f_small, IVORY, spacing=4, anchor='center')
    draw_tracking_text(draw, 'a b c d e f g h i j k l m n o p q r s t u v w x y z', ((spec_box2[0] + spec_box2[2]) // 2, y + 60), f_small, STONE, spacing=4, anchor='center')
    draw_tracking_text(draw, '0 1 2 3 4 5 6 7 8 9 · ! @ # $ % ^ &amp; * ( ) - _ + =', ((spec_box2[0] + spec_box2[2]) // 2, y + 94), f_caption, CHAMPAGNE, spacing=3, anchor='center')
    y += 170

    draw.text((c2_x, y), 'BODY TEXT (18px · 1.6 line-height · 0.02em tracking)', font=f_caption, fill=CHAMPAGNE)
    y += 24
    body_sample = 'A contemporary fragrance house that values sensory precision, architectural\nminimalism, and enduring timelessness. NOIR ÉCLAT explores the tension\nbetween raw darkness and radiant golden warmth.'
    for l in body_sample.split('\n'):
        draw.text((c2_x, y), l, font=f_body, fill=STONE)
        y += 28
    y += 20

    draw.text((c2_x, y), 'NAVIGATION &amp; BUTTON SYSTEM', font=f_caption, fill=CHAMPAGNE)
    y += 24
    # Nav Bar preview
    nav_box = [c2_x, y, c2_x + col_w - 20, y + 48]
    draw.rectangle(nav_box, fill=CHARCOAL, outline=(55, 52, 48), width=1)
    draw_tracking_text(draw, 'COLLECTION    ·    FRAGRANCES    ·    ATELIER    ·    CONTACT', ((nav_box[0] + nav_box[2]) // 2, y + 16), f_nav, IVORY, spacing=4, anchor='center')
    y += 68

    # Button preview
    draw.text((c2_x, y), 'BUTTON / CTA COMPONENT', font=f_caption, fill=CHAMPAGNE)
    y += 24
    btn_w, btn_h = 280, 52
    draw.rectangle([c2_x, y, c2_x + btn_w, y + btn_h], fill=IVORY)
    draw_tracking_text(draw, 'EXPLORE NOIR ÉCLAT', (c2_x + btn_w // 2, y + 18), f_caption, OBSIDIAN, spacing=3, anchor='center')

    # Secondary outline button
    btn2_x = c2_x + btn_w + 24
    draw.rectangle([btn2_x, y, btn2_x + btn_w, y + btn_h], fill=None, outline=CHAMPAGNE, width=1)
    draw_tracking_text(draw, 'VIEW SCENT NOTES', (btn2_x + btn_w // 2, y + 18), f_caption, CHAMPAGNE, spacing=3, anchor='center')

    by = H - margin - 75
    draw.line([(margin + 50, by), (W - margin - 50, by)], fill=(50, 47, 44), width=1)
    draw_tracking_text(draw, 'AURELIS DESIGN SYSTEM · 2-TYPEFACE LUXURY HIERARCHY · STRICT OPTICAL KERNING', (W // 2, by + 28), f_caption, CHAMPAGNE, spacing=4, anchor='center')

    out_p = os.path.join(BRAND_DIR, 'typography.webp')
    img.save(out_p, 'WEBP', quality=95)
    print(f'Wrote: {out_p}')


# ==============================================================================
# 3. PRODUCT / PRODUCT-MASTER.WEBP
# ==============================================================================
def generate_product_master():
    W, H = 1800, 2400
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(DIDOT, 46, index=0)
    f_h2 = ImageFont.truetype(DIDOT, 32, index=0)
    f_label_brand = ImageFont.truetype(DIDOT, 24, index=0)
    f_label_name = ImageFont.truetype(HELV, 14, index=1)
    f_label_sub = ImageFont.truetype(HELV, 11, index=0)
    f_body = ImageFont.truetype(HELV, 18, index=0)
    f_caption = ImageFont.truetype(HELV, 14, index=0)
    f_micro = ImageFont.truetype(HELV, 12, index=0)

    # Chiaroscuro studio background glow
    center_y = 1200
    for y in range(H):
        dist = abs(y - center_y) / 1200.0
        r = int(11 + 14 * (1.0 - dist * 0.8))
        g = int(11 + 12 * (1.0 - dist * 0.8))
        b = int(12 + 10 * (1.0 - dist * 0.8))
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Outer border
    m = 60
    draw.rectangle([m, m, W - m, H - m], outline=CHAMPAGNE, width=1)

    # Header
    draw_tracking_text(draw, 'AURELIS', (W // 2, 100), f_title, IVORY, spacing=16, anchor='center')
    draw_tracking_text(draw, 'CANONICAL PRODUCT MASTER SPECIFICATION · NOIR ÉCLAT', (W // 2, 160), f_caption, CHAMPAGNE, spacing=5, anchor='center')
    draw.line([(m + 40, 195), (W - m - 40, 195)], fill=(45, 42, 38), width=1)

    # Center Bottle Coordinates
    bx = W // 2
    by = 560
    bw = 360
    bh = 740

    # Polished Stone Plinth / Ground
    plinth_y = by + bh + 40
    draw.rectangle([bx - 500, plinth_y, bx + 500, plinth_y + 16], fill=(22, 21, 22), outline=(50, 46, 42), width=1)

    # Plinth surface subtle reflection gradient
    for i in range(120):
        alpha = int(45 * (1.0 - i / 120.0))
        draw.line([(bx - 480 + i * 2, plinth_y + 16 + i), (bx + 480 - i * 2, plinth_y + 16 + i)], fill=(20 + alpha // 3, 19 + alpha // 3, 20 + alpha // 4))

    # BOTTLE CAP (Brushed Champagne Brass)
    cap_w = 190
    cap_h = 160
    cap_top = by
    # Base metallic cylinder
    draw.rectangle([bx - cap_w // 2, cap_top, bx + cap_w // 2, cap_top + cap_h], fill=CHAMPAGNE, outline=CHAMPAGNE_LIGHT, width=1)
    # Brushed metal horizontal texture lines & lighting gradients
    for cx in range(bx - cap_w // 2, bx + cap_w // 2):
        t = (cx - (bx - cap_w // 2)) / cap_w
        # highlight on left third
        hl = math.exp(-((t - 0.28) ** 2) / 0.02)
        r = int(203 * (0.7 + 0.3 * t) + 40 * hl)
        g = int(185 * (0.7 + 0.3 * t) + 40 * hl)
        b = int(159 * (0.7 + 0.3 * t) + 40 * hl)
        draw.line([(cx, cap_top + 1), (cx, cap_top + cap_h - 1)], fill=(min(255, r), min(255, g), min(255, b)))

    # Engraved Monogram on Cap Top
    draw.ellipse([bx - 26, cap_top + 35, bx + 26, cap_top + 87], outline=CHAMPAGNE_DARK, width=1)
    draw_tracking_text(draw, 'A', (bx, cap_top + 50), f_label_name, CHAMPAGNE_DARK, spacing=0, anchor='center')
    draw_tracking_text(draw, 'MAGNETIC CLASP', (bx, cap_top + 120), f_micro, (90, 80, 70), spacing=2, anchor='center')

    # BOTTLE NECK & COLLAR
    neck_w = 90
    neck_h = 36
    neck_top = cap_top + cap_h
    draw.rectangle([bx - neck_w // 2, neck_top, bx + neck_w // 2, neck_top + neck_h], fill=(45, 42, 38), outline=CHAMPAGNE, width=1)

    # BOTTLE BODY (Heavy Monolithic Smoked Obsidian Crystal)
    body_top = neck_top + neck_h
    body_w = bw
    body_h = bh - (cap_h + neck_h)
    body_box = [bx - body_w // 2, body_top, bx + body_w // 2, body_top + body_h]

    # Glass Outer Wall (Dark Obsidian with subtle bevel highlights)
    draw.rectangle(body_box, fill=(16, 15, 16), outline=CHAMPAGNE, width=1)

    # Heavy Crystal Base (Solid Glass Bottom Wall - 70px thick)
    base_h = 100
    base_top = body_top + body_h - base_h
    draw.rectangle([bx - body_w // 2, base_top, bx + body_w // 2, body_top + body_h], fill=(24, 23, 25), outline=(50, 46, 42), width=1)

    # Internal Liquid Reservoir (Amber / Cognac Glow)
    res_w = body_w - 48
    res_top = body_top + 28
    res_bottom = base_top - 6
    draw.rectangle([bx - res_w // 2, res_top, bx + res_w // 2, res_bottom], fill=AMBER)
    # Liquid amber gradient & reflections
    for lx in range(bx - res_w // 2, bx + res_w // 2):
        t = (lx - (bx - res_w // 2)) / res_w
        hl = math.exp(-((t - 0.25) ** 2) / 0.03)
        r = int(55 + 65 * hl)
        g = int(36 + 45 * hl)
        b = int(22 + 25 * hl)
        draw.line([(lx, res_top), (lx, res_bottom)], fill=(r, g, b))

    # Glass Chamfer / Vertical Bevel Highlights (Left rim specular line)
    draw.line([(bx - body_w // 2 + 6, body_top + 10), (bx - body_w // 2 + 6, body_top + body_h - 10)], fill=(120, 110, 100), width=2)
    draw.line([(bx + body_w // 2 - 6, body_top + 10), (bx + body_w // 2 - 6, body_top + body_h - 10)], fill=(50, 45, 40), width=1)

    # EMBOSSED WARM IVORY LABEL
    lw = 210
    lh = 290
    lt = body_top + (body_h - base_h) // 2 - lh // 2 + 20
    label_box = [bx - lw // 2, lt, bx + lw // 2, lt + lh]

    # Label paper texture
    draw.rectangle(label_box, fill=IVORY, outline=CHAMPAGNE, width=1)
    # Inner subtle deboss frame
    draw.rectangle([label_box[0] + 8, label_box[1] + 8, label_box[2] - 8, label_box[3] - 8], outline=(220, 215, 205), width=1)

    # Label Typography
    ly = lt + 42
    draw_tracking_text(draw, 'AURELIS', (bx, ly), f_label_brand, OBSIDIAN, spacing=5, anchor='center')
    ly += 45
    draw.line([(bx - 35, ly), (bx + 35, ly)], fill=CHAMPAGNE, width=1)
    ly += 25
    draw_tracking_text(draw, 'NOIR ÉCLAT', (bx, ly), f_label_name, (40, 38, 36), spacing=3, anchor='center')
    ly += 32
    draw_tracking_text(draw, 'EAU DE PARFUM', (bx, ly), f_label_sub, STONE, spacing=2, anchor='center')
    ly += 24
    draw_tracking_text(draw, '100 ML · 3.4 FL. OZ.', (bx, ly), f_label_sub, STONE, spacing=2, anchor='center')
    ly += 40
    draw_tracking_text(draw, 'PARIS', (bx, ly), f_label_sub, CHAMPAGNE_DARK, spacing=4, anchor='center')

    # Side Technical Callouts / Engineering Annotations
    # 1. Cap Callout (Left)
    draw.line([(bx - cap_w // 2 - 10, cap_top + 40), (bx - cap_w // 2 - 140, cap_top + 40)], fill=CHAMPAGNE, width=1)
    draw.text((bx - cap_w // 2 - 340, cap_top + 26), 'CAP SPECIFICATION:', font=f_caption, fill=CHAMPAGNE)
    draw.text((bx - cap_w // 2 - 340, cap_top + 46), 'Brushed Champagne Brass\nMagnetic Neodymium Seal\nMonogram Top Engraving', font=f_micro, fill=STONE)

    # 2. Glass Flacon Callout (Left)
    draw.line([(bx - body_w // 2 - 10, body_top + 160), (bx - body_w // 2 - 140, body_top + 160)], fill=CHAMPAGNE, width=1)
    draw.text((bx - body_w // 2 - 340, body_top + 146), 'FLACON BODY:', font=f_caption, fill=CHAMPAGNE)
    draw.text((bx - body_w // 2 - 340, body_top + 166), 'Heavy Flint Crystal Glass\nSmoked Obsidian Smolder\nMicro-Chamfered Edges', font=f_micro, fill=STONE)

    # 3. Label Callout (Right)
    draw.line([(bx + lw // 2 + 10, lt + 80), (bx + body_w // 2 + 140, lt + 80)], fill=CHAMPAGNE, width=1)
    draw.text((bx + body_w // 2 + 160, lt + 66), 'LABEL SPECIFICATION:', font=f_caption, fill=CHAMPAGNE)
    draw.text((bx + body_w // 2 + 160, lt + 86), '320gsm Warm Ivory Rag Paper\nBlind Letterpress Deboss\nMicro Foil Hairline Rules', font=f_micro, fill=STONE)

    # 4. Base Callout (Right)
    draw.line([(bx + body_w // 2 + 10, base_top + 40), (bx + body_w // 2 + 140, base_top + 40)], fill=CHAMPAGNE, width=1)
    draw.text((bx + body_w // 2 + 160, base_top + 26), 'BASE WEIGHT &amp; PEDESTAL:', font=f_caption, fill=CHAMPAGNE)
    draw.text((bx + body_w // 2 + 160, base_top + 46), 'Ultra-Heavy 70mm Solid Glass Floor\nPolished Black Granite Podium\nMirror Chiaroscuro Reflection', font=f_micro, fill=STONE)

    # Bottom Product Spec Table
    by_spec = H - 420
    draw.line([(m + 60, by_spec), (W - m - 60, by_spec)], fill=(50, 46, 42), width=1)
    draw_tracking_text(draw, 'FLAGSHIP SPECIFICATIONS · NOIR ÉCLAT', (W // 2, by_spec + 25), f_caption, CHAMPAGNE, spacing=4, anchor='center')

    spec_data = [
        ('VOLUME', '100ml / 3.4 Fl. Oz.'),
        ('CONCENTRATION', 'Eau de Parfum (22% Scent Compound)'),
        ('MATERIALS', 'Heavy Flint Glass, Brass, Unbleached Cotton Rag'),
        ('CANONICAL RULE', 'Strict master reference for 3D/AI generation in Stages 2 &amp; 3')
    ]
    sy = by_spec + 70
    for label, val in spec_data:
        draw.text((m + 120, sy), label, font=f_body, fill=CHAMPAGNE)
        draw.text((m + 380, sy), val, font=f_body, fill=IVORY)
        sy += 38

    draw.line([(m + 60, H - 120), (W - m - 60, H - 120)], fill=(50, 46, 42), width=1)
    draw_tracking_text(draw, 'AURELIS CANONICAL DESIGN MASTER · REPRODUCTION FIDELITY LOCKED', (W // 2, H - 95), f_caption, STONE, spacing=3, anchor='center')

    out_p = os.path.join(PRODUCT_DIR, 'product-master.webp')
    img.save(out_p, 'WEBP', quality=95)
    print(f'Wrote: {out_p}')


# ==============================================================================
# 4. PRODUCT / PRODUCT-FRONT.WEBP
# ==============================================================================
def generate_product_front():
    W, H = 1800, 2400
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(DIDOT, 42, index=0)
    f_caption = ImageFont.truetype(HELV, 14, index=0)
    f_label_brand = ImageFont.truetype(DIDOT, 26, index=0)
    f_label_name = ImageFont.truetype(HELV, 15, index=1)
    f_label_sub = ImageFont.truetype(HELV, 11, index=0)

    # Dramatic radial chiaroscuro background
    cx, cy = W // 2, 1100
    for r in range(1200, 0, -8):
        factor = (1.0 - r / 1200.0)
        c_r = int(11 + 18 * factor)
        c_g = int(11 + 16 * factor)
        c_b = int(12 + 14 * factor)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(c_r, c_g, c_b))

    m = 60
    draw.rectangle([m, m, W - m, H - m], outline=CHAMPAGNE, width=1)

    draw_tracking_text(draw, 'AURELIS', (W // 2, 110), f_title, IVORY, spacing=16, anchor='center')
    draw_tracking_text(draw, 'DIRECT FRONT ELEVATION · STUDIO ARCHIVE', (W // 2, 170), f_caption, CHAMPAGNE, spacing=5, anchor='center')
    draw.line([(m + 40, 205), (W - m - 40, 205)], fill=(45, 42, 38), width=1)

    # Front Elevation Bottle
    bx = W // 2
    by = 520
    bw = 420
    bh = 860

    # Polished Pedestal
    plinth_y = by + bh + 40
    draw.rectangle([bx - 550, plinth_y, bx + 550, plinth_y + 20], fill=(20, 19, 20), outline=(50, 46, 42), width=1)
    for i in range(160):
        alpha = int(60 * (1.0 - i / 160.0))
        draw.line([(bx - 530 + i * 2, plinth_y + 20 + i), (bx + 530 - i * 2, plinth_y + 20 + i)], fill=(20 + alpha // 3, 19 + alpha // 3, 20 + alpha // 4))

    # Cap
    cap_w = 220
    cap_h = 180
    cap_top = by
    draw.rectangle([bx - cap_w // 2, cap_top, bx + cap_w // 2, cap_top + cap_h], fill=CHAMPAGNE, outline=CHAMPAGNE_LIGHT, width=1)
    for px in range(bx - cap_w // 2, bx + cap_w // 2):
        t = (px - (bx - cap_w // 2)) / cap_w
        hl = math.exp(-((t - 0.28) ** 2) / 0.015)
        r = int(203 * (0.75 + 0.25 * t) + 45 * hl)
        g = int(185 * (0.75 + 0.25 * t) + 45 * hl)
        b = int(159 * (0.75 + 0.25 * t) + 45 * hl)
        draw.line([(px, cap_top + 1), (px, cap_top + cap_h - 1)], fill=(min(255, r), min(255, g), min(255, b)))

    draw.ellipse([bx - 32, cap_top + 45, bx + 32, cap_top + 105], outline=CHAMPAGNE_DARK, width=1)
    draw_tracking_text(draw, 'A', (bx, cap_top + 62), f_label_name, CHAMPAGNE_DARK, spacing=0, anchor='center')

    # Neck
    neck_w = 100
    neck_h = 42
    neck_top = cap_top + cap_h
    draw.rectangle([bx - neck_w // 2, neck_top, bx + neck_w // 2, neck_top + neck_h], fill=(45, 42, 38), outline=CHAMPAGNE, width=1)

    # Body
    body_top = neck_top + neck_h
    body_w = bw
    body_h = bh - (cap_h + neck_h)
    draw.rectangle([bx - body_w // 2, body_top, bx + body_w // 2, body_top + body_h], fill=(16, 15, 16), outline=CHAMPAGNE, width=1)

    # Base
    base_h = 115
    base_top = body_top + body_h - base_h
    draw.rectangle([bx - body_w // 2, base_top, bx + body_w // 2, body_top + body_h], fill=(24, 23, 25), outline=(50, 46, 42), width=1)

    # Liquid
    res_w = body_w - 56
    res_top = body_top + 32
    res_bottom = base_top - 8
    draw.rectangle([bx - res_w // 2, res_top, bx + res_w // 2, res_bottom], fill=AMBER)
    for lx in range(bx - res_w // 2, bx + res_w // 2):
        t = (lx - (bx - res_w // 2)) / res_w
        hl = math.exp(-((t - 0.25) ** 2) / 0.025)
        r = int(55 + 75 * hl)
        g = int(36 + 50 * hl)
        b = int(22 + 28 * hl)
        draw.line([(lx, res_top), (lx, res_bottom)], fill=(r, g, b))

    # Glass edge vertical specular
    draw.line([(bx - body_w // 2 + 8, body_top + 12), (bx - body_w // 2 + 8, body_top + body_h - 12)], fill=(130, 120, 110), width=2)
    draw.line([(bx + body_w // 2 - 8, body_top + 12), (bx + body_w // 2 - 8, body_top + body_h - 12)], fill=(55, 50, 46), width=1)

    # Label
    lw = 240
    lh = 330
    lt = body_top + (body_h - base_h) // 2 - lh // 2 + 25
    label_box = [bx - lw // 2, lt, bx + lw // 2, lt + lh]
    draw.rectangle(label_box, fill=IVORY, outline=CHAMPAGNE, width=1)
    draw.rectangle([label_box[0] + 8, label_box[1] + 8, label_box[2] - 8, label_box[3] - 8], outline=(220, 215, 205), width=1)

    ly = lt + 48
    draw_tracking_text(draw, 'AURELIS', (bx, ly), f_label_brand, OBSIDIAN, spacing=5, anchor='center')
    ly += 52
    draw.line([(bx - 40, ly), (bx + 40, ly)], fill=CHAMPAGNE, width=1)
    ly += 28
    draw_tracking_text(draw, 'NOIR ÉCLAT', (bx, ly), f_label_name, (40, 38, 36), spacing=3, anchor='center')
    ly += 36
    draw_tracking_text(draw, 'EAU DE PARFUM', (bx, ly), f_label_sub, STONE, spacing=2, anchor='center')
    ly += 28
    draw_tracking_text(draw, '100 ML · 3.4 FL. OZ.', (bx, ly), f_label_sub, STONE, spacing=2, anchor='center')
    ly += 45
    draw_tracking_text(draw, 'PARIS', (bx, ly), f_label_sub, CHAMPAGNE_DARK, spacing=4, anchor='center')

    # Minimal Bottom Footer
    by_foot = H - 180
    draw.line([(m + 60, by_foot), (W - m - 60, by_foot)], fill=(50, 46, 42), width=1)
    draw_tracking_text(draw, '\"THE ART OF SCENT\"', (W // 2, by_foot + 40), f_title, IVORY, spacing=10, anchor='center')
    draw_tracking_text(draw, 'AURELIS LUXURY FRAGRANCE · FRONT VIEW 100ML EAU DE PARFUM', (W // 2, by_foot + 105), f_caption, STONE, spacing=3, anchor='center')

    out_p = os.path.join(PRODUCT_DIR, 'product-front.webp')
    img.save(out_p, 'WEBP', quality=95)
    print(f'Wrote: {out_p}')


# ==============================================================================
# 5. PRODUCT / PRODUCT-DETAIL.WEBP
# ==============================================================================
def generate_product_detail():
    W, H = 1800, 2400
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(DIDOT, 42, index=0)
    f_caption = ImageFont.truetype(HELV, 14, index=0)
    f_label_brand = ImageFont.truetype(DIDOT, 36, index=0)
    f_label_name = ImageFont.truetype(HELV, 22, index=1)
    f_label_sub = ImageFont.truetype(HELV, 16, index=0)
    f_h3 = ImageFont.truetype(DIDOT, 28, index=0)
    f_body = ImageFont.truetype(HELV, 18, index=0)

    # Macro close-up lighting
    for y in range(H):
        dist = abs(y - 900) / 1000.0
        r = int(11 + 22 * (1.0 - dist * 0.7))
        g = int(11 + 18 * (1.0 - dist * 0.7))
        b = int(12 + 15 * (1.0 - dist * 0.7))
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    m = 60
    draw.rectangle([m, m, W - m, H - m], outline=CHAMPAGNE, width=1)
    draw_tracking_text(draw, 'AURELIS', (W // 2, 100), f_title, IVORY, spacing=16, anchor='center')
    draw_tracking_text(draw, 'MACRO MATERIAL &amp; CRAFTSMANSHIP DETAIL', (W // 2, 160), f_caption, CHAMPAGNE, spacing=5, anchor='center')
    draw.line([(m + 40, 195), (W - m - 40, 195)], fill=(45, 42, 38), width=1)

    # Massive Macro Cap &amp; Shoulder
    bx = W // 2
    by = 380

    # Oversized Brushed Champagne Brass Cap
    cap_w = 460
    cap_h = 320
    draw.rectangle([bx - cap_w // 2, by, bx + cap_w // 2, by + cap_h], fill=CHAMPAGNE, outline=CHAMPAGNE_LIGHT, width=2)
    for px in range(bx - cap_w // 2, bx + cap_w // 2):
        t = (px - (bx - cap_w // 2)) / cap_w
        hl = math.exp(-((t - 0.28) ** 2) / 0.015)
        r = int(203 * (0.7 + 0.3 * t) + 48 * hl)
        g = int(185 * (0.7 + 0.3 * t) + 48 * hl)
        b = int(159 * (0.7 + 0.3 * t) + 48 * hl)
        draw.line([(px, by + 1), (px, by + cap_h - 1)], fill=(min(255, r), min(255, g), min(255, b)))

    # Precision Engraved Monogram on Cap
    draw.ellipse([bx - 60, by + 80, bx + 60, by + 200], outline=CHAMPAGNE_DARK, width=2)
    draw_tracking_text(draw, 'A', (bx, by + 115), f_label_brand, CHAMPAGNE_DARK, spacing=0, anchor='center')
    draw_tracking_text(draw, 'MAGNETIC DUAL-ACTION FIT', (bx, by + 260), f_caption, (80, 72, 60), spacing=3, anchor='center')

    # Collar &amp; Neck
    neck_w = 200
    neck_h = 60
    neck_top = by + cap_h
    draw.rectangle([bx - neck_w // 2, neck_top, bx + neck_w // 2, neck_top + neck_h], fill=(45, 42, 38), outline=CHAMPAGNE, width=1)

    # Massive Shoulder &amp; Bottle Upper Portion
    body_top = neck_top + neck_h
    body_w = 820
    body_h = 750
    draw.rectangle([bx - body_w // 2, body_top, bx + body_w // 2, body_top + body_h], fill=(16, 15, 16), outline=CHAMPAGNE, width=2)

    # Liquid Amber Core
    res_w = body_w - 90
    res_top = body_top + 45
    draw.rectangle([bx - res_w // 2, res_top, bx + res_w // 2, body_top + body_h], fill=AMBER)
    for lx in range(bx - res_w // 2, bx + res_w // 2):
        t = (lx - (bx - res_w // 2)) / res_w
        hl = math.exp(-((t - 0.28) ** 2) / 0.03)
        r = int(60 + 85 * hl)
        g = int(38 + 58 * hl)
        b = int(22 + 32 * hl)
        draw.line([(lx, res_top), (lx, body_top + body_h)], fill=(r, g, b))

    # Heavy Glass Shoulder Chamfer &amp; Refraction
    draw.line([(bx - body_w // 2 + 14, body_top + 10), (bx - body_w // 2 + 14, body_top + body_h)], fill=(150, 140, 125), width=3)
    draw.line([(bx + body_w // 2 - 14, body_top + 10), (bx + body_w // 2 - 14, body_top + body_h)], fill=(60, 55, 50), width=2)

    # Macro Textured Paper Label Preview
    lw = 480
    lh = 380
    lt = body_top + 160
    label_box = [bx - lw // 2, lt, bx + lw // 2, lt + lh]
    draw.rectangle(label_box, fill=IVORY, outline=CHAMPAGNE, width=2)
    draw.rectangle([label_box[0] + 12, label_box[1] + 12, label_box[2] - 12, label_box[3] - 12], outline=(220, 215, 205), width=1)

    ly = lt + 50
    draw_tracking_text(draw, 'AURELIS', (bx, ly), f_label_brand, OBSIDIAN, spacing=8, anchor='center')
    ly += 65
    draw.line([(bx - 70, ly), (bx + 70, ly)], fill=CHAMPAGNE, width=2)
    ly += 35
    draw_tracking_text(draw, 'NOIR ÉCLAT', (bx, ly), f_label_name, (40, 38, 36), spacing=4, anchor='center')
    ly += 45
    draw_tracking_text(draw, 'EAU DE PARFUM · 100 ML', (bx, ly), f_label_sub, STONE, spacing=3, anchor='center')
    ly += 36
    draw_tracking_text(draw, 'HAND-BLENDED IN GRASSE', (bx, ly), f_label_sub, STONE, spacing=2, anchor='center')
    ly += 45
    draw_tracking_text(draw, 'PARIS', (bx, ly), f_label_sub, CHAMPAGNE_DARK, spacing=4, anchor='center')

    # Craftsmanship Annotations below
    ay = body_top + body_h + 80
    draw.line([(m + 60, ay), (W - m - 60, ay)], fill=(50, 46, 42), width=1)
    ay += 40

    col_w = (W - 2 * m - 120) // 3
    c1 = m + 60
    c2 = c1 + col_w + 20
    c3 = c2 + col_w + 20

    draw.text((c1, ay), '01 · BRUSHED BRASS', font=f_h3, fill=CHAMPAGNE)
    draw.text((c1, ay + 38), 'Precision-milled cylindrical cap with\nradial brushed finish and heavy neodymium\nmagnetic closure with a satisfying tactile click.', font=f_body, fill=STONE)

    draw.text((c2, ay), '02 · COTTON RAG LABEL', font=f_h3, fill=CHAMPAGNE)
    draw.text((c2, ay + 38), '320gsm warm ivory tactile paper\nfeaturing blind debossed wordmark and\nchampagne micro-foil geometric rules.', font=f_body, fill=STONE)

    draw.text((c3, ay), '03 · SMOKED FLINT GLASS', font=f_h3, fill=CHAMPAGNE)
    draw.text((c3, ay + 38), 'High-density monolithic crystal flacon\nwith precision hand-beveled chamfers\nand luminous amber-cognac inner core.', font=f_body, fill=STONE)

    out_p = os.path.join(PRODUCT_DIR, 'product-detail.webp')
    img.save(out_p, 'WEBP', quality=95)
    print(f'Wrote: {out_p}')


# ==============================================================================
# 6. PRODUCT / PACKAGING.WEBP
# ==============================================================================
def generate_packaging():
    W, H = 2000, 1500
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(DIDOT, 52, index=0)
    f_box_brand = ImageFont.truetype(DIDOT, 38, index=0)
    f_box_name = ImageFont.truetype(HELV, 20, index=1)
    f_box_sub = ImageFont.truetype(HELV, 14, index=0)
    f_h3 = ImageFont.truetype(DIDOT, 30, index=0)
    f_body = ImageFont.truetype(HELV, 18, index=0)
    f_caption = ImageFont.truetype(HELV, 14, index=0)

    # Ambient studio lighting
    for y in range(H):
        dist = abs(y - 750) / 750.0
        r = int(11 + 16 * (1.0 - dist * 0.8))
        g = int(11 + 14 * (1.0 - dist * 0.8))
        b = int(12 + 12 * (1.0 - dist * 0.8))
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    m = 70
    draw.rectangle([m, m, W - m, H - m], outline=CHAMPAGNE, width=1)
    draw_tracking_text(draw, 'AURELIS', (W // 2, 110), f_title, IVORY, spacing=16, anchor='center')
    draw_tracking_text(draw, 'LUXURY PACKAGING &amp; PRESENTATION SUITE · NOIR ÉCLAT', (W // 2, 175), f_caption, CHAMPAGNE, spacing=5, anchor='center')
    draw.line([(m + 40, 215), (W - m - 40, 215)], fill=(45, 42, 38), width=1)

    # Display Stage: Presentation Box on Left, Bottle on Right
    # Ground shadow / surface
    ground_y = 1060
    draw.line([(m + 60, ground_y), (W - m - 60, ground_y)], fill=(40, 36, 32), width=2)
    for i in range(80):
        alpha = int(45 * (1.0 - i / 80.0))
        draw.line([(m + 80 + i * 4, ground_y + i), (W - m - 80 - i * 4, ground_y + i)], fill=(20 + alpha // 3, 19 + alpha // 3, 20 + alpha // 4))

    # 1. RIGID PACKAGING BOX (Deep Charcoal with Matte Velvet Touch)
    box_w = 520
    box_h = 760
    box_x = 520
    box_y = ground_y - box_h

    # Box Outer Shell
    draw.rectangle([box_x - box_w // 2, box_y, box_x + box_w // 2, box_y + box_h], fill=CHARCOAL, outline=(60, 56, 52), width=2)
    # Beveled edge highlight on box lid
    draw.rectangle([box_x - box_w // 2 + 12, box_y + 12, box_x + box_w // 2 - 12, box_y + box_h - 12], outline=(40, 38, 36), width=1)

    # Embossed Champagne Foil Typography on Box
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

    # Monogram blind-embossed at bottom of box
    by_text += 180
    draw.ellipse([box_x - 30, by_text, box_x + 30, by_text + 60], outline=(60, 55, 50), width=1)
    draw_tracking_text(draw, 'A', (box_x, by_text + 15), f_box_sub, (80, 75, 70), spacing=0, anchor='center')

    # 2. CANONICAL BOTTLE Beside Box (Right Side)
    bot_x = 1350
    bot_w = 320
    bot_h = 660
    bot_y = ground_y - bot_h

    # Cap
    cap_w = 160
    cap_h = 130
    draw.rectangle([bot_x - cap_w // 2, bot_y, bot_x + cap_w // 2, bot_y + cap_h], fill=CHAMPAGNE, outline=CHAMPAGNE_LIGHT, width=1)
    for px in range(bot_x - cap_w // 2, bot_x + cap_w // 2):
        t = (px - (bot_x - cap_w // 2)) / cap_w
        hl = math.exp(-((t - 0.28) ** 2) / 0.02)
        r = int(203 * (0.75 + 0.25 * t) + 40 * hl)
        g = int(185 * (0.75 + 0.25 * t) + 40 * hl)
        b = int(159 * (0.75 + 0.25 * t) + 40 * hl)
        draw.line([(px, bot_y + 1), (px, bot_y + cap_h - 1)], fill=(min(255, r), min(255, g), min(255, b)))

    # Neck
    neck_w = 75
    neck_h = 30
    draw.rectangle([bot_x - neck_w // 2, bot_y + cap_h, bot_x + neck_w // 2, bot_y + cap_h + neck_h], fill=(45, 42, 38), outline=CHAMPAGNE, width=1)

    # Body
    b_top = bot_y + cap_h + neck_h
    b_h = bot_h - (cap_h + neck_h)
    draw.rectangle([bot_x - bot_w // 2, b_top, bot_x + bot_w // 2, b_top + b_h], fill=(16, 15, 16), outline=CHAMPAGNE, width=1)

    # Liquid Amber Core
    draw.rectangle([bot_x - (bot_w - 44) // 2, b_top + 24, bot_x + (bot_w - 44) // 2, b_top + b_h - 80], fill=AMBER)

    # Solid Base
    draw.rectangle([bot_x - bot_w // 2, b_top + b_h - 80, bot_x + bot_w // 2, b_top + b_h], fill=(24, 23, 25), outline=(50, 46, 42), width=1)

    # Bottle Label
    blw = 180
    blh = 240
    blt = b_top + (b_h - 80) // 2 - blh // 2 + 10
    draw.rectangle([bot_x - blw // 2, blt, bot_x + blw // 2, blt + blh], fill=IVORY, outline=CHAMPAGNE, width=1)
    draw_tracking_text(draw, 'AURELIS', (bot_x, blt + 35), f_box_sub, OBSIDIAN, spacing=4, anchor='center')
    draw_tracking_text(draw, 'NOIR ÉCLAT', (bot_x, blt + 90), f_caption, (40, 38, 36), spacing=2, anchor='center')
    draw_tracking_text(draw, 'EAU DE PARFUM', (bot_x, blt + 125), f_caption, STONE, spacing=1, anchor='center')

    # Packaging Specifications at Bottom
    by_spec = H - 280
    draw.line([(m + 60, by_spec), (W - m - 60, by_spec)], fill=(50, 46, 42), width=1)
    by_spec += 35

    draw.text((m + 80, by_spec), 'PACKAGING SPECIFICATIONS', font=f_h3, fill=CHAMPAGNE)
    spec_lines = [
        'BOX MATERIAL: 1800gsm rigid Greyboard wrapped in FSC-certified soft-touch Charcoal paper.',
        'FOILING: Hot-stamped muted Champagne alloy foil (#CBB99F) with precision blind debossing.',
        'INTERIOR: Custom laser-cut high-density velvet-flocked obsidian EVA foam insert.',
        'UNBOXING RITUAL: Weighted magnetic friction lid opening with seamless sensory reveal.'
    ]
    sy = by_spec + 45
    for l in spec_lines:
        draw.text((m + 80, sy), '— ' + l, font=f_body, fill=STONE)
        sy += 28

    out_p = os.path.join(PRODUCT_DIR, 'packaging.webp')
    img.save(out_p, 'WEBP', quality=95)
    print(f'Wrote: {out_p}')


# ==============================================================================
# 7. DIRECTION / MOODBOARD.WEBP
# ==============================================================================
def generate_moodboard():
    W, H = 2400, 1600
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(DIDOT, 68, index=0)
    f_h2 = ImageFont.truetype(DIDOT, 38, index=0)
    f_h3 = ImageFont.truetype(DIDOT, 26, index=0)
    f_body = ImageFont.truetype(HELV, 18, index=0)
    f_caption = ImageFont.truetype(HELV, 14, index=0)
    f_micro = ImageFont.truetype(HELV, 12, index=0)

    m = 70
    draw.rectangle([m, m, W - m, H - m], outline=CHAMPAGNE, width=1)
    draw.rectangle([m + 10, m + 10, W - m - 10, H - m - 10], outline=(40, 38, 36), width=1)

    draw_tracking_text(draw, 'AURELIS', (W // 2, 110), f_title, IVORY, spacing=18, anchor='center')
    draw_tracking_text(draw, 'CREATIVE DIRECTION MOODBOARD · SENSORY ATMOSPHERE', (W // 2, 190), f_caption, CHAMPAGNE, spacing=6, anchor='center')
    draw.line([(m + 50, 235), (W - m - 50, 235)], fill=(50, 47, 44), width=1)

    # 6 Curated Atmospheric Panels (3 x 2 Grid)
    grid_top = 265
    grid_h = H - m - 160 - grid_top
    cell_w = (W - 2 * m - 80 - 40) // 3
    cell_h = (grid_h - 20) // 2

    panels = [
        ('01 / DARKNESS', 'The Obsidian Void', 'Deep, enveloping chiaroscuro where forms emerge from liquid shadow rather than bright illumination.'),
        ('02 / LIGHT', 'Chiaroscuro Shafts', 'Narrow razor-sharp beams of warm champagne light slicing through architectural darkness.'),
        ('03 / GLASS', 'Prismatic Refraction', 'Heavy lead-free flint crystal bending light into golden caustic waves across polished stone.'),
        ('04 / TEXTURE', 'Tactile Contrast', 'Rough volcanic basalt, unbleached 320gsm cotton rag, and cold brushed champagne brass.'),
        ('05 / BOTANICALS', 'Scent Origins', 'Cracked Madagascar pink pepper berries, Calabrian bergamot zest, Florentine iris root, and smoky Haitian vetiver.'),
        ('06 / SPACE', 'Architectural Negative Space', 'Expansive quietude where every empty millimeter amplifies the gravity of the product.')
    ]

    for idx, (title, subtitle, desc) in enumerate(panels):
        r = idx // 3
        c = idx % 3
        px = m + 40 + c * (cell_w + 20)
        py = grid_top + r * (cell_h + 20)

        # Panel Box
        draw.rectangle([px, py, px + cell_w, py + cell_h], fill=CHARCOAL, outline=(60, 56, 50), width=1)

        # Visual illustration area inside panel
        img_h = cell_h - 130
        draw.rectangle([px + 12, py + 12, px + cell_w - 12, py + 12 + img_h], fill=(16, 15, 16), outline=(45, 42, 38), width=1)

        # Unique graphic motif for each pillar
        ix = px + 12
        iy = py + 12
        iw = cell_w - 24
        ih = img_h

        if idx == 0:  # Darkness
            for dy in range(ih):
                val = int(10 + 20 * (dy / ih) ** 2)
                draw.line([(ix, iy + dy), (ix + iw, iy + dy)], fill=(val, val, val + 2))
            draw.ellipse([ix + iw // 2 - 50, iy + ih // 2 - 50, ix + iw // 2 + 50, iy + ih // 2 + 50], outline=CHAMPAGNE, width=1)
        elif idx == 1:  # Light
            for dx in range(iw):
                t = dx / iw
                hl = math.exp(-((t - 0.5) ** 2) / 0.04)
                r_c = int(20 + 180 * hl)
                g_c = int(18 + 150 * hl)
                b_c = int(15 + 110 * hl)
                draw.line([(ix + dx, iy), (ix + dx, iy + ih)], fill=(r_c, g_c, b_c))
        elif idx == 2:  # Glass
            # Faceted geometric prism
            draw.polygon([(ix + iw // 2, iy + 25), (ix + iw - 40, iy + ih - 30), (ix + 40, iy + ih - 30)], outline=CHAMPAGNE, fill=(28, 26, 28))
            draw.line([(ix + iw // 2, iy + 25), (ix + iw // 2, iy + ih - 30)], fill=CHAMPAGNE_LIGHT, width=2)
            draw.line([(ix + iw // 2, iy + 25), (ix + iw // 2 + 80, iy + ih - 30)], fill=(80, 70, 55), width=1)
        elif idx == 3:  # Texture
            # Material bands
            b_h = ih // 3
            draw.rectangle([ix, iy, ix + iw, iy + b_h], fill=(35, 33, 32))  # Basalt
            draw.rectangle([ix, iy + b_h, ix + iw, iy + 2 * b_h], fill=IVORY)  # Cotton paper
            draw.rectangle([ix, iy + 2 * b_h, ix + iw, iy + ih], fill=CHAMPAGNE)  # Brass
            draw.text((ix + 16, iy + 10), 'VOLCANIC BASALT', font=f_micro, fill=STONE)
            draw.text((ix + 16, iy + b_h + 10), 'COTTON RAG 320GSM', font=f_micro, fill=OBSIDIAN)
            draw.text((ix + 16, iy + 2 * b_h + 10), 'BRUSHED BRASS', font=f_micro, fill=OBSIDIAN)
        elif idx == 4:  # Botanicals
            # Stylized botanical circles
            draw.ellipse([ix + 60, iy + ih // 2 - 40, ix + 140, iy + ih // 2 + 40], outline=CHAMPAGNE, width=1)
            draw.text((ix + 76, iy + ih // 2 - 8), 'IRIS', font=f_micro, fill=IVORY)
            draw.ellipse([ix + iw // 2 - 40, iy + ih // 2 - 40, ix + iw // 2 + 40, iy + ih // 2 + 40], outline=CHAMPAGNE, width=1)
            draw.text((ix + iw // 2 - 28, iy + ih // 2 - 8), 'PEPPER', font=f_micro, fill=IVORY)
            draw.ellipse([ix + iw - 140, iy + ih // 2 - 40, ix + iw - 60, iy + ih // 2 + 40], outline=CHAMPAGNE, width=1)
            draw.text((ix + iw - 130, iy + ih // 2 - 8), 'VETIVER', font=f_micro, fill=IVORY)
        elif idx == 5:  # Space
            # Vast minimalist frame
            draw.rectangle([ix + 40, iy + 30, ix + iw - 40, iy + ih - 30], outline=(60, 56, 50), width=1)
            draw_tracking_text(draw, 'SILENCE', (ix + iw // 2, iy + ih // 2 - 10), f_caption, CHAMPAGNE, spacing=6, anchor='center')

        # Typography below image
        ty = py + img_h + 24
        draw.text((px + 14, ty), title, font=f_h3, fill=CHAMPAGNE)
        ty += 32
        draw.text((px + 14, ty), subtitle, font=f_caption, fill=IVORY)
        ty += 24
        # Wrap desc
        words = desc.split()
        line = ''
        for w in words:
            if len(line + w) > 42:
                draw.text((px + 14, ty), line, font=f_micro, fill=STONE)
                ty += 16
                line = w + ' '
            else:
                line += w + ' '
        if line:
            draw.text((px + 14, ty), line, font=f_micro, fill=STONE)

    # Bottom Campaign Banner
    by = H - m - 75
    draw.line([(m + 50, by), (W - m - 50, by)], fill=(50, 47, 44), width=1)
    draw_tracking_text(draw, '\"THE ART OF SCENT\" · CRAFTED FOR PRESENCE · DEFINED BY DETAIL', (W // 2, by + 28), f_caption, CHAMPAGNE, spacing=5, anchor='center')

    out_p = os.path.join(DIRECTION_DIR, 'moodboard.webp')
    img.save(out_p, 'WEBP', quality=95)
    print(f'Wrote: {out_p}')


# ==============================================================================
# 8. DIRECTION / ART-DIRECTION.WEBP
# ==============================================================================
def generate_art_direction():
    W, H = 2400, 1600
    img = Image.new('RGB', (W, H), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(DIDOT, 68, index=0)
    f_h2 = ImageFont.truetype(DIDOT, 36, index=0)
    f_h3 = ImageFont.truetype(DIDOT, 26, index=0)
    f_body = ImageFont.truetype(HELV, 18, index=0)
    f_body_bold = ImageFont.truetype(HELV, 18, index=1)
    f_caption = ImageFont.truetype(HELV, 14, index=0)
    f_micro = ImageFont.truetype(HELV, 12, index=0)

    m = 70
    draw.rectangle([m, m, W - m, H - m], outline=CHAMPAGNE, width=1)
    draw.rectangle([m + 10, m + 10, W - m - 10, H - m - 10], outline=(40, 38, 36), width=1)

    draw_tracking_text(draw, 'AURELIS', (W // 2, 110), f_title, IVORY, spacing=18, anchor='center')
    draw_tracking_text(draw, 'CINEMATIC ART DIRECTION &amp; STUDIO LIGHTING PROTOCOL', (W // 2, 190), f_caption, CHAMPAGNE, spacing=6, anchor='center')
    draw.line([(m + 50, 235), (W - m - 50, 235)], fill=(50, 47, 44), width=1)

    # 3 Main Columns
    col_w = (W - 2 * m - 100) // 3
    c1 = m + 40
    c2 = c1 + col_w + 25
    c3 = c2 + col_w + 25

    draw.line([(c2 - 12, 260), (c2 - 12, H - m - 80)], fill=(45, 42, 38), width=1)
    draw.line([(c3 - 12, 260), (c3 - 12, H - m - 80)], fill=(45, 42, 38), width=1)

    # Column 1: Chiaroscuro Lighting Engine
    y = 265
    draw_tracking_text(draw, '01 / LIGHTING ENGINE', (c1, y), f_caption, CHAMPAGNE, spacing=4, anchor='left')
    y += 32
    draw.text((c1, y), 'Studio Chiaroscuro Protocol', font=f_h2, fill=IVORY)
    y += 55

    # Studio Schematic Box
    s_box = [c1, y, c1 + col_w - 20, y + 360]
    draw.rectangle(s_box, fill=CHARCOAL, outline=(60, 56, 50), width=1)

    # Draw Studio Top-Down Setup
    scx = (s_box[0] + s_box[2]) // 2
    scy = (s_box[1] + s_box[3]) // 2 - 20

    # Subject Flacon in center
    draw.rectangle([scx - 20, scy - 15, scx + 20, scy + 15], fill=IVORY, outline=CHAMPAGNE, width=1)
    draw_tracking_text(draw, 'SUBJECT', (scx, scy - 4), f_micro, OBSIDIAN, spacing=1, anchor='center')

    # Key Light (45° Honeycomb Grid Softbox)
    draw.line([(scx - 120, scy + 100), (scx - 40, scy + 30)], fill=CHAMPAGNE, width=2)
    draw.rectangle([scx - 160, scy + 90, scx - 110, scy + 130], fill=AMBER_LIGHT, outline=CHAMPAGNE, width=1)
    draw.text((scx - 190, scy + 140), 'KEY: 45° GRID SOFTBOX', font=f_micro, fill=CHAMPAGNE)

    # Rim Light (Edge Strip Softbox for Glass Contour)
    draw.line([(scx + 130, scy - 80), (scx + 30, scy - 20)], fill=CHAMPAGNE_LIGHT, width=2)
    draw.rectangle([scx + 120, scy - 120, scx + 160, scy - 70], fill=(80, 70, 55), outline=CHAMPAGNE_LIGHT, width=1)
    draw.text((scx + 60, scy - 140), 'RIM: 1x4 STRIP SOFTBOX', font=f_micro, fill=CHAMPAGNE_LIGHT)

    # Negative Fill Flags (Obsidian Foamcore)
    draw.rectangle([scx - 110, scy - 50, scx - 90, scy + 30], fill=(10, 10, 10), outline=(50, 48, 45), width=1)
    draw.text((scx - 140, scy - 70), 'OBSIDIAN FLAG', font=f_micro, fill=STONE)

    # Camera Position
    draw.polygon([(scx - 15, scy + 130), (scx + 15, scy + 130), (scx, scy + 110)], fill=IVORY)
    draw.text((scx - 30, scy + 140), 'CAM 90mm', font=f_micro, fill=IVORY)

    y += 390
    draw.text((c1, y), 'Lighting Commandments:', font=f_h3, fill=CHAMPAGNE)
    y += 38
    rules_l = [
        ('NEVER FLOOD THE SCENE', 'At least 55% of the frame must remain in deep chiaroscuro.'),
        ('SCULPT THE GLASS', 'Use narrow rim highlights to trace the beveled glass edge.'),
        ('AMBER INNER GLOW', 'Backlight must excite the warm liquid without blowing out.'),
        ('NO CHEAP REFLECTIONS', 'Use polished dark granite with falloff, not mirror plastic.')
    ]
    for r_t, r_d in rules_l:
        draw.text((c1, y), '— ' + r_t, font=f_body_bold, fill=IVORY)
        y += 24
        draw.text((c1 + 20, y), r_d, font=f_caption, fill=STONE)
        y += 32

    # Column 2: Camera, Optics & Composition
    y = 265
    draw_tracking_text(draw, '02 / OPTICS &amp; COMPOSITION', (c2, y), f_caption, CHAMPAGNE, spacing=4, anchor='left')
    y += 32
    draw.text((c2, y), 'Camera &amp; Editorial Framing', font=f_h2, fill=IVORY)
    y += 55

    cam_box = [c2, y, c2 + col_w - 20, y + 360]
    draw.rectangle(cam_box, fill=CHARCOAL, outline=(60, 56, 50), width=1)

    cy_m = y + 30
    specs = [
        ('FOCAL LENGTH', '85mm – 100mm Prime Macro (zero barrel distortion)'),
        ('APERTURE', 'f/8 – f/11 for edge-to-edge product sharpness'),
        ('ASPECT RATIOS', '4:5 (Instagram) · 9:16 (Commercial Story) · 16:9 (Hero Web)'),
        ('NEGATIVE SPACE', 'Minimum 40% open space for editorial gravitas'),
        ('POINT OF FOCUS', 'Sharp focus locked onto embossed warm ivory label'),
        ('HORIZON LINE', 'Low camera elevation (5° below bottle equator)')
    ]
    for s_label, s_val in specs:
        draw.text((c2 + 20, cy_m), s_label, font=f_body_bold, fill=CHAMPAGNE)
        cy_m += 24
        draw.text((c2 + 20, cy_m), s_val, font=f_caption, fill=IVORY)
        cy_m += 34

    y += 390
    draw.text((c2, y), 'Framing Grid Standard:', font=f_h3, fill=CHAMPAGNE)
    y += 38
    rules_c = [
        ('MONOLITHIC CENTER', 'Hero bottle commands the optical center with architectural gravity.'),
        ('GOLDEN SPIRAL OFFSET', 'When paired with typography, bottle anchors the right third.'),
        ('TACTILE MACRO CUTS', 'Tight crops on the brushed cap, glass shoulder, and paper grain.')
    ]
    for r_t, r_d in rules_c:
        draw.text((c2, y), '— ' + r_t, font=f_body_bold, fill=IVORY)
        y += 24
        draw.text((c2 + 20, y), r_d, font=f_caption, fill=STONE)
        y += 32

    # Column 3: Commercial Video & AI Motion Pacing
    y = 265
    draw_tracking_text(draw, '03 / MOTION &amp; COMMERCIAL', (c3, y), f_caption, CHAMPAGNE, spacing=4, anchor='left')
    y += 32
    draw.text((c3, y), 'AI Commercial Direction', font=f_h2, fill=IVORY)
    y += 55

    ad_box = [c3, y, c3 + col_w - 20, y + 360]
    draw.rectangle(ad_box, fill=CHARCOAL, outline=(60, 56, 50), width=1)

    ay_m = y + 30
    ad_specs = [
        ('CAMERA MOVEMENT', 'Slow, hypnotic, linear dolly moves (zero jerky panning)'),
        ('LIGHT BEAM DYNAMICS', 'Slow sweeping champagne rim light revealing silhouette'),
        ('TEXTURE CLOSE-UPS', 'Micro liquid amber refractions &amp; slow-motion smoke veil'),
        ('ATMOSPHERE', 'Suspended micro-particulate illuminated by low-angle beam'),
        ('COLOR GRADING', 'Kodak 5219 film emulation with deep obsidian blacks'),
        ('AUDIO PROFILE', 'Sub-bass resonance, crystal resonance, whispered voiceover')
    ]
    for a_label, a_val in ad_specs:
        draw.text((c3 + 20, ay_m), a_label, font=f_body_bold, fill=CHAMPAGNE)
        ay_m += 24
        draw.text((c3 + 20, ay_m), a_val, font=f_caption, fill=IVORY)
        ay_m += 34

    y += 390
    draw.text((c3, y), 'Campaign Continuity Rule:', font=f_h3, fill=CHAMPAGNE)
    y += 38
    rules_a = [
        ('IDENTICAL FLACON', 'Stage 2 &amp; 3 assets must utilize the exact master geometry.'),
        ('CONSISTENT MOOD', 'Every visual must feel like one cohesive high-fashion campaign.'),
        ('RESTRAINED LUXURY', 'No bright neon colors, no loud animations, no generic tropes.')
    ]
    for r_t, r_d in rules_a:
        draw.text((c3, y), '— ' + r_t, font=f_body_bold, fill=IVORY)
        y += 24
        draw.text((c3 + 20, y), r_d, font=f_caption, fill=STONE)
        y += 32

    by = H - m - 75
    draw.line([(m + 50, by), (W - m - 50, by)], fill=(50, 47, 44), width=1)
    draw_tracking_text(draw, 'AURELIS MASTER ART DIRECTION · SOURCE OF TRUTH FOR STAGES 1, 2, AND 3', (W // 2, by + 28), f_caption, CHAMPAGNE, spacing=5, anchor='center')

    out_p = os.path.join(DIRECTION_DIR, 'art-direction.webp')
    img.save(out_p, 'WEBP', quality=95)
    print(f'Wrote: {out_p}')


if __name__ == '__main__':
    print("Beginning visual asset generation for AURELIS Stage 1...")
    generate_color_palette()
    generate_typography_specimen()
    generate_product_master()
    generate_product_front()
    generate_product_detail()
    generate_packaging()
    generate_moodboard()
    generate_art_direction()
    print("All AURELIS Stage 1 visual assets generated successfully!")
