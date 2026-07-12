// ResumeIQ - shared front-end behavior (theme toggle, auto-dismiss alerts)

(function () {
  const root = document.documentElement;
  const toggleBtn = document.getElementById('themeToggle');
  const iconSun = document.getElementById('iconSun');
  const iconMoon = document.getElementById('iconMoon');

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    if (iconSun && iconMoon) {
      iconSun.style.display = theme === 'dark' ? 'none' : 'inline';
      iconMoon.style.display = theme === 'dark' ? 'inline' : 'none';
    }
  }

  const saved = localStorage.getItem('resumeiq-theme');
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(saved || (prefersDark ? 'dark' : 'light'));

  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      const current = root.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      localStorage.setItem('resumeiq-theme', next);
    });
  }

  // Auto-dismiss flash alerts after 5 seconds
  document.querySelectorAll('.alert').forEach((alertEl) => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
      bsAlert.close();
    }, 5000);
  });
})();
