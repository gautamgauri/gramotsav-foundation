// Mobile nav toggle
document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      links.classList.toggle('open');
    });
  }
});

// Contact form -> mailto (no server needed on GitHub Pages)
document.addEventListener('DOMContentLoaded', function () {
  var form = document.getElementById('contact-form');
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = function (id) { var el = document.getElementById(id); return el ? el.value.trim() : ''; };
    var subject = '[Website] ' + v('cf-topic') + ' — ' + (v('cf-name') || 'enquiry');
    var body = 'Name: ' + v('cf-name') + '\n'
             + 'Organisation: ' + (v('cf-org') || '—') + '\n'
             + 'Topic: ' + v('cf-topic') + '\n\n'
             + v('cf-msg') + '\n';
    window.location.href = 'mailto:gramotsavfoundation@gmail.com'
      + '?subject=' + encodeURIComponent(subject)
      + '&body=' + encodeURIComponent(body);
  });
});

// Nav toggle: keep aria-expanded honest
document.addEventListener('DOMContentLoaded', function () {
  var t = document.querySelector('.nav-toggle');
  if (!t) return;
  t.addEventListener('click', function () {
    var links = document.querySelector('.nav-links');
    t.setAttribute('aria-expanded', links && links.classList.contains('open') ? 'true' : 'false');
  });
});
