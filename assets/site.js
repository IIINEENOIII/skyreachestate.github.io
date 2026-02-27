// simple intersection animation
const els = document.querySelectorAll('.fade-in');
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) e.target.classList.add('show');
  });
}, {threshold: 0.12});

els.forEach(el => io.observe(el));

// set year
const y = document.getElementById('year');
if (y) y.textContent = new Date().getFullYear();
