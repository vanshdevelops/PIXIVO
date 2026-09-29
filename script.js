/**
 * PIXIVO — Official Agency JavaScript
 * "Where Vision Meets Motion"
 * 
 * Features:
 * - Production-ready configuration architecture
 * - Splash screen loading sequence
 * - Fixed/sticky navbar with scroll shrink & mobile drawer
 * - Custom desktop cursor (requestAnimationFrame) with reduced-motion safety
 * - IntersectionObserver scroll reveals & animated counter metrics
 * - Filterable portfolio & accessible case study modal (keyboard accessible, focus trap, Escape close)
 * - Interactive pricing toggle (Individual vs. Packages)
 * - Functional interactive project pricing calculator with 25% discount logic
 * - Accessible FAQ accordion with ARIA management
 * - Production contact form architecture (configurable endpoint, graceful fallback, zero PII localStorage)
 * - Newsletter subscription handling with honest configuration state
 * - How We Work studio methodology presentation
 * - Back to top smooth navigation
 */

(function () {
  'use strict';

  // ==========================================================================
  // 1. PRODUCTION CONFIGURATION ARCHITECTURE
  // ==========================================================================
  const PIXIVO_CONFIG = Object.assign({
    // Remote HTTPS POST endpoint for contact inquiries (e.g. Formspree, Netlify Forms, custom API)
    // When left empty, the contact form validates input and provides an explicit configuration state with direct email fallback.
    contactEndpoint: '',

    // Remote HTTPS endpoint for newsletter subscriptions (e.g. ConvertKit, Mailchimp, custom webhook)
    // When left empty, indicates the subscription service is undergoing configuration.
    newsletterEndpoint: ''
  }, window.PIXIVO_CONFIG || {});
  window.PIXIVO_CONFIG = PIXIVO_CONFIG;

  // ==========================================================================
  // 2. AGENCY DATA STRUCTURE (PIXIVO_DEFAULTS)
  // ==========================================================================
  const PIXIVO_DEFAULTS = {
    settings: {
      discountBannerActive: true,
      logoAnim: 'on',
      ambientBg: 'on',
      animIntensity: 'medium'
    },
    pricing: [
      {
        id: 'brand-websites',
        name: 'Brand Websites',
        category: 'Web Design',
        originalPrice: '₹6,665–₹17,332',
        discountPrice: '₹4,999–₹12,999',
        calcRate: 4999,
        description: 'Landing pages, responsive corporate websites, and conversion architecture engineered for speed and visual prestige.'
      },
      {
        id: 'premium-logos',
        name: 'Premium Logos',
        category: 'Branding',
        originalPrice: '₹399–₹932',
        discountPrice: '₹299–₹699',
        calcRate: 299,
        description: 'Bespoke geometric visual marks, color harmonies, and scalable vector brand identity systems.'
      },
      {
        id: 'ai-ads',
        name: 'AI Product Advertisements',
        category: 'AI Advertising',
        originalPrice: '₹1,065–₹1,732',
        discountPrice: '₹799–₹1,299',
        calcRate: 799,
        description: 'Cinematic 10-second video ads and vertical reels powered by advanced neural generation and color grading.'
      },
      {
        id: 'logo-animation',
        name: 'Logo Animation',
        category: 'Motion Design',
        originalPrice: '₹665–₹1,332',
        discountPrice: '₹499–₹999',
        calcRate: 499,
        description: 'Dynamic 3D & 2D motion idents, UI splash signatures, and fluid video stingers that bring your mark to life.'
      },
      {
        id: 'product-launch',
        name: 'Product Launch Creatives',
        category: 'Launch Campaigns',
        originalPrice: '₹1,332–₹2,132',
        discountPrice: 'From ₹999',
        calcRate: 999,
        description: 'Full-funnel teaser visual suites, key art banners, and hero promotional creative suites built for launch day impact.'
      },
      {
        id: 'social-media',
        name: 'Social Media Posts & Posters',
        category: 'Social Creative',
        originalPrice: '₹532–₹1,599',
        discountPrice: '₹399–₹1,199',
        calcRate: 399,
        description: 'High-impact static and carousel visual designs tailored for Instagram, LinkedIn, and X that stop the scroll.'
      },
      {
        id: 'page-handling',
        name: 'Social Media Page Handling',
        category: 'Account Management',
        originalPrice: '₹2,132–₹2,665',
        discountPrice: '₹1,599–₹1,999',
        calcRate: 1599,
        description: 'Complete channel curation: aesthetic grid planning, scheduled creative rollouts, and ongoing visual refinement.'
      },
      {
        id: 'ai-cx',
        name: 'AI-Powered Customer Experience',
        category: 'AI Systems',
        originalPrice: '₹665–₹1,332',
        discountPrice: '₹499–₹999',
        calcRate: 499,
        description: 'Bespoke conversational flows, intelligent lead qualifiers, and AI-driven interfaces that convert prospects.'
      }
    ],
    packages: [
      {
        id: 'starter',
        name: 'Starter Identity & Web',
        badge: 'STARTER',
        originalPrice: '₹7,999',
        discountPrice: '₹5,999',
        features: [
          'Complete Brand Website (3–4 Sections)',
          'Premium Vector Logo & Color System',
          '5 High-Impact Social Media Creatives',
          '2D/3D Logo Animation Ident',
          'Mobile & SEO Optimization'
        ]
      },
      {
        id: 'professional',
        name: 'Growth Brand Experience',
        badge: 'PROFESSIONAL',
        originalPrice: '₹13,332',
        discountPrice: '₹9,999',
        features: [
          'Full Multi-Section Brand Website & CMS Structure',
          'Premium Logo Suite & Complete Brand Guidelines',
          'High-Definition 3D Logo Animation Ident',
          'AI Product Video Ad (10s Reel / Promo)',
          '10 Bespoke Social Media Creatives',
          'Product Launch Visual Creative Suite',
          'Basic Social Media Handling & Strategy',
          '30 Days Post-Launch Support'
        ]
      },
      {
        id: 'enterprise',
        name: 'Custom Ecosystem',
        badge: 'ENTERPRISE',
        originalPrice: 'Custom Scope',
        discountPrice: 'Custom Quote',
        features: [
          'Bespoke Architecture & Interactive Web Systems',
          'Global Brand Identity & Design Token Architecture',
          'Multiple AI Video Advertisements & Reels',
          '3D Motion Identity & Product Visuals',
          'End-to-End Product Launch Campaign',
          'Complete Social Media Management & Analytics',
          'AI-Powered Customer Experience Integration',
          'Dedicated Art Director & Priority SLA'
        ]
      }
    ],
    portfolio: [
      {
        id: 1,
        title: 'Nova Coffee',
        category: 'Web Design & E-Commerce · Concept Project',
        filterKey: 'web-design',
        image: 'assets/portfolio/project-1.jpg',
        tag: 'STUDIO CONCEPT 01',
        projectType: 'Concept Project',
        challenge: 'Nova Coffee concept explored an artisanal digital storefront designed to transition from a boutique roaster to an online subscription brand.',
        solution: 'Engineered a responsive website concept featuring rich coffee tones, custom brew calculators, and a streamlined 2-step checkout flow.',
        services: 'Brand Websites, UI/UX Design, E-Commerce Architecture',
        outcomeLabel: 'Design Outcome',
        outcome: 'Responsive e-commerce concept featuring product discovery, subscription architecture and streamlined checkout flows.'
      },
      {
        id: 2,
        title: 'Aurelia',
        category: 'Luxury Brand Identity · Concept Project',
        filterKey: 'branding',
        image: 'assets/portfolio/project-2.jpg',
        tag: 'STUDIO CONCEPT 02',
        projectType: 'Concept Project',
        challenge: 'Aurelia concept explored high-fashion sustainable luxury with an identity system tailored for discerning international audiences.',
        solution: 'Crafted a bespoke geometric serif wordmark, custom iridescent foil packaging concepts, and an editorial digital guidelines suite.',
        services: 'Premium Logos, Brand Identity, Packaging Guidelines',
        outcomeLabel: 'Design Outcome',
        outcome: 'Bespoke editorial brand identity suite, geometric serif wordmark and sustainable luxury packaging design guidelines.'
      },
      {
        id: 3,
        title: 'Vanta AI',
        category: 'AI Product Advertisement · Concept Project',
        filterKey: 'ai-ads',
        image: 'assets/portfolio/project-3.jpg',
        tag: 'STUDIO CONCEPT 03',
        projectType: 'Concept Project',
        challenge: 'Vanta concept developed a neural product advertisement showcase to explore dynamic robotics visualization.',
        solution: 'Produced a neural-generated 3D product showcase featuring dramatic cyberpunk lighting, sleek motion pacing, and atmospheric soundscapes.',
        services: 'AI Product Advertisements, 3D Rendering, Motion Direction',
        outcomeLabel: 'Design Outcome',
        outcome: '10-second neural-generated product-film concept exploring cinematic lighting, motion and technology-focused storytelling.'
      },
      {
        id: 4,
        title: 'Luma Sound',
        category: 'Social Media Campaign · Concept Project',
        filterKey: 'social-media',
        image: 'assets/portfolio/project-4.jpg',
        tag: 'STUDIO CONCEPT 04',
        projectType: 'Concept Project',
        challenge: 'Luma concept explored high-contrast visual messaging to highlight spatial audio studio monitors in modern social feeds.',
        solution: 'Developed a high-contrast carousel campaign and audio-reactive motion teaser visual system emphasizing sonic fidelity and industrial elegance.',
        services: 'Social Media Posts & Posters, Motion Teasers',
        outcomeLabel: 'Design Outcome',
        outcome: 'High-contrast social carousel design suite and audio-reactive motion teasers built for sound hardware product discovery.'
      },
      {
        id: 5,
        title: 'Axiom Pay',
        category: '3D Motion & Logo System · Concept Project',
        filterKey: 'animation',
        image: 'assets/portfolio/project-5.jpg',
        tag: 'STUDIO CONCEPT 05',
        projectType: 'Concept Project',
        challenge: 'Fintech platform concept Axiom required a kinetic brand mark that balanced geometric precision with fluid motion behavior.',
        solution: 'Designed a multidimensional animated logo ribbon that flexes, flows, and locks into place with crisp geometric alignments.',
        services: 'Logo Animation, 3D Identity, App Splash Motion',
        outcomeLabel: 'Design Outcome',
        outcome: 'Kinetic brand mark and multidimensional motion ribbon exploring fluid UI transitions and mobile app splash states.'
      },
      {
        id: 6,
        title: 'Nexa Mobility',
        category: 'Product Launch Creatives · Concept Project',
        filterKey: 'product-launch',
        image: 'assets/portfolio/project-6.jpg',
        tag: 'STUDIO CONCEPT 06',
        projectType: 'Concept Project',
        challenge: 'An urban electric mobility concept exploring full-funnel launch art to drive reservations for a flagship electric two-wheeler.',
        solution: 'Built an integrated countdown visual system, high-energy teaser sequences, and landing page creative suites optimized for mobile reservations.',
        services: 'Product Launch Creatives, Landing Page Assets, AI Video',
        outcomeLabel: 'Design Outcome',
        outcome: 'Full-funnel vehicle launch teaser suite, countdown visual system and mobile-optimized reservation interface.'
      }
    ],
    methodology: [
      {
        step: '01',
        title: 'Discover',
        description: 'Understand the brand, audience, objective and competitive environment to establish clear strategic direction.'
      },
      {
        step: '02',
        title: 'Design',
        description: 'Build the visual system, digital experience and creative direction with high-fidelity craftsmanship.'
      },
      {
        step: '03',
        title: 'Refine',
        description: 'Test, review and refine the work across relevant devices, screen resolutions and media formats.'
      },
      {
        step: '04',
        title: 'Deliver',
        description: 'Prepare organized production-ready assets, documentation and responsive implementation.'
      }
    ],
    faq: [
      {
        id: 1,
        question: 'How long does a typical project take?',
        answer: 'Timelines vary by scope. Standalone services like Premium Logos, Logo Animation, or AI Ads typically deliver within 3 to 7 business days. Comprehensive Brand Websites and Growth Packages typically range from 1 to 3 weeks with dedicated sprint milestones.'
      },
      {
        id: 2,
        question: 'How many revisions are included?',
        answer: 'All individual services and package deals include 2 to 3 comprehensive rounds of revisions to ensure absolute alignment with your vision. We present polished design drafts and refine details iteratively.'
      },
      {
        id: 3,
        question: 'What are your payment terms?',
        answer: 'Standard projects operate on a 50% initial commitment deposit to commence design sprints, with the remaining 50% settled upon final approval prior to asset delivery and live website handover.'
      },
      {
        id: 4,
        question: 'Who owns the website and assets after completion?',
        answer: 'You retain 100% full intellectual property ownership. Upon project sign-off and final settlement, all vector source files, code repositories, 3D motion renders, and graphics belong completely to your business.'
      },
      {
        id: 5,
        question: 'How do you hand over project assets and websites?',
        answer: 'We deliver clean, modular production code, organized design tokens, vector masters, and comprehensive asset documentation. For websites requiring regular updates, we configure client-friendly editing architecture so your team can manage content seamlessly.'
      },
      {
        id: 6,
        question: 'Can I customize a package?',
        answer: 'Absolutely. While our Starter and Professional packages bundle the most commonly required deliverables at an attractive discount, we frequently tailor custom scopes to fit specialized brand launches and enterprise requirements.'
      },
      {
        id: 7,
        question: 'Do you provide ongoing website maintenance?',
        answer: 'Yes! We provide our dedicated Website Maintenance & Customization plan at ₹999/month, covering minor content updates, speed optimization, small design adjustments, and ongoing technical support.'
      },
      {
        id: 8,
        question: 'Can I purchase services individually?',
        answer: 'Yes, every single discipline we offer is available as an individual standalone service. You can also mix-and-match specific services using our interactive Pricing Calculator above.'
      }
    ],
    team: {
      founder: {
        name: 'Vansh Prajapati',
        role: 'Founder & Creative Director',
        experience: '',
        image: 'assets/founder.jpg',
        bio: '',
        linkedin: '',
        instagram: ''
      },
      coFounder: {
        name: 'Himanshu Kumar',
        role: 'Co-Founder & Strategy & Technology Lead',
        experience: '',
        image: '',
        bio: '',
        linkedin: '',
        instagram: ''
      },
      metrics: {
        projectsDelivered: 5,
        monthsActive: 1,
        disciplines: 8
      }
    }
  };

  // Active state data
  const sitePricing = PIXIVO_DEFAULTS.pricing;
  const sitePortfolio = PIXIVO_DEFAULTS.portfolio;
  const siteMethodology = PIXIVO_DEFAULTS.methodology;
  const siteFaq = PIXIVO_DEFAULTS.faq;
  const siteTeam = PIXIVO_DEFAULTS.team;

  let selectedCalcServices = new Set(['Brand Websites']); // Default 1 selected
  let lastFocusedTrigger = null;

  // ==========================================================================
  // 3. SPLASH / LOADING SCREEN
  // ==========================================================================
  function initSplashScreen() {
    const splash = document.getElementById('splash-screen');
    if (!splash) return;

    const hideSplash = () => {
      splash.classList.add('fade-out');
      setTimeout(() => {
        splash.style.display = 'none';
      }, 600);
    };

    if (document.readyState === 'complete') {
      setTimeout(hideSplash, 900);
    } else {
      window.addEventListener('load', () => setTimeout(hideSplash, 600));
      setTimeout(hideSplash, 1600);
    }
  }

  // ==========================================================================
  // 4. HEADER, STICKY SCROLL & MOBILE DRAWER
  // ==========================================================================
  function initNavigation() {
    const header = document.getElementById('site-header');
    const menuBtn = document.getElementById('mobile-menu-btn');
    const mobileNav = document.getElementById('mobile-nav');
    const closeBtn = document.getElementById('mobile-nav-close');
    const backdrop = document.getElementById('mobile-nav-backdrop');
    const mobileLinks = document.querySelectorAll('.mobile-nav-link, .mobile-cta');
    const navLinks = document.querySelectorAll('.desktop-nav .nav-link');

    // Sticky scroll effect
    window.addEventListener('scroll', () => {
      if (window.scrollY > 40) {
        header?.classList.add('scrolled');
      } else {
        header?.classList.remove('scrolled');
      }
      updateActiveNavLink();
    }, { passive: true });

    // Active nav link highlight on scroll
    function updateActiveNavLink() {
      const sections = document.querySelectorAll('section[id]');
      const scrollPos = window.scrollY + 120;

      sections.forEach(sec => {
        const top = sec.offsetTop;
        const height = sec.offsetHeight;
        const id = sec.getAttribute('id');

        if (scrollPos >= top && scrollPos < top + height) {
          navLinks.forEach(link => {
            link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
          });
        }
      });
    }

    // Mobile Drawer Open / Close
    function openMobileMenu() {
      if (!mobileNav || !menuBtn) return;
      mobileNav.classList.add('open');
      mobileNav.setAttribute('aria-hidden', 'false');
      menuBtn.setAttribute('aria-expanded', 'true');
      document.body.classList.add('menu-open');
      closeBtn?.focus();
    }

    function closeMobileMenu() {
      if (!mobileNav || !menuBtn) return;
      mobileNav.classList.remove('open');
      mobileNav.setAttribute('aria-hidden', 'true');
      menuBtn.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('menu-open');
      menuBtn.focus();
    }

    menuBtn?.addEventListener('click', openMobileMenu);
    closeBtn?.addEventListener('click', closeMobileMenu);
    backdrop?.addEventListener('click', closeMobileMenu);

    mobileLinks.forEach(link => {
      link.addEventListener('click', closeMobileMenu);
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobileNav?.classList.contains('open')) {
        closeMobileMenu();
      }
    });
  }

  // ==========================================================================
  // 5. CUSTOM CURSOR
  // ==========================================================================
  function initCursor() {
    const cursor = document.getElementById('custom-cursor');
    if (!cursor || window.innerWidth < 1024) return;

    // Respect reduced motion preference
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      cursor.style.display = 'none';
      return;
    }

    const dot = cursor.querySelector('.cursor-dot');
    const ring = cursor.querySelector('.cursor-ring');
    let mouseX = -100, mouseY = -100;
    let ringX = -100, ringY = -100;

    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      if (dot) {
        dot.style.transform = `translate(${mouseX}px, ${mouseY}px)`;
      }
    }, { passive: true });

    function renderRing() {
      ringX += (mouseX - ringX) * 0.18;
      ringY += (mouseY - ringY) * 0.18;
      if (ring) {
        ring.style.transform = `translate(${ringX}px, ${ringY}px)`;
      }
      requestAnimationFrame(renderRing);
    }
    requestAnimationFrame(renderRing);

    // Expand on hover
    const hoverTargets = 'a, button, input, select, textarea, .portfolio-card, .portfolio-item, .brand-logo-link, .service-card, .calc-checkbox-card';
    document.addEventListener('mouseover', (e) => {
      if (e.target.closest(hoverTargets)) {
        cursor.classList.add('hovered');
      } else {
        cursor.classList.remove('hovered');
      }
    });
  }

  // ==========================================================================
  // 6. SCROLL REVEALS & METRIC COUNTERS
  // ==========================================================================
  function initAnimations() {
    const reveals = document.querySelectorAll('[data-reveal]');
    if ('IntersectionObserver' in window) {
      const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const el = entry.target;
            const delay = el.getAttribute('data-delay');
            if (delay) {
              el.style.transitionDelay = `${delay}s`;
            }
            el.classList.add('revealed');
            observer.unobserve(el);
          }
        });
      }, { threshold: 0.15 });

      reveals.forEach(el => revealObserver.observe(el));
    } else {
      reveals.forEach(el => el.classList.add('revealed'));
    }

    // Animated Metric Counters
    const metricsContainer = document.getElementById('about-metrics');
    let counted = false;

    if (metricsContainer && 'IntersectionObserver' in window) {
      const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting && !counted) {
            counted = true;
            animateCounters();
          }
        });
      }, { threshold: 0.3 });

      counterObserver.observe(metricsContainer);
    } else {
      animateCounters();
    }

    function animateCounters() {
      const counters = document.querySelectorAll('.counter');
      counters.forEach(counter => {
        const target = +counter.getAttribute('data-target') || 0;
        const duration = 1200;
        const start = performance.now();

        function step(now) {
          const progress = Math.min((now - start) / duration, 1);
          const ease = 1 - Math.pow(1 - progress, 3);
          counter.textContent = Math.floor(ease * target);
          if (progress < 1) {
            requestAnimationFrame(step);
          } else {
            counter.textContent = target;
          }
        }
        requestAnimationFrame(step);
      });
    }
  }

  // ==========================================================================
  // 7. TEAM / LEADERSHIP RENDERING
  // ==========================================================================
  function renderTeam() {
    const founder = siteTeam.founder || {};
    const coFounder = siteTeam.coFounder || {};
    const metrics = siteTeam.metrics || {};

    // 1. Founder Card
    const founderImg = document.getElementById('founder-display-img');
    const founderName = document.getElementById('founder-display-name');
    const founderRole = document.getElementById('founder-display-role');

    if (founderImg) {
      founderImg.src = founder.image && founder.image.trim() ? founder.image : 'assets/founder.jpg';
    }
    if (founderName) {
      founderName.textContent = founder.name || 'Vansh Prajapati';
    }
    if (founderRole) {
      founderRole.textContent = founder.role || 'Founder & Creative Director';
    }

    // 2. Co-Founder Card
    const cofounderImg = document.getElementById('cofounder-display-img');
    const cofounderName = document.getElementById('cofounder-display-name');
    const cofounderRole = document.getElementById('cofounder-display-role');

    if (cofounderImg) {
      cofounderImg.src = coFounder.image && coFounder.image.trim() ? coFounder.image : 'assets/cofounder-placeholder.svg';
    }
    if (cofounderName) {
      cofounderName.textContent = coFounder.name || 'Himanshu Kumar';
    }
    if (cofounderRole) {
      cofounderRole.textContent = coFounder.role || 'Co-Founder & Strategy & Technology Lead';
    }

    // 3. About Section Truthful Metrics
    const metricCounters = document.querySelectorAll('#about-metrics .counter');
    if (metricCounters.length >= 3) {
      metricCounters[0].setAttribute('data-target', metrics.projectsDelivered || 5);
      metricCounters[1].setAttribute('data-target', metrics.monthsActive || 1);
      metricCounters[2].setAttribute('data-target', metrics.disciplines || 8);
    }
  }

  // ==========================================================================
  // 8. PORTFOLIO FILTER & CASE STUDY MODAL
  // ==========================================================================
  function initPortfolio() {
    const filterTabs = document.querySelectorAll('.filter-tab');
    const items = document.querySelectorAll('.portfolio-item');
    const modal = document.getElementById('case-study-modal');
    const modalBackdrop = document.getElementById('modal-backdrop');
    const modalClose = document.getElementById('modal-close-btn');
    const modalBody = document.getElementById('modal-body-content');

    // Filter tabs
    filterTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        filterTabs.forEach(t => {
          t.classList.remove('active');
          t.setAttribute('aria-selected', 'false');
        });
        tab.classList.add('active');
        tab.setAttribute('aria-selected', 'true');

        const filter = tab.getAttribute('data-filter');
        const flagship = document.querySelector('.portfolio-flagship-showcase');
        if (flagship) {
          const flagshipCats = (flagship.getAttribute('data-category') || '').split(' ');
          if (filter === 'all' || flagshipCats.includes(filter)) {
            flagship.classList.remove('hidden');
          } else {
            flagship.classList.add('hidden');
          }
        }
        items.forEach(item => {
          const cat = item.getAttribute('data-category');
          if (filter === 'all' || cat === filter) {
            item.classList.remove('hidden');
          } else {
            item.classList.add('hidden');
          }
        });
      });
    });

    // Modal Focus Trap Helper
    function handleModalKeydown(e) {
      if (e.key === 'Escape') {
        e.preventDefault();
        closeModal();
        return;
      }

      if (e.key === 'Tab') {
        const focusable = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
        if (focusable.length === 0) return;

        const firstFocusable = focusable[0];
        const lastFocusable = focusable[focusable.length - 1];

        if (e.shiftKey) {
          if (document.activeElement === firstFocusable) {
            e.preventDefault();
            lastFocusable.focus();
          }
        } else {
          if (document.activeElement === lastFocusable) {
            e.preventDefault();
            firstFocusable.focus();
          }
        }
      }
    }

    // Open Case Study Modal
    function triggerCaseStudy(itemEl) {
      lastFocusedTrigger = itemEl;
      const projId = parseInt(itemEl.getAttribute('data-project-id'), 10);
      const project = sitePortfolio.find(p => p.id === projId) || sitePortfolio[0];
      openCaseStudy(project);
    }

    items.forEach(item => {
      item.addEventListener('click', (e) => {
        triggerCaseStudy(item);
      });

      // Native keyboard support
      item.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          triggerCaseStudy(item);
        }
      });
    });

    function openCaseStudy(project) {
      if (!modal || !modalBody) return;

      modalBody.innerHTML = `
        <div class="case-study-header">
          <span class="portfolio-category">${escapeHTML(project.category)}</span>
          <h2 id="modal-project-title" class="section-heading" style="margin-top: 6px;">${escapeHTML(project.title)}</h2>
        </div>
        <img src="${escapeHTML(project.image)}" alt="${escapeHTML(project.title)}" class="case-study-hero-img" width="800" height="450">
        <div class="case-meta-grid">
          <div class="case-meta-item">
            <span class="meta-label">Project Code</span>
            <span class="meta-value">${escapeHTML(project.tag || 'STUDIO CONCEPT')}</span>
          </div>
          <div class="case-meta-item">
            <span class="meta-label">Discipline</span>
            <span class="meta-value">${escapeHTML(project.services || project.category)}</span>
          </div>
          <div class="case-meta-item">
            <span class="meta-label">Project Type</span>
            <span class="meta-value">${escapeHTML(project.projectType || 'Studio Concept')}</span>
          </div>
        </div>
        <div class="case-block">
          <h4>The Challenge</h4>
          <p>${escapeHTML(project.challenge)}</p>
        </div>
        <div class="case-block">
          <h4>The PIXIVO Solution</h4>
          <p>${escapeHTML(project.solution)}</p>
        </div>
        <div class="case-block">
          <h4>${escapeHTML(project.outcomeLabel || 'Design Outcome')}</h4>
          <div class="case-result-badge">${escapeHTML(project.outcome)}</div>
        </div>
      `;

      modal.classList.add('open');
      modal.setAttribute('aria-hidden', 'false');
      document.body.classList.add('modal-open');

      document.addEventListener('keydown', handleModalKeydown);
      setTimeout(() => {
        modalClose?.focus();
      }, 50);
    }

    function closeModal() {
      if (!modal) return;
      modal.classList.remove('open');
      modal.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('modal-open');

      document.removeEventListener('keydown', handleModalKeydown);

      if (lastFocusedTrigger && typeof lastFocusedTrigger.focus === 'function') {
        lastFocusedTrigger.focus();
      }
    }

    modalClose?.addEventListener('click', closeModal);
    modalBackdrop?.addEventListener('click', closeModal);
  }

  // ==========================================================================
  // 9. PRICING SECTION & DYNAMIC CARDS
  // ==========================================================================
  function renderPricingCards() {
    const container = document.getElementById('individual-services-cards');
    if (!container) return;

    container.innerHTML = sitePricing.map(service => `
      <div class="price-card" data-service-id="${service.id}">
        <div class="price-card-header">
          <span class="offer-label">New Customer Offer</span>
          <h3 class="price-card-title">${escapeHTML(service.name)}</h3>
        </div>
        <p class="price-card-desc">${escapeHTML(service.description)}</p>
        <div class="price-tag-wrap">
          <span class="original-strike">Standard: ${escapeHTML(service.originalPrice)}</span>
          <span class="discounted-rate">Intro: ${escapeHTML(service.discountPrice)}</span>
        </div>
        <a href="#contact" class="btn btn-primary btn-block select-service-btn" data-service="${escapeHTML(service.name)}">
          Order Service
        </a>
      </div>
    `).join('');

    container.querySelectorAll('.select-service-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const sName = btn.getAttribute('data-service');
        prefillContactService(sName);
      });
    });
  }

  function initPricingToggle() {
    const toggleBtn = document.getElementById('pricing-toggle-switch');
    const labelInd = document.getElementById('label-individual');
    const labelPkg = document.getElementById('label-packages');
    const indView = document.getElementById('individual-pricing-view');
    const pkgView = document.getElementById('packages-pricing-view');

    function setView(isPackages) {
      if (isPackages) {
        toggleBtn?.setAttribute('aria-checked', 'true');
        labelPkg?.classList.add('active');
        labelInd?.classList.remove('active');
        indView?.classList.remove('active');
        pkgView?.classList.add('active');
      } else {
        toggleBtn?.setAttribute('aria-checked', 'false');
        labelInd?.classList.add('active');
        labelPkg?.classList.remove('active');
        pkgView?.classList.remove('active');
        indView?.classList.add('active');
      }
    }

    toggleBtn?.addEventListener('click', () => {
      const isCurrentlyPkg = toggleBtn.getAttribute('aria-checked') === 'true';
      setView(!isCurrentlyPkg);
    });

    labelInd?.addEventListener('click', () => setView(false));
    labelPkg?.addEventListener('click', () => setView(true));

    document.querySelectorAll('.package-cta').forEach(btn => {
      btn.addEventListener('click', () => {
        const pkgName = btn.getAttribute('data-package');
        prefillContactService(`${pkgName} Package`);
      });
    });

    document.querySelectorAll('[data-service-select]').forEach(link => {
      link.addEventListener('click', () => {
        setView(false);
      });
    });
  }

  // ==========================================================================
  // 10. INTERACTIVE PRICING CALCULATOR
  // ==========================================================================
  function initCalculator() {
    const checkContainer = document.getElementById('calculator-checkboxes');
    const itemsCountEl = document.getElementById('calc-items-count');
    const subtotalEl = document.getElementById('calc-subtotal');
    const discountEl = document.getElementById('calc-discount');
    const totalEl = document.getElementById('calc-total');
    const startProjectBtn = document.getElementById('calc-start-project-btn');

    if (!checkContainer) return;

    checkContainer.innerHTML = sitePricing.map(s => `
      <div class="calc-checkbox-card ${selectedCalcServices.has(s.name) ? 'selected' : ''}" data-calc-name="${escapeHTML(s.name)}" data-calc-rate="${s.calcRate}" tabindex="0" role="checkbox" aria-checked="${selectedCalcServices.has(s.name) ? 'true' : 'false'}" aria-label="${escapeHTML(s.name)}">
        <div class="calc-check-box" aria-hidden="true"></div>
        <span class="calc-service-name">${escapeHTML(s.name)}</span>
        <span class="calc-service-cost">From ₹${s.calcRate.toLocaleString('en-IN')}</span>
      </div>
    `).join('');

    function toggleCard(card) {
      const name = card.getAttribute('data-calc-name');
      if (selectedCalcServices.has(name)) {
        if (selectedCalcServices.size > 1) {
          selectedCalcServices.delete(name);
          card.classList.remove('selected');
          card.setAttribute('aria-checked', 'false');
        }
      } else {
        selectedCalcServices.add(name);
        card.classList.add('selected');
        card.setAttribute('aria-checked', 'true');
      }
      recalculateTotal();
    }

    checkContainer.querySelectorAll('.calc-checkbox-card').forEach(card => {
      card.addEventListener('click', () => toggleCard(card));
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          toggleCard(card);
        }
      });
    });

    function recalculateTotal() {
      let subtotal = 0;
      sitePricing.forEach(s => {
        if (selectedCalcServices.has(s.name)) {
          const basePrice = Math.round(s.calcRate / 0.75);
          subtotal += basePrice;
        }
      });

      const discount = Math.round(subtotal * 0.25);
      const total = subtotal - discount;

      if (itemsCountEl) itemsCountEl.textContent = `${selectedCalcServices.size} service${selectedCalcServices.size === 1 ? '' : 's'}`;
      if (subtotalEl) subtotalEl.textContent = `₹${subtotal.toLocaleString('en-IN')}`;
      if (discountEl) discountEl.textContent = `-₹${discount.toLocaleString('en-IN')}`;
      if (totalEl) totalEl.textContent = `₹${total.toLocaleString('en-IN')}`;
    }

    recalculateTotal();

    startProjectBtn?.addEventListener('click', () => {
      const selectedList = Array.from(selectedCalcServices).join(', ');
      prefillContactService(selectedList);
      const contactSec = document.getElementById('contact');
      contactSec?.scrollIntoView({ behavior: 'smooth' });
    });
  }

  function prefillContactService(serviceName) {
    const contactSec = document.getElementById('contact');
    if (contactSec) {
      contactSec.scrollIntoView({ behavior: 'smooth' });
    }
  }

  // ==========================================================================
  // 11. FAQ ACCORDION
  // ==========================================================================
  function initFAQ() {
    const container = document.getElementById('faq-accordion');
    if (!container) return;

    container.innerHTML = siteFaq.map((item, idx) => `
      <div class="faq-item ${idx === 0 ? 'active' : ''}" data-faq-id="${item.id}">
        <button class="faq-question-btn" aria-expanded="${idx === 0 ? 'true' : 'false'}" aria-controls="faq-ans-${item.id}">
          <span>${escapeHTML(item.question)}</span>
          <span class="faq-icon" aria-hidden="true">+</span>
        </button>
        <div id="faq-ans-${item.id}" class="faq-answer" style="${idx === 0 ? 'max-height: 220px;' : ''}">
          <p>${escapeHTML(item.answer)}</p>
        </div>
      </div>
    `).join('');

    const items = container.querySelectorAll('.faq-item');

    items.forEach(item => {
      const btn = item.querySelector('.faq-question-btn');
      const ans = item.querySelector('.faq-answer');

      btn?.addEventListener('click', () => {
        const isActive = item.classList.contains('active');

        items.forEach(other => {
          if (other !== item) {
            other.classList.remove('active');
            other.querySelector('.faq-question-btn')?.setAttribute('aria-expanded', 'false');
            const otherAns = other.querySelector('.faq-answer');
            if (otherAns) otherAns.style.maxHeight = '0';
          }
        });

        if (isActive) {
          item.classList.remove('active');
          btn.setAttribute('aria-expanded', 'false');
          if (ans) ans.style.maxHeight = '0';
        } else {
          item.classList.add('active');
          btn.setAttribute('aria-expanded', 'true');
          if (ans) ans.style.maxHeight = `${ans.scrollHeight + 30}px`;
        }
      });
    });
  }

  // ==========================================================================
  // 12. HOW WE WORK (METHODOLOGY)
  // ==========================================================================
  function renderHowWeWork() {
    const container = document.getElementById('how-we-work-grid');
    if (!container) return;

    container.innerHTML = siteMethodology.map(item => `
      <div class="workflow-card" data-reveal="fade-up">
        <div class="workflow-step">${escapeHTML(item.step)}</div>
        <h3 class="workflow-title">${escapeHTML(item.title)}</h3>
        <p class="workflow-desc">${escapeHTML(item.description)}</p>
      </div>
    `).join('');
  }

  // ==========================================================================
  // 13. CONTACT CHANNELS (GOOGLE FORM & DIRECT INQUIRY)
  // ==========================================================================
  function initContactChannels() {
    const briefLinks = document.querySelectorAll('a[href*="docs.google.com/forms"]');
    briefLinks.forEach(link => {
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
    });
  }

  // ==========================================================================
  // 14. NEWSLETTER & FOOTER
  // ==========================================================================
  function initNewsletter() {
    const form = document.getElementById('newsletter-form');
    const feedback = document.getElementById('newsletter-feedback');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const emailInput = document.getElementById('newsletter-email');
      const email = emailInput?.value.trim();
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (!email || !emailRegex.test(email)) {
        if (feedback) {
          feedback.textContent = 'Please enter a valid email address';
          feedback.style.color = '#ef4444';
        }
        return;
      }

      // Check if newsletter service endpoint is configured
      if (!PIXIVO_CONFIG.newsletterEndpoint || !PIXIVO_CONFIG.newsletterEndpoint.trim()) {
        if (feedback) {
          feedback.innerHTML = 'Newsletter dispatch is currently being prepared. Follow <a href="https://www.instagram.com/heypixivo/" target="_blank" rel="noopener noreferrer" style="color:var(--c-cyan);">@heypixivo</a> for studio dispatches.';
          feedback.style.color = 'var(--c-cyan)';
        }
        return;
      }

      try {
        const response = await fetch(PIXIVO_CONFIG.newsletterEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, subscribedAt: new Date().toISOString() })
        });

        if (response.ok) {
          if (feedback) {
            feedback.textContent = 'Subscribed to PIXIVO Studio insights!';
            feedback.style.color = 'var(--c-cyan)';
          }
          form.reset();
        } else {
          throw new Error('Subscription failed');
        }
      } catch (err) {
        if (feedback) {
          feedback.textContent = 'Subscription currently unavailable. Please connect via Instagram or direct email.';
          feedback.style.color = '#ef4444';
        }
      }
    });
  }

  function initFooter() {
    const backToTop = document.getElementById('back-to-top-btn');
    backToTop?.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ==========================================================================
  // 15. UTILITY: HTML ESCAPING
  // ==========================================================================
  function escapeHTML(str) {
    if (typeof str !== 'string') return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // ==========================================================================
  // 16. INITIALIZATION CONTROLLER
  // ==========================================================================
  function init() {
    initSplashScreen();
    initNavigation();
    initCursor();
    initAnimations();
    renderTeam();
    renderPricingCards();
    initPricingToggle();
    initCalculator();
    initPortfolio();
    renderHowWeWork();
    initFAQ();
    initContactChannels();
    initNewsletter();
    initFooter();
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
