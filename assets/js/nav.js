// Navigation - scroll-hide header + mobile hamburger menu
(function() {
  document.addEventListener('DOMContentLoaded', function() {
    var masthead = document.querySelector('.masthead');
    var navToggle = document.querySelector('.nav-toggle');
    var mobileNav = document.querySelector('.mobile-nav');
    var navOverlay = document.querySelector('.nav-overlay');
    var lastScroll = 0;
    var scrollThreshold = 10;

    // Scroll-hide header
    if (masthead) {
      window.addEventListener('scroll', function() {
        var currentScroll = window.pageYOffset;
        if (Math.abs(currentScroll - lastScroll) < scrollThreshold) return;

        if (currentScroll > lastScroll && currentScroll > 56) {
          masthead.classList.add('is-hidden');
          closeMobileNav();
        } else {
          masthead.classList.remove('is-hidden');
        }
        lastScroll = currentScroll;
      }, { passive: true });
    }

    // Mobile menu toggle
    function closeMobileNav() {
      if (navToggle) navToggle.classList.remove('is-active');
      if (mobileNav) mobileNav.classList.remove('is-open');
      if (navOverlay) navOverlay.style.display = 'none';
      document.body.style.overflow = '';
    }

    if (navToggle && mobileNav) {
      navToggle.addEventListener('click', function() {
        var isOpen = mobileNav.classList.contains('is-open');
        if (isOpen) {
          closeMobileNav();
        } else {
          navToggle.classList.add('is-active');
          mobileNav.classList.add('is-open');
          if (navOverlay) navOverlay.style.display = 'block';
          document.body.style.overflow = 'hidden';
        }
      });
    }

    if (navOverlay) {
      navOverlay.addEventListener('click', closeMobileNav);
    }

    // Close mobile nav on escape key
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeMobileNav();
    });
  });
})();
