// Mobile menu and dropdown toggles
document.addEventListener('DOMContentLoaded', function () {
  var menuBtn = document.querySelector('.menu-btn');
  if (menuBtn) {
    menuBtn.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      menuBtn.setAttribute('aria-expanded', open);
    });
  }
  document.querySelectorAll('.sub-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var li = btn.parentElement;
      var open = li.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
    });
  });
  // Count-up numbers: each figure counts from 1 to its value when the row scrolls into view.
  // The final text (e.g. "30+", "100s", "100-vis") stays in the page for search engines and no-JS visitors.
  var counters = document.querySelectorAll('.numbers-row strong');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (counters.length && 'IntersectionObserver' in window && !reduce) {
    var run = function (el) {
      var finalText = el.getAttribute('data-final');
      var target = parseInt(finalText, 10);
      if (!target) { el.textContent = finalText; return; }
      var start = null, duration = 1600;
      var step = function (t) {
        if (start === null) start = t;
        var p = Math.min((t - start) / duration, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.max(1, Math.round(1 + (target - 1) * eased));
        if (p < 1) requestAnimationFrame(step); else el.textContent = finalText;
      };
      requestAnimationFrame(step);
    };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { run(e.target); io.unobserve(e.target); }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) {
      el.setAttribute('data-final', el.textContent.trim());
      el.style.minWidth = el.offsetWidth + 'px';
      el.textContent = '1';
      io.observe(el);
    });
  }
  // Chapter guide: highlight the chapter being read in the sticky contents list
  var chapLinks = document.querySelectorAll('.chap-nav a[href^="#"]');
  var chaps = document.querySelectorAll('.chap[id]');
  if (chapLinks.length && chaps.length) {
    var current = null, ticking = false;
    var update = function () {
      ticking = false;
      var id = chaps[0].id;
      chaps.forEach(function (c) { if (c.getBoundingClientRect().top < 180) id = c.id; });
      if (id === current) return;
      current = id;
      chapLinks.forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + id); });
    };
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
});
