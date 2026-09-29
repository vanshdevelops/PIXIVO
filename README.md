# PIXIVO — Production-Oriented Creative & Digital Experience Agency Website

> **"Where Vision Meets Motion"**  
> *Strategic Digital Experiences for Ambitious Brands*

A production-oriented, high-performance static agency website crafted for **PIXIVO**. Built strictly with semantic **HTML5**, modern **CSS3** (with bespoke design tokens and fluid responsive typography), and vanilla **JavaScript** — zero external frameworks or heavy dependencies required.

---

## 📁 Project Structure

```
PIXIVO.org/
│
├── index.html                   # Semantic structure, accessible markup, SEO & Open Graph tags
├── styles.css                   # Design tokens, CSS animations, responsive breakpoints (320px–1920px+)
├── script.js                    # Interactions, calculator, modals, contact architecture
├── README.md                    # Full documentation & configuration guide
│
├── assets/
│   ├── logo.svg                 # Master vector logo
│   ├── logo.png                 # Transparent high-resolution PNG master
│   ├── logo.webp                # Optimized WebP raster
│   ├── logo-mark.svg            # Standalone vector icon mark
│   ├── favicon.svg              # Modern SVG favicon for browser tabs
│   ├── favicon.png              # PNG fallback favicon
│   ├── og-image.png             # 1200×630 Open Graph & Twitter social card
│   ├── founder.jpg              # Founder photography
│   ├── cofounder-placeholder.svg # Co-founder avatar placeholder
│   └── portfolio/
│       ├── project-1.jpg        # Nova Coffee (Web Design & E-Commerce concept)
│       ├── project-2.jpg        # Aurelia (Luxury Brand Identity concept)
│       ├── project-3.jpg        # Vanta AI (AI Product Advertisement concept)
│       ├── project-4.jpg        # Luma Sound (Social Media Campaign concept)
│       ├── project-5.jpg        # Axiom Pay (3D Motion & Logo System concept)
│       └── project-6.jpg        # Nexa Mobility (Product Launch Creatives concept)
│
└── projects/
    └── aurelis/                 # PIXIVO Flagship Self-Initiated Concept Case Study
        ├── index.html           # AURELIS experiential showcase
        ├── styles.css           # AURELIS design & luxury styling
        ├── script.js            # AURELIS interactive behaviors
        ├── aurelis-motion.css   # Motion & warm luxury color enhancements
        ├── aurelis-motion.js    # Kinetic interactions
        └── assets/
            ├── editorial/       # Brand board, color palette, moodboard, editorial layouts
            ├── icons/           # Navigation & playback SVGs
            ├── logo/            # Primary logos & monogram marks
            ├── photography/     # Campaign masters, editorial, architectural, macro
            ├── product/         # NOIR ÉCLAT, ÉCLAT, and AMBRE product photography
            ├── product-master/  # Canonical product specification renders
            ├── social/          # Social campaign masters & previews
            └── video/           # 4-shot commercial MP4, poster, storyboard specification
```

---

## 🚀 Getting Started

### 1. Local Development Server
To preview the website locally using Python's built-in HTTP server:

```bash
# From the project root (PIXIVO.org/)
python3 -m http.server 8000
```

Open your browser and navigate to:
`http://localhost:8000/`

To test the AURELIS Flagship Case Study directly:
`http://localhost:8000/projects/aurelis/`

---

## 🎨 Visual Identity & Motion System

- **Official PIXIVO Logo**: Keyed transparent mark rendered cleanly across all surface elevations without ugly bounding boxes.
- **Color Palette**: Deep obsidian surface elevation (`#070709`, `#0e0e13`, `#161622`) accented with signature logo tones:
  - Cyan (`#00f0ff`)
  - Electric Blue (`#3a86ff`)
  - Purple (`#7209b7`)
  - Magenta / Pink (`#f72585`)
  - Subtle Gold (`#ffd166`)
- **Interactive Cursor**: Hardware-accelerated desktop cursor with `requestAnimationFrame`, automatically disabled on touch devices and respects reduced-motion preferences.
- **Reduced Motion**: Native compliance with `prefers-reduced-motion: reduce`. Particle loops, transitions, and transforms gracefully yield to accessible, static layouts.

