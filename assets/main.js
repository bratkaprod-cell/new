// reveal on scroll
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      io.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

// fake-but-honest urgency timer: "free diagnostics slots today"
const slotsEl = document.getElementById('slots');
if (slotsEl) {
  const h = new Date().getHours();
  slotsEl.textContent = Math.max(2, 7 - Math.floor(h / 4));
}

// mobile burger menu (right-side drawer)
const burger = document.getElementById('burger');
const mobileMenu = document.getElementById('mobile-menu');
const mmOverlay = document.getElementById('mm-overlay');
const mmClose = document.getElementById('mm-close');
if (burger && mobileMenu) {
  const setMenu = (open) => {
    mobileMenu.classList.toggle('open', open);
    if (mmOverlay) mmOverlay.classList.toggle('open', open);
    burger.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
    mobileMenu.setAttribute('aria-hidden', String(!open));
    lockScroll(open);
  };
  burger.addEventListener('click', () => setMenu(!mobileMenu.classList.contains('open')));
  if (mmOverlay) mmOverlay.addEventListener('click', () => setMenu(false));
  if (mmClose) mmClose.addEventListener('click', () => setMenu(false));
  mobileMenu.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => setMenu(false)));
}

// scroll lock without layout shift
const lockScroll = (on) => {
  if (on) {
    const sbw = window.innerWidth - document.documentElement.clientWidth;
    document.documentElement.style.setProperty('--sbw', sbw + 'px');
  }
  document.body.classList.toggle('modal-open', on);
};

// lead modal
const modal = document.getElementById('lead-modal');
if (modal) {
  const box = modal.querySelector('.modal');
  const cmsEl = document.getElementById('modal-cms');
  const openModal = (cms) => {
    if (cmsEl) cmsEl.textContent = cms ? 'на ' + cms : '';
    box.classList.remove('sent');
    modal.classList.add('open');
    lockScroll(true);
    const first = modal.querySelector('input');
    if (first) setTimeout(() => first.focus(), 250);
  };
  const closeModal = () => {
    modal.classList.remove('open');
    lockScroll(false);
  };
  document.querySelectorAll('.js-open-modal').forEach((btn) =>
    btn.addEventListener('click', (ev) => {
      ev.preventDefault();
      ev.stopPropagation();
      openModal(btn.dataset.cms || '');
    })
  );
  modal.addEventListener('click', (ev) => {
    if (ev.target === modal) closeModal();
  });
  const closeBtn = document.getElementById('modal-close');
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  document.addEventListener('keydown', (ev) => {
    if (ev.key === 'Escape' && modal.classList.contains('open')) closeModal();
  });
  const modalForm = document.getElementById('modal-form');
  if (modalForm) {
    modalForm.addEventListener('submit', (ev) => {
      ev.preventDefault();
      if (!validateLeadForm(modalForm)) return;
      box.classList.add('sent');
    });
  }
}

// --- phone mask: +7 (XXX) XXX-XX-XX ---
const formatPhone = (digits) => {
  let d = digits.replace(/\D/g, '');
  if (d.startsWith('8')) d = '7' + d.slice(1);
  if (d.startsWith('7')) d = d.slice(1);
  if (d.length >= 11 && (d[0] === '7' || d[0] === '8')) d = d.slice(1);
  d = d.slice(0, 10);
  let out = '+7';
  if (d.length > 0) out += ' (' + d.slice(0, 3);
  if (d.length >= 3) out += ')';
  if (d.length > 3) out += ' ' + d.slice(3, 6);
  if (d.length > 6) out += '-' + d.slice(6, 8);
  if (d.length > 8) out += '-' + d.slice(8, 10);
  return out;
};
const phoneDigits = (value) => {
  let d = value.replace(/\D/g, '');
  if (d.startsWith('8')) d = '7' + d.slice(1);
  if (!d.startsWith('7')) d = '7' + d;
  return d;
};
document.querySelectorAll('input.js-phone').forEach((inp) => {
  const nationalDigits = () => {
    let d = inp.value.replace(/\D/g, '');
    if (d.startsWith('8')) d = '7' + d.slice(1);
    if (d.startsWith('7')) d = d.slice(1);
    return d.slice(0, 10);
  };
  const setValue = (d) => {
    inp.value = formatPhone('7' + d);
    const end = inp.value.length;
    inp.setSelectionRange(end, end);
  };
  inp.addEventListener('focus', () => {
    if (!inp.value) inp.value = '+7 (';
  });
  inp.addEventListener('blur', () => {
    if (inp.value === '+7 (' || inp.value === '+7') inp.value = '';
  });
  // digits are always appended in order, regardless of caret position
  inp.addEventListener('keydown', (ev) => {
    if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
    if (ev.key.length === 1) {
      ev.preventDefault();
      if (/\d/.test(ev.key)) {
        const d = nationalDigits();
        if (d.length < 10) setValue(d + ev.key);
      }
    } else if (ev.key === 'Backspace' || ev.key === 'Delete') {
      ev.preventDefault();
      const d = nationalDigits();
      if (d.length > 0) setValue(d.slice(0, -1));
      else inp.value = '+7 (';
    }
  });
  // paste / autofill / mobile keyboards
  inp.addEventListener('input', () => {
    inp.value = inp.value ? formatPhone(inp.value) : '';
    const end = inp.value.length;
    inp.setSelectionRange(end, end);
  });
  inp.addEventListener('paste', (ev) => {
    ev.preventDefault();
    const text = (ev.clipboardData || window.clipboardData).getData('text');
    inp.value = formatPhone(text);
  });
});

