// Dark mode toggle - reads preference from localStorage, falls back to system
(function() {
  var theme = localStorage.getItem('theme');
  if (theme) {
    document.documentElement.setAttribute('data-theme', theme);
  }

  document.addEventListener('DOMContentLoaded', function() {
    var toggle = document.querySelector('.theme-toggle');
    if (!toggle) return;

    function updateIcon() {
      var current = document.documentElement.getAttribute('data-theme');
      var isDark = current === 'dark' ||
        (!current && window.matchMedia('(prefers-color-scheme: dark)').matches);
      toggle.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
      toggle.textContent = isDark ? '\u2600' : '\u263E';
    }

    toggle.addEventListener('click', function() {
      var current = document.documentElement.getAttribute('data-theme');
      var isDark = current === 'dark' ||
        (!current && window.matchMedia('(prefers-color-scheme: dark)').matches);
      var newTheme = isDark ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      updateIcon();
    });

    updateIcon();
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateIcon);
  });
})();