---

## 📬 Contact Form & Endpoint Configuration

The website utilizes a clean, configurable endpoint architecture isolated in `script.js`:

```javascript
const PIXIVO_CONFIG = {
  // Remote HTTPS POST endpoint for contact inquiries
  contactEndpoint: '',

  // Remote HTTPS endpoint for newsletter subscriptions
  newsletterEndpoint: ''
};
```

### Development vs. Production State:

1. **Unconfigured Endpoint (Current State)**:
   - Form validates all fields (Name, Email, Phone, Discipline, Budget, Details).
   - Informs visitors truthfully that the automated online endpoint is undergoing configuration.
   - Provides direct, actionable fallbacks to `connect.pixivo@gmail.com` and the official **Google Form Project Brief**.
   - Preserves form input fields upon submission so user data is never lost.
   - **Zero personal lead data is written to localStorage or logged to console.**

2. **Connecting a Production Endpoint**:
   Supply your preferred remote HTTPS URL in `script.js`:
   - **Formspree / Formspark**: `'https://formspree.io/f/YOUR_FORM_ID'`
   - **Netlify Forms**: Post to `'/'` with encoded form payload.
   - **Custom Backend / Serverless Function**: `'https://api.yourdomain.com/v1/inquiries'`

When configured, the client dispatches an HTTPS POST request, manages accessible loading states (`aria-busy`), prevents repeated submissions, and confirms receipt only after receiving an HTTP 200/OK response.

---

## 🧮 Interactive Pricing Calculator

Located in the **Pricing** section:
- Prospective clients can toggle checkboxes across all 8 core services.
- Real-time calculation shows standard investment, introductory discount savings, and final estimated scope.
- Clicking **"Start My Project"** automatically transfers chosen services to the consultation form.

---

## 🔍 SEO & Accessibility Implementation

- **Semantic Hierarchy**: Single `<h1>` per page, validated section landmarks, native `<button>` and `<a>` interactive elements.
- **Keyboard Navigation**: All portfolio cards and interactive elements are keyboard focusable with high-visibility cyan focus outlines (`:focus-visible`).
- **Modal Focus Management**: Case study modal captures focus upon opening, enforces keyboard trap, closes on Escape, and restores focus to the triggering element.
- **Structured Data**: Valid JSON-LD `Organization` schema embedded in `<head>`.
- **Open Graph & Twitter Cards**: Complete 1200×630 metadata tags configured for social sharing.

---

## 🌐 Production Readiness Status

| Component | Status | Details |
|---|---|---|
| Visual Design System | **VERIFIED** | Obsidian dark aesthetic, fluid typography, locked brand identity |
| AURELIS Flagship Route | **VERIFIED** | Relative HTTP navigation between homepage and `./projects/aurelis/` |
| Credibility Hardening | **VERIFIED** | Unsupported performance claims replaced with factual creative deliverables |
| Testimonials | **VERIFIED** | Replaced with structured "How We Work" studio methodology |
| Security | **VERIFIED** | Hardcoded credentials, pseudo-auth, and admin modals completely removed |
| Keyboard Accessibility | **VERIFIED** | Native buttons, focus traps, Escape handling, and ARIA attributes |
| Contact Form Architecture | **CODE READY** | Endpoint configurable; external endpoint not yet supplied |
| Newsletter Architecture | **CODE READY** | Honest state; external service not yet supplied |
| Google Analytics (GA4) | **READY** | Commented placeholder in `<head>` pending Measurement ID |

---

## 📄 License & Ownership

© 2026 **PIXIVO**. All rights reserved.  
Official contact: `connect.pixivo@gmail.com`  
Instagram: [`@heypixivo`](https://www.instagram.com/heypixivo/)  
Project Brief (Google Form): [Open Direct Intake Form](https://docs.google.com/forms/d/e/1FAIpQLSc7GfuMAbpWOUm3ev4ShTIrvHQ8t2C8Zf_lW9PGN_SROAVxRg/viewform)
