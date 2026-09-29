# AURELIS NOIR ÉCLAT — PRODUCT MASTER SPECIFICATION
## STAGE 3.1: SINGLE SOURCE OF TRUTH & VISUAL SYSTEM

```text
BRAND:             AURELIS
PRODUCT:           NOIR ÉCLAT
CATEGORY:          Eau de Parfum
PRESENTATION:      100 ML · 3.4 FL. OZ. · PARIS
DESIGN ARCHIVE:    PIXIVO Flagship Case Study
CANONICAL STATUS:  LOCKED · SINGLE SOURCE OF TRUTH
```

---

## 1. EXECUTIVE PURPOSE & ARCHITECTURAL IMMUTABILITY

> [!IMPORTANT]
> **THE SINGLE SOURCE OF TRUTH RULE**
> This document and the associated asset suite in `projects/aurelis/assets/product-master/` and `projects/aurelis/assets/photography/` establish the **sole canonical reference** for the AURELIS NOIR ÉCLAT fragrance flacon.
> 
> Every future visual asset—including Stage 3.2 social media campaign creatives, Stage 3.3 AI diffusion commercial shots, and Stage 3.4 PIXIVO portfolio integration—must be derived from this exact product definition without geometric, typographic, or material deviation.

---

## 2. CANONICAL PRODUCT GEOMETRY & MATERIALS

### 2.1 Flacon Architecture
* **Silhouette**: Monolithic rectangular geometry engineered with crisp 45° micro-chamfered edge bevels that catch directional light.
* **Proportions**: Aspect ratio of 1:2.05 (Width: 430px, Height: 880px equivalent).
* **Glass Composition**: Smoked obsidian outer flint glass with controlled optical transparency fading towards the center.
* **Solid Glass Foundation**: Weighted 70mm solid crystal base establishing optical grounding, physical gravity, and rich caustic refraction.
* **Neck Architecture**: Dark gunmetal-toned cylindrical collar (`#2A2724`) providing a seamless transition between the glass shoulder and brass cap.

### 2.2 Cap Architecture
* **Material**: Solid cylindrical brushed champagne brass (`#CBB99F`) with radial micro-grain texture.
* **Specular Highlight**: Focused vertical highlight band at 28% from the light source edge.
* **Apex Detailing**: Engraved architectural monogram medallion (`A`) recessed into the circular top surface.
* **Closure Mechanism**: Precision dual-action magnetic snap fit.

### 2.3 Liquid Core & Olfactory Resonance
* **Hue**: Translucent cognac / glowing amber resin (`#5A3C20` base, scaling to `#D49545` under direct rim lighting).
* **Optical Behavior**: Glows warmly from within the smoked glass cavity when backlit, evoking warmth, intimacy, and resinous depth.

### 2.4 Label Specifications
* **Substrate**: 320gsm unbleached warm ivory fine cotton rag paper (`#F7F5F0`).
* **Placement**: Centered on the lower-middle third of the bottle face with an internal hairline border.
* **Typographic Hierarchy**:
  1. `AURELIS`: Bespoke high-contrast Didot serif wordmark with wide letter-spacing (`0.14em`), blind letterpress debossed.
  2. Accent Line: Centered 1px champagne metallic hairline divider (`#CBB99F`).
  3. `NOIR ÉCLAT`: Clean grotesque sans-serif in charcoal (`#282624`) with `0.18em` letter-spacing.
  4. `EAU DE PARFUM`: Supporting grotesque in warm stone (`#8C857B`) with `0.22em` letter-spacing.
  5. `100 ML · 3.4 FL. OZ.`: Specification text in warm stone (`#8C857B`).
  6. `PARIS`: Origin designation in dark champagne (`#968269`) with ultra-wide tracking (`0.32em`).

---

## 3. COLOR PALETTE SPECIFICATION

