document.querySelectorAll('[data-copy]').forEach(function (b) {
  b.addEventListener('click', function () {
    var t = b.getAttribute('data-copy'), done = function () { b.textContent = 'Copied'; setTimeout(function () { b.textContent = 'Copy'; }, 1800); };
    try {
      navigator.clipboard.writeText(t).then(done, function () { sel(b); });
    } catch (e) { sel(b); }
  });
});
function sel(b) {
  var v = b.parentNode.querySelector('.val'); if (!v) return;
  var r = document.createRange(); r.selectNodeContents(v);
  var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
  b.textContent = 'Press Ctrl/Cmd+C';
}
(function () {
  var t = document.getElementById('nav-toggle');
  document.querySelectorAll('.site-nav a').forEach(function (a) { a.addEventListener('click', function () { if (t) t.checked = false; }); });
})();
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) return;
  document.documentElement.classList.add('js-motion');

  // Scroll reveals: section heads, cards, pillars, guides, facts
  var targets = document.querySelectorAll('main .section-head, main .card, main .pillar, main .guide, main .fact, main .help-item, main .panel li, main .timeline li');
  targets.forEach(function (el) { if (el.getBoundingClientRect().top > window.innerHeight) el.classList.add('reveal'); });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });

  // Chart: bars grow and numbers count up when seen
  var chart = document.querySelector('.chart');
  if (chart) {
    var fills = chart.querySelectorAll('.fill');
    var targetsN = Array.prototype.map.call(fills, function (f) { return parseInt(f.textContent, 10) || 0; });
    var started = false;
    function run() {
      if (started) return; started = true;
      chart.classList.add('in');
      var t0 = performance.now(), dur = 1400;
      (function tick(now) {
        var k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 3);
        fills.forEach(function (f, i) { f.textContent = Math.round(targetsN[i] * e); });
        if (k < 1) requestAnimationFrame(tick);
      })(t0);
    }
    if (chart.getBoundingClientRect().top < window.innerHeight * 0.85) chart.classList.add('in');
    else {
      var cio = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { run(); cio.disconnect(); } }, { threshold: .35 });
      cio.observe(chart);
    }
  }
  setTimeout(function () {
    document.querySelectorAll('.reveal').forEach(function (el) { if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add('in'); });
  }, 2500);

  // Embers rising behind the phoenix
  var c = document.querySelector('.embers');
  if (!c || !c.getContext) return;
  var ctx = c.getContext('2d'), W = 0, H = 0, dpr = Math.min(window.devicePixelRatio || 1, 2), parts = [], visible = true, raf = 0;
  var cs = getComputedStyle(document.documentElement);
  function col(v, fb) { return (cs.getPropertyValue(v) || fb).trim() || fb; }
  var colors = [col('--ember', '#f2a33a'), col('--red', '#e01e14')];
  function size() { var r = c.getBoundingClientRect(); W = r.width; H = r.height; c.width = W * dpr; c.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
  function spawn(fresh) {
    var right = W > 760 ? W * 0.55 : 0;
    return { x: right + Math.random() * (W - right), y: fresh ? Math.random() * H : H + 10, r: .8 + Math.random() * 2.2,
             vy: .25 + Math.random() * .7, vx: (Math.random() - .5) * .25, ph: Math.random() * 6.28,
             c: colors[Math.random() < .65 ? 0 : 1], life: 0 };
  }
  function init() { size(); var n = Math.round(Math.min(70, W / 18)); parts = []; for (var i = 0; i < n; i++) parts.push(spawn(true)); }
  function frame() {
    ctx.clearRect(0, 0, W, H);
    for (var i = 0; i < parts.length; i++) {
      var p = parts[i]; p.y -= p.vy; p.ph += .03; p.x += p.vx + Math.sin(p.ph) * .3; p.life++;
      var a = Math.max(0, Math.min(1, p.y / H)) * (.55 + .45 * Math.sin(p.ph * 2));
      ctx.globalAlpha = a * .85; ctx.fillStyle = p.c;
      ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.283); ctx.fill();
      if (p.y < -10) parts[i] = spawn(false);
    }
    ctx.globalAlpha = 1;
    raf = visible && !document.hidden ? requestAnimationFrame(frame) : 0;
  }
  function start() { if (!raf && visible && !document.hidden) raf = requestAnimationFrame(frame); }
  init(); start();
  window.addEventListener('resize', function () { init(); });
  document.addEventListener('visibilitychange', start);
  new IntersectionObserver(function (es) { visible = es[0].isIntersecting; start(); }).observe(c);
})();
