// GitHubBook - 公共JS
(function () {
  'use strict';

  // ---- 返回顶部 ----
  const backBtn = document.querySelector('.back-to-top');
  if (backBtn) {
    window.addEventListener('scroll', () => {
      backBtn.classList.toggle('visible', window.scrollY > 400);
    });
    backBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ---- 激活当前导航 ----
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href') || '';
    if (
      (path === 'index.html' && href === 'index.html') ||
      (path === '' && href === 'index.html') ||
      (path !== 'index.html' && href.includes(path.replace('.html', '')))
    ) {
      link.classList.add('active');
    }
  });

  // ---- 语言颜色映射 ----
  const langColors = {
    TypeScript: '#3178c6',
    JavaScript: '#f1e05a',
    Python: '#3572A5',
    Rust: '#dea584',
    Go: '#00ADD8',
    Java: '#b07219',
    Ruby: '#701516',
    Shell: '#89e051',
    C: '#555555',
    'C++': '#f34b7d',
    HTML: '#e34c26',
    CSS: '#563d7c',
    Swift: '#F05138',
    Kotlin: '#A97BFF',
  };

  document.querySelectorAll('[data-lang]').forEach(el => {
    const lang = el.dataset.lang;
    if (langColors[lang]) {
      el.style.background = langColors[lang];
    }
  });

  // ---- 数字动画 ----
  function animateNum(el, target) {
    let start = 0;
    const duration = 1000;
    const step = target / (duration / 16);
    const timer = setInterval(() => {
      start += step;
      if (start >= target) {
        el.textContent = target.toLocaleString();
        clearInterval(timer);
      } else {
        el.textContent = Math.floor(start).toLocaleString();
      }
    }, 16);
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const val = parseInt(el.dataset.count || '0', 10);
        if (val > 0) animateNum(el, val);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.2 });

  document.querySelectorAll('[data-count]').forEach(el => observer.observe(el));

  // ---- 订阅表单 ----
  const subscribeForm = document.querySelector('.subscribe-form');
  if (subscribeForm) {
    subscribeForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = subscribeForm.querySelector('.subscribe-input');
      if (input && input.value) {
        const btn = subscribeForm.querySelector('.subscribe-btn');
        btn.textContent = '✓ 已订阅！';
        btn.style.background = '#3fb950';
        input.value = '';
        setTimeout(() => {
          btn.textContent = '订阅';
          btn.style.background = '';
        }, 3000);
      }
    });
  }

  // ---- 语言进度条动画 ----
  const langBars = document.querySelectorAll('.lang-bar');
  const barObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.width = entry.target.dataset.width || '0%';
        barObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  langBars.forEach(bar => {
    const target = bar.style.width;
    bar.style.width = '0%';
    bar.dataset.width = target;
    barObserver.observe(bar);
  });

})();