| Swatch | Color Name | HEX Code | RGB | Role & Application |
| :---: | :--- | :--- | :--- | :--- |
| ![#0B0B0C](https://via.placeholder.com/15/0B0B0C/000000?text=+) | **Obsidian** | `#0B0B0C` | `11, 11, 12` | Primary void, background canvas, flacon outer glass |
| ![#1A1918](https://via.placeholder.com/15/1A1918/000000?text=+) | **Deep Charcoal** | `#1A1918` | `26, 25, 24` | Rigid presentation box, secondary depth shadows |
| ![#8C857B](https://via.placeholder.com/15/8C857B/000000?text=+) | **Warm Stone** | `#8C857B` | `140, 133, 123` | Secondary label copy, subtle dividers |
| ![#CBB99F](https://via.placeholder.com/15/CBB99F/000000?text=+) | **Champagne** | `#CBB99F` | `203, 185, 159` | Brushed brass cap, micro-foil hairlines, borders |
| ![#F7F5F0](https://via.placeholder.com/15/F7F5F0/000000?text=+) | **Warm Ivory** | `#F7F5F0` | `247, 245, 240` | Cotton rag label substrate, display typography |
| ![#5A3C20](https://via.placeholder.com/15/5A3C20/000000?text=+) | **Cognac Amber** | `#5A3C20` | `90, 60, 32` | Translucent glowing liquid fragrance core |

---

## 4. APPROVED PRODUCT MASTER ASSET INVENTORY

All master assets are locked in `projects/aurelis/assets/product-master/`:

| Filename | Resolution | Description & Approved Use |
| :--- | :---: | :--- |
| `aurelis-noir-eclat-front-master.webp` | `1800×2400` | **Primary Front Master Elevation**. Straight-on studio camera, centered, neutral chiaroscuro background. Primary reference for all digital and 3D modeling. |
| `aurelis-noir-eclat-angle-left.webp` | `1800×2400` | **3/4 Perspective Left View**. Shows front label, left glass depth, chamfered corner reflection, and cap curvature. |
| `aurelis-noir-eclat-angle-right.webp` | `1800×2400` | **3/4 Perspective Right View**. Shows front label, right glass depth, amber internal caustics, and cap curvature. |
| `aurelis-noir-eclat-side.webp` | `1800×2400` | **Profile Side Elevation (90°)**. Direct side view showing glass thickness, solid 70mm crystal base profile, and cylindrical cap silhouette. |
| `aurelis-noir-eclat-macro.webp` | `1800×2400` | **Macro Shoulder & Glass Detail**. Extreme close-up of 45° chamfered glass, luminous cognac liquid, and upper label border. |
| `aurelis-noir-eclat-cap-detail.webp` | `1800×2400` | **Macro Cap Craftsmanship Detail**. Extreme close-up of brushed champagne brass cylinder, radial micro-grain, and monogram apex medallion. |
| `aurelis-noir-eclat-label-detail.webp` | `1800×2400` | **Macro Label Substrate Detail**. Extreme close-up of 320gsm cotton rag paper texture, debossed Didot serif wordmark, and hairline divider. |
| `aurelis-noir-eclat-packaging.webp` | `2000×1500` | **Packaging Presentation Suite**. Rigid soft-touch charcoal presentation box with hot-stamped champagne lettering beside the canonical bottle. |
| `aurelis-product-master-board.webp` | `2400×1600` | **Consolidated Master Specification Board**. Comprehensive visual board containing front elevation, material specs, color swatches, and immutable rules. |

---

## 5. APPROVED HERO PRODUCT PHOTOGRAPHY SUITE

All photographic assets are locked in `projects/aurelis/assets/photography/`:

| Directory & Filename | Resolution | Concept & Purpose |
| :--- | :---: | :--- |
| `hero/aurelis-noir-eclat-hero-portrait.webp` | `1600×2000` (4:5) | **Image 01 — Hero Portrait**. Bottle standing alone in vast obsidian negative space with warm amber backlight. *Designated primary hero visual for website and case study header.* |
| `architectural/aurelis-noir-eclat-architectural-studio.webp` | `1600×2000` (4:5) | **Image 02 — Architectural Studio**. Bottle on stepped dark basalt/granite blocks, emphasizing geometry, crisp linear shadows, and optical reflection. |
| `amber/aurelis-noir-eclat-warm-amber.webp` | `1600×2000` (4:5) | **Image 03 — Warm Amber**. Intimate, warm golden illumination radiating from the liquid reservoir, communicating sensory amber warmth. |
| `macro/aurelis-noir-eclat-macro-craftsmanship.webp` | `1600×2000` (4:5) | **Image 04 — Macro Craftsmanship**. Shallow depth-of-field close-up focusing on cold brushed brass, engraved monogram, and chamfered glass edges. |
| `editorial/aurelis-noir-eclat-editorial-side.webp` | `1600×2000` (4:5) | **Image 05 — Editorial Side Composition**. Asymmetrical composition with the bottle on the right third, leaving vast negative space on the left for editorial typography. |
| `cinematic/aurelis-noir-eclat-dark-cinematic.webp` | `1600×2000` (4:5) | **Image 06 — Dark Cinematic**. High-contrast chiaroscuro with the bottle emerging from velvety shadow, sculpted by a razor-thin 3200K champagne rim light. *Visual anchor for AI commercial.* |
| `tactile/aurelis-noir-eclat-tactile-material.webp` | `1600×2000` (4:5) | **Image 07 — Tactile Material**. Juxtaposition of smooth crystal glass against raw architectural volcanic rock and fine cotton paper. |
| `campaign-master/aurelis-noir-eclat-campaign-master.webp` | `1600×2000` (4:5) | **Image 08 — Campaign Master**. The definitive flagship key visual uniting chiaroscuro lighting, caustics, overhead brand lockup, and campaign quote. *Designated primary campaign visual for Stage 3.2 and Stage 3.3.* |

---

## 6. IMMUTABLE "DO-NOT-CHANGE" RULES

To guarantee absolute visual consistency across all future stages:

1. **Geometry Lock**: Under no circumstances should the rectangular proportions, chamfered corner radius, cap cylinder diameter, or label height be modified.
2. **Color Purity**: Use strictly muted warm Champagne (`#CBB99F`). Never introduce saturated yellow gold, brassy yellow, or neon accents.
3. **No Decorative Clutter**: Forbidden elements include loose rose petals, scattered fruit, artificial fog/smoke clouds, generic marble swirl textures, and floating perfume droplets.
4. **Chiaroscuro Discipline**: Every composition must maintain at least 50% deep obsidian shadow (`#0B0B0C`) to preserve quiet luxury and high-fashion gravitas.
5. **Exact Typography**: The label copy is strictly locked to:
   - `AURELIS`
   - `NOIR ÉCLAT`
   - `EAU DE PARFUM`
   - `100 ML · 3.4 FL. OZ.`
   - `PARIS`
