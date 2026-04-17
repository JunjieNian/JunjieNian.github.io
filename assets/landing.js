/**
 * Landing Page Animations
 */
document.addEventListener('DOMContentLoaded', function () {
    /* ======================================
       Card Grid Scroll Reveal
       ====================================== */
    const cardsGrid = document.querySelector('.cards-grid');

    if (cardsGrid) {
        const cardsObserver = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
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
    const scrollIndicator = document.querySelector('.scroll-indicator');
    const cardsSection = document.querySelector('.cards-section');

    if (scrollIndicator && cardsSection) {
        scrollIndicator.addEventListener('click', function () {
            cardsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    }
});
