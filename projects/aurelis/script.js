/**
 * AURELIS — Luxury Fragrance Experience
 * Vanilla JavaScript Controller
 * Conceived for PIXIVO Flagship Portfolio
 */

(function () {
  'use strict';

  // ---------------------------------------------------------------------------
  // 1. PRELOADER / ENTRANCE
  // ---------------------------------------------------------------------------
  function initPreloader() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;

    if (window.location.hash || window.location.search.includes('nopreloader')) {
      preloader.remove();
      return;
    }

    const hidePreloader = () => {
      preloader.classList.add('fade-out');
      setTimeout(() => {
        preloader.remove();
      }, 700);
    };

    // Ensure preloader doesn't stay indefinitely if window load takes long
    if (document.readyState === 'complete') {
      setTimeout(hidePreloader, 400);
    } else {
      window.addEventListener('load', () => {
        setTimeout(hidePreloader, 400);
      });
      // Safety fallback timeout
      setTimeout(hidePreloader, 1500);
    }
  }

  // ---------------------------------------------------------------------------
  // 2. HEADER & NAVIGATION SCROLL EFFECT
  // ---------------------------------------------------------------------------
  function initHeaderScroll() {
    const header = document.getElementById('siteHeader');
    if (!header) return;

    const handleScroll = () => {
      if (window.scrollY > 40) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
  }

  // ---------------------------------------------------------------------------
  // 3. MOBILE DRAWER NAVIGATION
  // ---------------------------------------------------------------------------
  function initMobileNav() {
    const menuToggle = document.getElementById('menuToggle');
    const mobileDrawer = document.getElementById('mobileDrawer');
    const drawerClose = document.getElementById('drawerClose');
    const mobileLinks = document.querySelectorAll('.mobile-nav-link');

    if (!menuToggle || !mobileDrawer) return;

    const openDrawer = () => {
      mobileDrawer.classList.add('open');
      mobileDrawer.setAttribute('aria-hidden', 'false');
      menuToggle.setAttribute('aria-expanded', 'true');
      document.body.classList.add('drawer-open');
      if (drawerClose) drawerClose.focus();
    };

    const closeDrawer = () => {
      mobileDrawer.classList.remove('open');
      mobileDrawer.setAttribute('aria-hidden', 'true');
      menuToggle.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('drawer-open');
      menuToggle.focus();
    };

    menuToggle.addEventListener('click', openDrawer);
    if (drawerClose) drawerClose.addEventListener('click', closeDrawer);

    mobileLinks.forEach((link) => {
      link.addEventListener('click', closeDrawer);
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobileDrawer.classList.contains('open')) {
        closeDrawer();
      }
    });

    // Close if clicked outside drawer inner
    mobileDrawer.addEventListener('click', (e) => {
      if (e.target === mobileDrawer) {
        closeDrawer();
      }
    });

    // Auto-close on viewport resize past mobile breakpoint
    window.addEventListener('resize', () => {
      if (window.innerWidth >= 900 && mobileDrawer.classList.contains('open')) {
        closeDrawer();
      }
    });
  }

  // ---------------------------------------------------------------------------
  // 4. ACTIVE NAVIGATION LINK TRACKING (IntersectionObserver)
  // ---------------------------------------------------------------------------
  function initActiveNavTracking() {
    const sections = document.querySelectorAll('main > section, footer#contact');
    const navLinks = document.querySelectorAll('.desktop-nav .nav-link');
    if (!sections.length || !navLinks.length) return;

    const observerOptions = {
      root: null,
      rootMargin: '-30% 0px -60% 0px',
      threshold: 0,
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          navLinks.forEach((link) => {
            const href = link.getAttribute('href');
            if (href === `#${id}`) {
              link.classList.add('active');
            } else {
              link.classList.remove('active');
            }
          });
        }
      });
    }, observerOptions);

    sections.forEach((sec) => observer.observe(sec));
  }

  // ---------------------------------------------------------------------------
  // 5. FRAGRANCE NOTES TABS (Top / Heart / Base)
  // ---------------------------------------------------------------------------
  function initNotesTabs() {
    const tabButtons = document.querySelectorAll('.notes-tab-btn');
    const tabPanels = document.querySelectorAll('.notes-panel');
    if (!tabButtons.length || !tabPanels.length) return;

    tabButtons.forEach((btn) => {
      btn.addEventListener('click', () => {
        const targetPanelId = btn.getAttribute('aria-controls');

        // Update Buttons
        tabButtons.forEach((b) => {
          b.classList.remove('active');
          b.setAttribute('aria-selected', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');

        // Update Panels
        tabPanels.forEach((panel) => {
          if (panel.id === targetPanelId) {
            panel.classList.add('active');
            panel.removeAttribute('hidden');
          } else {
            panel.classList.remove('active');
            panel.setAttribute('hidden', '');
          }
        });
      });

      // Keyboard arrow navigation for tabs
      btn.addEventListener('keydown', (e) => {
        let targetIdx = null;
        const btnList = Array.from(tabButtons);
        const currentIdx = btnList.indexOf(btn);

        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
          targetIdx = (currentIdx + 1) % btnList.length;
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
          targetIdx = (currentIdx - 1 + btnList.length) % btnList.length;
        }

        if (targetIdx !== null) {
          e.preventDefault();
          btnList[targetIdx].focus();
          btnList[targetIdx].click();
        }
      });
    });
  }

  // ---------------------------------------------------------------------------
  // 6. THE AURELIS COLLECTION INTERACTIVE SWITCHER
  // ---------------------------------------------------------------------------
  const collectionData = {
    noir: {
      title: 'NOIR ÉCLAT',
      edition: 'EDITION 01 · THE CANONICAL FLAGSHIP',
      concentration: 'EAU DE PARFUM · 100 ML · PARIS',
      image: './assets/product/noir-eclat-bottle.webp',
      alt: 'Noir Éclat Fragrance Bottle in Smoked Obsidian Glass',
      desc: 'The signature dark composition. Smoked obsidian flint crystal cradling a glowing inner core of warm cognac amber, illuminated by bergamot and pink pepper, anchored in Haitian vetiver.',
      top: 'Calabrian Bergamot, Madagascar Pink Pepper',
      heart: 'Florentine Iris Concrete, Mineral Violet Leaf',
      base: 'Smoked Haitian Vetiver, Atlas Cedar, Golden Amber',
      mood: 'Chiaroscuro, Quiet Authority, Velvety Shadow',
      auraClass: 'noir-aura',
    },
    eclat: {
      title: 'ÉCLAT',
      edition: 'EDITION 02 · LUMINOUS REINTERPRETATION',
      concentration: 'EAU DE PARFUM · 100 ML · PARIS',
      image: './assets/product/eclat-bottle.webp',
      alt: 'Éclat Fragrance Bottle in Luminous Clear Flint Glass',
      desc: 'A luminous, refined interpretation. Crystal-clear flint flacon housing a pale golden champagne aura. Crystalline citrus facets dissolve into soft white orris and sunlit cedarwood.',
      top: 'Italian Mandarin, White Neroli, Bergamot Zest',
      heart: 'White Iris Petals, Hedione, Crisp Linen',
      base: 'Sunlit Cedarwood, Light Ambergris, Cashmeran',
      mood: 'Luminosity, Architectural Radiance, Crisp Clarity',
      auraClass: 'eclat-aura',
    },
    ambre: {
      title: 'AMBRE',
      edition: 'EDITION 03 · SENSUAL WARMTH',
      concentration: 'EAU DE PARFUM · 100 ML · PARIS',
      image: './assets/product/ambre-bottle.webp',
      alt: 'Ambre Fragrance Bottle in Smoked Copper Glass',
      desc: 'A warm, sensual composition. Deep copper smoked glass preserving a rich honeyed amber resin core. Spiced cardamon and roasted tonka bean create an intimate, intoxicating drydown.',
      top: 'Ceylon Cardamon, Bitter Orange, Saffron Hair',
      heart: 'Roasted Tonka Bean, Benzoin Tear, Cinnamon Bark',
      base: 'Fossilized Amber, Dark Patchouli, Labdanum Resin',
      mood: 'Intimacy, Smoldering Caustics, Velvety Warmth',
      auraClass: 'ambre-aura',
    },
  };

  function initCollectionSwitcher() {
    const buttons = document.querySelectorAll('.collection-btn');
    const bottleImg = document.getElementById('collectionBottleImg');
    const bottleAura = document.getElementById('collectionAura');
    const editionEl = document.getElementById('collectionEdition');
    const titleEl = document.getElementById('collectionTitle');
    const concEl = document.getElementById('collectionConcentration');
    const descEl = document.getElementById('collectionDesc');
    const topEl = document.getElementById('collectionTop');
    const heartEl = document.getElementById('collectionHeart');
    const baseEl = document.getElementById('collectionBase');
    const moodEl = document.getElementById('collectionMood');

    if (!buttons.length || !bottleImg) return;

    buttons.forEach((btn) => {
      btn.addEventListener('click', () => {
        const fragKey = btn.getAttribute('data-fragrance');
        const data = collectionData[fragKey];
        if (!data) return;

        // Update Buttons
        buttons.forEach((b) => {
          b.classList.remove('active');
          b.setAttribute('aria-selected', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');

        // Smooth Crossfade on Bottle Image
        bottleImg.style.opacity = '0';
        bottleImg.style.transform = 'translateY(8px)';

        setTimeout(() => {
          bottleImg.src = data.image;
          bottleImg.alt = data.alt;
          if (editionEl) editionEl.textContent = data.edition;
          if (titleEl) titleEl.textContent = data.title;
          if (concEl) concEl.textContent = data.concentration;
          if (descEl) descEl.textContent = data.desc;
          if (topEl) topEl.textContent = data.top;
          if (heartEl) heartEl.textContent = data.heart;
          if (baseEl) baseEl.textContent = data.base;
          if (moodEl) moodEl.textContent = data.mood;

          if (bottleAura) {
            bottleAura.className = `bottle-aura ${data.auraClass}`;
          }

          bottleImg.style.opacity = '1';
          bottleImg.style.transform = 'translateY(0)';
        }, 220);
      });

      // Keyboard arrow navigation for collection tabs
      btn.addEventListener('keydown', (e) => {
        let targetIdx = null;
        const btnList = Array.from(buttons);
        const currentIdx = btnList.indexOf(btn);

        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
          targetIdx = (currentIdx + 1) % btnList.length;
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
          targetIdx = (currentIdx - 1 + btnList.length) % btnList.length;
        }

        if (targetIdx !== null) {
          e.preventDefault();
          btnList[targetIdx].focus();
          btnList[targetIdx].click();
        }
      });
    });
  }

  // ---------------------------------------------------------------------------
  // 7. CAMPAIGN VIDEO THEATRE CONTROLS (ACTIVE H.264 PLAYABLE MASTER & FALLBACK)
  // ---------------------------------------------------------------------------
  function initVideoPlayer() {
    const video = document.getElementById('campaignVideo');
    const container = document.getElementById('videoContainer');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const playIcon = document.getElementById('playIcon');
    const pauseIcon = document.getElementById('pauseIcon');
    const fallback = document.getElementById('videoFallback');

    if (!playPauseBtn || !video) return;

    const updatePlayState = (isPlaying) => {
      if (isPlaying) {
        if (playIcon) playIcon.classList.add('hidden');
        if (pauseIcon) pauseIcon.classList.remove('hidden');
        if (container) container.classList.add('playing');
        playPauseBtn.setAttribute('aria-label', 'Pause campaign film');
      } else {
        if (playIcon) playIcon.classList.remove('hidden');
        if (pauseIcon) pauseIcon.classList.add('hidden');
        if (container) container.classList.remove('playing');
        playPauseBtn.setAttribute('aria-label', 'Play campaign film');
      }
    };

    const activateFallback = () => {
      if (fallback) {
        fallback.classList.remove('hidden');
        fallback.setAttribute('aria-hidden', 'false');
      }
      video.style.display = 'none';
      video.pause();
      if (container) {
        container.classList.remove('playing');
        container.classList.add('fallback-active');
      }
      if (playPauseBtn) {
        playPauseBtn.disabled = true;
        playPauseBtn.style.opacity = '0.35';
        playPauseBtn.style.cursor = 'not-allowed';
        playPauseBtn.setAttribute('aria-label', 'Video unavailable — animated storyboard preview active');
      }
      const runtimeBadge = document.querySelector('.film-runtime');
      if (runtimeBadge) {
        runtimeBadge.textContent = 'STORYBOARD PREVIEW';
      }
      const footnote = document.querySelector('.film-footnote p');
      if (footnote) {
        footnote.textContent = '* ANIMATED STORYBOARD PREVIEW · FINAL MP4 UNAVAILABLE — Self-initiated concept storyboard preview displayed.';
      }
    };

    const handleVideoToggle = () => {
      if (video.paused || video.ended) {
        const playPromise = video.play();
        if (playPromise !== undefined) {
          playPromise
            .then(() => {
              updatePlayState(true);
            })
            .catch((err) => {
              console.warn('Video playback notice:', err);
              if (video.error) {
                activateFallback();
              }
            });
        }
      } else {
        video.pause();
        updatePlayState(false);
      }
    };

    playPauseBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      handleVideoToggle();
    });

    playPauseBtn.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        handleVideoToggle();
      }
    });

    video.addEventListener('play', () => updatePlayState(true));
    video.addEventListener('pause', () => updatePlayState(false));
    video.addEventListener('ended', () => updatePlayState(false));

    // Handle error events cleanly to activate visual fallback
    video.addEventListener('error', (e) => {
      console.warn('Video failed to load, activating visual fallback:', e);
      activateFallback();
    });

    const sourceEl = video.querySelector('source');
    if (sourceEl) {
      sourceEl.addEventListener('error', (e) => {
        console.warn('Video source failed to load, activating visual fallback:', e);
        activateFallback();
      });
    }
  }

  // ---------------------------------------------------------------------------
  // 8. LIGHTBOX MODAL FOR GALLERY CARDS
  // ---------------------------------------------------------------------------
  function initLightbox() {
    const galleryCards = document.querySelectorAll('.gallery-card');
    const modal = document.getElementById('imageLightbox');
    const modalImg = document.getElementById('lightboxImg');
    const modalCaption = document.getElementById('lightboxCaption');
    const closeBtn = document.getElementById('lightboxClose');

    if (!modal || !modalImg) return;

    const openModal = (imgSrc, captionText) => {
      modalImg.src = imgSrc;
      if (modalCaption) modalCaption.textContent = captionText || '';
      modal.classList.add('active');
      modal.setAttribute('aria-hidden', 'false');
      document.body.classList.add('drawer-open');
      if (closeBtn) closeBtn.focus();
    };

    const closeModal = () => {
      modal.classList.remove('active');
      modal.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('drawer-open');
    };

    galleryCards.forEach((card) => {
      const img = card.querySelector('.gallery-img');
      const title = card.querySelector('.card-heading');
      if (img) {
        card.addEventListener('click', () => {
          openModal(img.src, title ? title.textContent : '');
        });
        card.addEventListener('keydown', (e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            openModal(img.src, title ? title.textContent : '');
          }
        });
      }
    });

    if (closeBtn) closeBtn.addEventListener('click', closeModal);

    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('active')) {
        closeModal();
      }
    });
  }

  // ---------------------------------------------------------------------------
  // 9. SCROLL REVEAL ANIMATIONS (IntersectionObserver)
  // ---------------------------------------------------------------------------
  function initScrollReveals() {
    const reveals = document.querySelectorAll('.reveal-element');
    if (!reveals.length) return;

    // Check for prefers-reduced-motion
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      reveals.forEach((el) => {
        el.classList.add('revealed');
        el.classList.add('is-revealed');
      });
      return;
    }

    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            entry.target.classList.add('is-revealed');
            observer.unobserve(entry.target);
          }
        });
      },
      {
        root: null,
        rootMargin: '0px 0px -5% 0px',
        threshold: 0.08,
      }
    );

    reveals.forEach((el) => revealObserver.observe(el));
  }

  // ---------------------------------------------------------------------------
  // 10. BACK TO TOP BUTTON
  // ---------------------------------------------------------------------------
  function initBackToTop() {
    const backBtn = document.getElementById('backToTopBtn');
    if (!backBtn) return;

    backBtn.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth',
      });
    });
  }

  // ---------------------------------------------------------------------------
  // INITIALIZATION
  // ---------------------------------------------------------------------------
  document.addEventListener('DOMContentLoaded', () => {
    initPreloader();
    initHeaderScroll();
    initMobileNav();
    initActiveNavTracking();
    initNotesTabs();
    initCollectionSwitcher();
    initVideoPlayer();
    initLightbox();
    initScrollReveals();
    initBackToTop();
  });
})();
