/**
 * Landing Page — Envelope Intro & Animations
 */

/* ======================================
   Envelope Intro
   ====================================== */
(function () {
    if (!document.body.classList.contains('envelope-sealed')) return;

    var overlay = document.getElementById('envelope-overlay');
    var seal = document.getElementById('envelope-seal');
    var sealAvatar = seal.querySelector('.seal-avatar');
    var heroAvatar = document.querySelector('.hero-avatar');

    // Respect reduced-motion: skip animation entirely
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        overlay.remove();
        document.body.classList.remove('envelope-sealed');
        sessionStorage.setItem('envelope-opened', '1');
        return;
    }

    seal.addEventListener('click', function () {
        // Prevent double interaction
        seal.style.pointerEvents = 'none';

        // Stop breathing animation so transform is clean
        sealAvatar.style.animation = 'none';

        // Measure hero avatar's natural (final) position
        // Temporarily override the sealed suppression to get the true layout rect
        heroAvatar.style.cssText = 'opacity:0!important;transform:none!important;animation:none!important;';
        var heroRect = heroAvatar.getBoundingClientRect();
        heroAvatar.style.cssText = '';

        // Measure seal avatar's current position
        var sealRect = sealAvatar.getBoundingClientRect();

        // Calculate movement
        var dx = (heroRect.left + heroRect.width / 2) - (sealRect.left + sealRect.width / 2);
        var dy = (heroRect.top + heroRect.height / 2) - (sealRect.top + sealRect.height / 2);
        var scale = heroRect.width / sealRect.width;

        // Phase 1: Brief "seal break" pulse (tactile click feedback)
        sealAvatar.style.transition = 'transform 0.12s ease-out';
        sealAvatar.style.transform = 'scale(1.08)';

        setTimeout(function () {
            // Phase 2: Flaps fly open + seal moves to hero position
            overlay.classList.add('opening');

            sealAvatar.style.transition =
                'transform 0.88s cubic-bezier(0.22, 1, 0.36, 1), ' +
                'box-shadow 0.88s cubic-bezier(0.22, 1, 0.36, 1)';
            sealAvatar.style.transform =
                'translate(' + dx + 'px, ' + dy + 'px) scale(' + scale + ')';
            sealAvatar.style.boxShadow =
                '0 0 0 4px var(--color-bg), 0 0 0 6px var(--color-accent)';

            // Phase 3: Cleanup — reveal hero content
            setTimeout(function () {
                // Place hero avatar at its final state instantly
                heroAvatar.style.opacity = '1';
                heroAvatar.style.transform = 'translateY(0)';
                heroAvatar.style.animation = 'none';

                // Remove overlay from DOM
                overlay.remove();

                // Unlock hero animations (removing sealed class lets heroFadeUp play)
                document.body.classList.remove('envelope-sealed');

                // Remember for this browser tab session
                sessionStorage.setItem('envelope-opened', '1');
            }, 900);
        }, 140);
    });
})();

/* ======================================
   Card Grid Scroll Reveal
   ====================================== */
document.addEventListener('DOMContentLoaded', function () {
    var cardsGrid = document.querySelector('.cards-grid');

    if (cardsGrid) {
        var cardsObserver = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('revealed');
                        cardsObserver.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
        );

        cardsObserver.observe(cardsGrid);
    }

    /* ======================================
       Scroll Indicator → Cards Section
       ====================================== */
    var scrollIndicator = document.querySelector('.scroll-indicator');
    var cardsSection = document.querySelector('.cards-section');

    if (scrollIndicator && cardsSection) {
        scrollIndicator.addEventListener('click', function () {
            cardsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    }
});
