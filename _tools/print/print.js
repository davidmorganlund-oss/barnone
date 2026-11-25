// Adds the running footer and page number to every page except the cover,
// then flags any page whose content runs into the footer (the build script reads the flags).
(function () {
  var text = document.body.getAttribute('data-footer') || '';
  var pages = document.querySelectorAll('.page');
  pages.forEach(function (page, i) {
    if (page.classList.contains('cover')) return;
    var f = document.createElement('div');
    f.className = 'pf';
    var left = document.createElement('span');
    if (page.classList.contains('end')) {
      var img = document.createElement('img');
      img.src = '../../phoenix.png';
      img.alt = '';
      left.appendChild(img);
    }
    left.appendChild(document.createTextNode(text));
    var right = document.createElement('span');
    right.textContent = String(i + 1);
    f.appendChild(left);
    f.appendChild(right);
    page.appendChild(f);
  });
  window.checkOverflow = function () {
    var problems = [];
    pages.forEach(function (page, i) {
      var limit = page.getBoundingClientRect().bottom;
      var foot = page.querySelector('.pf');
      if (foot) limit = foot.getBoundingClientRect().top - 4;
      var worst = 0, culprit = '';
      page.querySelectorAll('*').forEach(function (el) {
        if (el.closest('.pf') || el.closest('.art') || el.classList.contains('p16dark')) return;
        var r = el.getBoundingClientRect();
        if (r.height === 0) return;
        if (r.bottom > limit + 0.5 && r.bottom - limit > worst) {
          worst = r.bottom - limit;
          culprit = el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ').join('.') : '')
            + ' "' + (el.textContent || '').trim().slice(0, 40) + '"';
        }
        if (r.right > page.getBoundingClientRect().right - 53) {
          var over = r.right - (page.getBoundingClientRect().right - 54);
          if (over > 1 && !page.classList.contains('cover')) worst = Math.max(worst, 0.01);
        }
      });
      // room left at the bottom, so tight pages can be spotted too
      var last = 0;
      page.querySelectorAll(':scope > *:not(.pf):not(.art)').forEach(function (el) {
        if (getComputedStyle(el).position === 'absolute') return;
        last = Math.max(last, el.getBoundingClientRect().bottom);
      });
      problems.push({ page: i + 1, overflow_px: Math.round(worst * 10) / 10, room_px: Math.round((limit - last) * 10) / 10, culprit: culprit });
    });
    return problems;
  };
})();
