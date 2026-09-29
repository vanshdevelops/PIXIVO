/**
 * =============================================================================
 * AURELIS — LUXURY MOTION & SCROLL-DRIVEN PRODUCT STORY ENGINE
 * Sophisticated cinematic motion, chiaroscuro studio lighting & subtle parallax
 * Conceived for PIXIVO Flagship Portfolio
 * =============================================================================
 */

(function () {
  'use strict';

  // 1. Reduced Motion Safety Gate
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (prefersReducedMotion.matches) {
    // Reveal all elements immediately
    document.querySelectorAll('.reveal-element').forEach((el) => {
      el.classList.add('revealed', 'is-revealed');
    });
    return;
  }

  // 2. Hardware & Device Queries
  const isTouch = window.matchMedia('(hover: none) or (pointer: coarse)').matches;
  let isMobile = window.innerWidth < 768;
  window.addEventListener('resize', () => {
    isMobile = window.innerWidth < 768;
  }, { passive: true });

  // 3. Cache Elements
  const heroSection = document.getElementById('hero');
  const heroBottle = document.querySelector('.hero-bottle-img');
  const heroReflection = document.querySelector('.bottle-plinth-reflection');
  const heroGlow = document.querySelector('.hero-background-glow');

  const signatureSection = document.getElementById('signature');
  const signatureBottle = document.querySelector('.signature-bottle-img');
  const signatureHalo = document.querySelector('.halo-light');
  const specItems = document.querySelectorAll('.specs-list li');

  const collectionSection = document.getElementById('collection');
  const collectionBottle = document.getElementById('collectionBottleImg');

  const galleryCards = document.querySelectorAll('.gallery-card');

  // State
  let scrollY = window.pageYOffset || document.documentElement.scrollTop;
  let viewportHeight = window.innerHeight;
  let isTicking = false;

  window.addEventListener('resize', () => {
    viewportHeight = window.innerHeight;
  }, { passive: true });

  // ---------------------------------------------------------------------------
  // 4. HERO SECTION PRODUCT PARALLAX & LIGHT DRIFT (PART 4, 14, 15)
  // ---------------------------------------------------------------------------
  function updateHeroParallax() {
    if (!heroBottle || !heroSection) return;

    if (scrollY < viewportHeight * 1.3) {
      if (isMobile) {
        // Mobile: very subtle vertical translation only
        const mobileOffset = Math.min(scrollY * 0.025, 14);
        heroBottle.style.transform = `translate3d(0, ${mobileOffset.toFixed(1)}px, 0)`;
        return;
      }

      // Desktop: slow vertical lag (18px max), subtle scale compression, reflection tracking
      const offset = Math.min(scrollY * 0.04, 26);
      const scale = Math.max(0.97, 1 - (scrollY / viewportHeight) * 0.04);
      heroBottle.style.transform = `translate3d(0, ${offset.toFixed(1)}px, 0) scale(${scale.toFixed(3)})`;

      if (heroReflection) {
        heroReflection.style.transform = `translateX(-50%) translate3d(0, ${(offset * 0.35).toFixed(1)}px, 0)`;
        heroReflection.style.opacity = Math.max(0.2, 0.7 - (scrollY / viewportHeight) * 0.5).toFixed(2);
      }

      if (heroGlow) {
        const glowOffset = (scrollY * 0.02).toFixed(1);
        heroGlow.style.transform = `translate(-50%, calc(-50% + ${glowOffset}px))`;
      }
    }
  }

  // ---------------------------------------------------------------------------
  // 5. PRODUCT SCROLL STORY (PART 12 — PHASES 1 TO 5)
  // ---------------------------------------------------------------------------
  function updateSignatureProductStory() {
    if (!signatureSection || !signatureBottle) return;

    const rect = signatureSection.getBoundingClientRect();
    const sectionHeight = rect.height;

    // Only process when signature section is near or in viewport
    if (rect.bottom < -100 || rect.top > viewportHeight + 100) return;

    // Normalized progress through section: 0 when top enters bottom of viewport, 1 when bottom leaves top
    const totalDist = sectionHeight + viewportHeight;
    const currentDist = viewportHeight - rect.top;
    const progress = Math.max(0, Math.min(1, currentDist / totalDist));

    if (isMobile) {
      // Mobile: elegant restrained movement, no horizontal shift or rotation to prevent jitter
      const mobileY = ((progress - 0.5) * -16).toFixed(1);
      signatureBottle.style.transform = `translate3d(0, ${mobileY}px, 0)`;
      return;
    }

    // Relative to section vertical center: -1.0 (entering) to 0.0 (centered) to +1.0 (exiting)
    const relProgress = ((viewportHeight / 2 - (rect.top + sectionHeight / 2)) / (viewportHeight / 2));

    // PHASE 1 — ENTRANCE (relProgress from -1.2 to -0.3)
    // PHASE 2 — PRODUCT REVEAL & FLOAT (relProgress from -0.3 to 0.0)
    // PHASE 3 — HERO PRODUCT FOCUS (relProgress around 0.0, -0.2 to +0.2)
    // PHASE 4 — DETAIL CASCADE (specs reveal during central passage)
    // PHASE 5 — EXIT (relProgress from +0.2 to +1.2)

    let scale = 1.0;
    let transY = 0;
    let transX = 0;
    let rotDeg = 0;
    let opacity = 1.0;

    if (relProgress < 0) {
      // Entrance & Reveal
      const t = Math.max(0, (relProgress + 1.2) / 1.2); // 0 at entry, 1 at center
      scale = 0.95 + 0.075 * t; // scales from 0.95 to 1.025
      transY = (1 - t) * 32;     // glides up into center
      transX = (1 - t) * -10;    // gentle emergence from slight left offset
      rotDeg = (1 - t) * -0.7;   // tiny, subtle rotation straightening out
      opacity = 0.88 + 0.12 * t;
    } else {
      // Focal Center & Exit
      const t = Math.min(1, relProgress / 1.2); // 0 at center, 1 at exit
      scale = 1.025 - 0.055 * t; // gently scales down from 1.025 to 0.97
      transY = t * -24;          // glides slowly upward into exit
      transX = t * 8;            // gentle exit drift to the right
      rotDeg = t * 0.6;          // tiny rotation (+0.6deg max)
      opacity = 1.0 - 0.08 * t;
    }

    signatureBottle.style.transform = `translate3d(${transX.toFixed(1)}px, ${transY.toFixed(1)}px, 0) scale(${scale.toFixed(3)}) rotate(${rotDeg.toFixed(2)}deg)`;
    signatureBottle.style.opacity = opacity.toFixed(2);

    // Studio Chiaroscuro Lighting (Halo movement & caustic expansion)
    if (signatureHalo) {
      const haloX = (-transX * 0.4).toFixed(1);
      const haloY = (-transY * 0.35).toFixed(1);
      const haloOpacity = Math.max(0.4, 0.9 - Math.abs(relProgress) * 0.4).toFixed(2);
      signatureHalo.style.transform = `translate(calc(-50% + ${haloX}px), calc(-50% + ${haloY}px)) scale(${(scale * 1.05).toFixed(2)})`;
      signatureHalo.style.opacity = haloOpacity;
    }

    // PHASE 4 — DETAIL REVEAL (Specification Items Cascade)
    if (specItems.length > 0) {
      if (isMobile) {
        specItems.forEach((item) => {
          item.style.opacity = '1';
          item.style.transform = 'none';
        });
      } else {
        specItems.forEach((item, idx) => {
          const itemThreshold = -0.5 + (idx / specItems.length) * 0.5;
          if (relProgress > itemThreshold) {
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
          } else {
            item.style.opacity = '0.9';
            item.style.transform = 'translateX(5px)';
          }
        });
      }
    }
  }

  // ---------------------------------------------------------------------------
  // 6. EDITORIAL CARD & ARCHIVE PARALLAX
  // ---------------------------------------------------------------------------
  const visibleCards = new Set();
  if (!isTouch && galleryCards.length > 0 && 'IntersectionObserver' in window) {
    const cardObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            visibleCards.add(entry.target);
          } else {
            visibleCards.delete(entry.target);
          }
        });
      },
      { rootMargin: '100px 0px 100px 0px', threshold: 0 }
    );

    galleryCards.forEach((card) => cardObserver.observe(card));
  }

  function updateGalleryParallax() {
    if (isTouch || isMobile || visibleCards.size === 0) return;

    visibleCards.forEach((card) => {
      const img = card.querySelector('.gallery-img');
      if (!img) return;

      const rect = card.getBoundingClientRect();
      const viewportCenter = viewportHeight / 2;
      const cardCenter = rect.top + rect.height / 2;
      const distanceFromCenter = cardCenter - viewportCenter;

      // Restrained shift: -6px to +6px
      const parallaxY = Math.max(-6, Math.min(6, distanceFromCenter * -0.025));
      img.style.transform = `scale(1.02) translate3d(0, ${parallaxY.toFixed(1)}px, 0)`;
    });
  }

  // ---------------------------------------------------------------------------
  // 7. SCROLL REVEAL ENHANCER (Guarantees visible elements reveal reliably)
  // ---------------------------------------------------------------------------
  function revealVisibleElements() {
    if (window.location.search.includes('reveal=all')) {
      document.querySelectorAll('.reveal-element').forEach((el) => {
        el.classList.add('revealed', 'is-revealed');
      });
      return;
    }
    const vh = window.innerHeight || document.documentElement.clientHeight;
    document.querySelectorAll('.reveal-element:not(.revealed)').forEach((el) => {
      const rect = el.getBoundingClientRect();
      if (rect.top < vh * 0.98 && rect.bottom > -80) {
        el.classList.add('revealed', 'is-revealed');
      }
    });
  }

  function enhanceScrollReveals() {
    const revealElements = document.querySelectorAll('.reveal-element');
    if (!revealElements.length) return;

    const observer = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed', 'is-revealed');
            obs.unobserve(entry.target);
          }
        });
      },
      {
        root: null,
        rootMargin: '0px 0px -4% 0px',
        threshold: 0.05,
      }
    );

    revealElements.forEach((el) => {
      observer.observe(el);
    });

    // Immediate check
    revealVisibleElements();
  }

  // ---------------------------------------------------------------------------
  // 8. SCROLL TICKER (PERFORMANCE-OPTIMIZED VIA requestAnimationFrame)
  // ---------------------------------------------------------------------------
  function onScroll() {
    scrollY = window.pageYOffset || document.documentElement.scrollTop;
    if (!isTicking) {
      requestAnimationFrame(() => {
        revealVisibleElements();
        updateHeroParallax();
        updateSignatureProductStory();
        updateGalleryParallax();
        isTicking = false;
      });
      isTicking = true;
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });

  // ---------------------------------------------------------------------------
  // 9. AMBIENT CURSOR-FOLLOW LIGHT (DESKTOP ONLY)
  // ---------------------------------------------------------------------------
  if (!isTouch && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    const ambientLight = document.createElement('div');
    ambientLight.className = 'aur-ambient-cursor';
    ambientLight.setAttribute('aria-hidden', 'true');
    document.body.appendChild(ambientLight);

    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let currentX = mouseX;
    let currentY = mouseY;
    let cursorActive = false;

    function renderCursor() {
      currentX += (mouseX - currentX) * 0.12;
      currentY += (mouseY - currentY) * 0.12;

      ambientLight.style.transform = `translate3d(${currentX.toFixed(1)}px, ${currentY.toFixed(1)}px, 0) translate(-50%, -50%)`;

      if (cursorActive) {
        requestAnimationFrame(renderCursor);
      }
    }

    document.addEventListener(
      'mousemove',
      (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        if (!cursorActive) {
          cursorActive = true;
          ambientLight.style.opacity = '1';
          requestAnimationFrame(renderCursor);
        }
      },
      { passive: true }
    );

    document.addEventListener(
      'mouseleave',
      () => {
        cursorActive = false;
        ambientLight.style.opacity = '0';
      },
      { passive: true }
    );
  }

  // ---------------------------------------------------------------------------
  // 10. DEEP LINKING & SECTION INSPECTION CONTROLLER
  // ---------------------------------------------------------------------------
  function handleSectionNavigation() {
    const params = new URLSearchParams(window.location.search);
    const targetSection = params.get('section');
    const scrollPos = params.get('scroll');

    if (targetSection) {
      const sec = document.getElementById(targetSection);
      if (sec) {
        const preloader = document.getElementById('preloader');
        if (preloader) preloader.remove();
        document.documentElement.style.scrollBehavior = 'auto';
        document.body.style.scrollBehavior = 'auto';
        const targetTop = sec.offsetTop;
        window.scrollTo(0, Math.max(0, targetTop - 20));
        revealVisibleElements();
        updateHeroParallax();
        updateSignatureProductStory();
      }
    } else if (scrollPos) {
      const preloader = document.getElementById('preloader');
      if (preloader) preloader.remove();
      document.documentElement.style.scrollBehavior = 'auto';
      document.body.style.scrollBehavior = 'auto';
      const y = parseInt(scrollPos, 10);
      window.scrollTo(0, y);
      revealVisibleElements();
      updateHeroParallax();
      updateSignatureProductStory();
    }
  }

  // ---------------------------------------------------------------------------
  // 11. INITIALIZATION
  // ---------------------------------------------------------------------------
  window.addEventListener('DOMContentLoaded', () => {
    enhanceScrollReveals();
    updateHeroParallax();
    updateSignatureProductStory();
    handleSectionNavigation();
  });

  window.addEventListener('load', () => {
    enhanceScrollReveals();
    updateHeroParallax();
    updateSignatureProductStory();
    handleSectionNavigation();
  });
})();
