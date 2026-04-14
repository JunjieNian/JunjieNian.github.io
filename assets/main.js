/**
 * Navigation Highlighting & Scroll Reveal Animations
 */
document.addEventListener('DOMContentLoaded', function () {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.content > section');

    /* ======================================
       Navigation Highlighting (IntersectionObserver)
       ====================================== */
    const navObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    navLinks.forEach((link) => link.classList.remove('active'));
                    const activeLink = document.querySelector(
                        `.nav-link[data-section="${entry.target.id}"]`
                    );
                    if (activeLink) activeLink.classList.add('active');
                }
            });
        },
        { root: null, rootMargin: '-50% 0px -50% 0px', threshold: 0 }
    );

    sections.forEach((section) => navObserver.observe(section));

    /* ======================================
       Smooth Scroll on Nav Click
       ====================================== */
    navLinks.forEach((link) => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('data-section');
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                navLinks.forEach((l) => l.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });

    /* ======================================
       Scroll Reveal Animations
       ====================================== */
    const revealElements = document.querySelectorAll('.reveal');

    const revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    revealObserver.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
    );

    revealElements.forEach((el) => revealObserver.observe(el));
});