// --- name field: letters only ---
document.querySelectorAll('input[name="name"]').forEach((inp) => {
  inp.addEventListener('keydown', (ev) => {
    if (ev.key.length === 1 && /[\d]/.test(ev.key)) ev.preventDefault();
  });
  inp.addEventListener('input', () => {
    const clean = inp.value.replace(/[0-9]/g, '');
    if (clean !== inp.value) inp.value = clean;
  });
});

// --- anti-spam + validation ---
const PAGE_LOADED_AT = Date.now();
const RATE_KEY = 'sr24_leads';
const submitsAllowed = () => {
  let list = [];
  try { list = JSON.parse(localStorage.getItem(RATE_KEY)) || []; } catch (e) { list = []; }
  const now = Date.now();
  list = list.filter((t) => now - t < 10 * 60 * 1000);
  if (list.length >= 3) return false;
  list.push(now);
  try { localStorage.setItem(RATE_KEY, JSON.stringify(list)); } catch (e) {}
  return true;
};
const showError = (form, msg) => {
  const el = form.querySelector('.form-error');
  if (el) el.textContent = msg;
};
const validPhone = (value) => {
  const d = phoneDigits(value);
  if (d.length !== 11) return false;
  if (!/^7[3489]\d{9}$/.test(d)) return false;
  if (/^7(\d)\1{9}$/.test(d)) return false;
  return true;
};
const validSite = (value) => {
  let v = value.trim();
  if (!v) return false;
  if (!/^https?:\/\//i.test(v)) v = 'https://' + v;
  let u;
  try { u = new URL(v); } catch (e) { return false; }
  if (u.protocol !== 'http:' && u.protocol !== 'https:') return false;
  return /^([a-z0-9а-яё-]+\.)+([a-zа-яё]{2,}|xn--[a-z0-9-]{2,})$/i.test(u.hostname);
};
const validateLeadForm = (form) => {
  showError(form, '');
  const hp = form.querySelector('.hp-field');
  if (hp && hp.value) return false; // honeypot: silently drop bots
  if (Date.now() - PAGE_LOADED_AT < 3000) {
    showError(form, 'Подождите пару секунд и попробуйте ещё раз.');
    return false;
  }
  const name = form.querySelector('input[name="name"]');
  if (name && name.value.trim().length < 2) {
    showError(form, 'Введите ваше имя.');
    name.focus();
    return false;
  }
  const site = form.querySelector('input[name="site"]');
  if (site && !validSite(site.value)) {
    showError(form, 'Введите корректный адрес сайта, например site.ru');
    site.focus();
    return false;
  }
  const phone = form.querySelector('input.js-phone');
  if (phone && !validPhone(phone.value)) {
    showError(form, 'Введите корректный номер: +7 (XXX) XXX-XX-XX');
    phone.focus();
    return false;
  }
  if (!submitsAllowed()) {
    showError(form, 'Слишком много заявок. Позвоните нам или напишите в Telegram.');
    return false;
  }
  return true;
};

// form
const form = document.getElementById('lead-form');
if (form) {
  form.addEventListener('submit', (ev) => {
    ev.preventDefault();
    if (!validateLeadForm(form)) return;
    const btn = form.querySelector('button[type="submit"]');
    btn.textContent = 'Заявка отправлена ✓';
    btn.disabled = true;
    btn.style.background = 'linear-gradient(135deg,#10b981,#34d399)';
  });
}
