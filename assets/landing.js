/**
 * Landing Page Interactions
 */

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
