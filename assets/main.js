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
    if (!open && mobileMenu.contains(document.activeElement)) {
      document.activeElement.blur();
      burger.focus();
    }
    mobileMenu.classList.toggle('open', open);
    if (mmOverlay) mmOverlay.classList.toggle('open', open);
    burger.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
    mobileMenu.setAttribute('aria-hidden', String(!open));
    mobileMenu.inert = !open;
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
    modal.setAttribute('aria-hidden', 'false');
    modal.inert = false;
    lockScroll(true);
    const first = modal.querySelector('input');
    if (first) setTimeout(() => first.focus(), 250);
  };
  const closeModal = () => {
    if (modal.contains(document.activeElement)) document.activeElement.blur();
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    modal.inert = true;
    lockScroll(false);
  };
  document.querySelectorAll('.js-open-modal').forEach((btn) => {
    btn.addEventListener('click', (ev) => {
      ev.preventDefault();
      ev.stopPropagation();
      openModal(btn.dataset.cms || '');
    });
    btn.addEventListener('keydown', (ev) => {
      if (ev.key === 'Enter' || ev.key === ' ') {
        ev.preventDefault();
        openModal(btn.dataset.cms || '');
      }
    });
  });
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
      const cms = cmsEl ? cmsEl.textContent.replace(/^на\s+/, '') : '';
      sendLead(modalForm, cms, () => box.classList.add('sent'));
    });
  }

}

// quick "site + phone" forms: send the lead right away, no popup
document.querySelectorAll('.js-quick-form').forEach((qf) => {
  qf.addEventListener('submit', (ev) => {
    ev.preventDefault();
    showError(qf, '');
    const hp = qf.querySelector('.hp-field');
    if (hp && hp.value) return; // honeypot: silently drop bots
    if (Date.now() - PAGE_LOADED_AT < 3000) {
      showError(qf, 'Подождите пару секунд и попробуйте ещё раз.');
      return;
    }
    const site = qf.querySelector('input[name="site"]');
    if (!validSite(site.value)) {
      showError(qf, 'Введите корректный адрес сайта, например site.ru');
      site.focus();
      return;
    }
    const phone = qf.querySelector('input.js-phone');
    if (phone && !validPhone(phone.value)) {
      showError(qf, 'Введите корректный номер: +7 (XXX) XXX-XX-XX');
      phone.focus();
      return;
    }
    if (!submitsAllowed()) {
      showError(qf, 'Слишком много заявок. Позвоните нам или напишите в мессенджер.');
      return;
    }
    sendLead(qf, '');
  });
});

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
  const nationalDigits = (value) => {
    let d = value.replace(/\D/g, '');
    if (d.startsWith('8')) d = '7' + d.slice(1);
    if (d.startsWith('7')) d = d.slice(1);
    return d.slice(0, 10);
  };
  // how many national digits are before a caret position in the formatted value
  const digitIndexAt = (pos) => {
    const total = nationalDigits(inp.value).length;
    let count = 0;
    let skippedPrefix = false;
    for (let i = 0; i < Math.min(pos, inp.value.length); i++) {
      if (/\d/.test(inp.value[i])) {
        if (!skippedPrefix && inp.value[i] === '7' && inp.value.slice(0, i + 1).replace(/\D/g, '') === '7') {
          skippedPrefix = true;
          continue;
        }
        count++;
      }
    }
    return Math.min(count, total);
  };
  // caret position in the formatted value right after the n-th national digit
  const caretForDigit = (n) => {
    if (n <= 0) return Math.min(4, inp.value.length);
    let count = 0;
    let skippedPrefix = false;
    for (let i = 0; i < inp.value.length; i++) {
      if (/\d/.test(inp.value[i])) {
        if (!skippedPrefix && inp.value[i] === '7' && inp.value.slice(0, i + 1).replace(/\D/g, '') === '7') {
          skippedPrefix = true;
          continue;
        }
        count++;
        if (count === n) return i + 1;
      }
    }
    return inp.value.length;
  };
  const setValue = (d, caretDigit) => {
    inp.value = formatPhone('7' + d);
    const pos = caretDigit === undefined ? inp.value.length : caretForDigit(caretDigit);
    inp.setSelectionRange(pos, pos);
  };
  inp.addEventListener('focus', () => {
    if (!inp.value) inp.value = '+7 (';
  });
  inp.addEventListener('blur', () => {
    if (inp.value === '+7 (' || inp.value === '+7') inp.value = '';
  });
  inp.addEventListener('keydown', (ev) => {
    if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
    if (ev.key.length !== 1 && ev.key !== 'Backspace' && ev.key !== 'Delete') return;
    ev.preventDefault();
    const d = nationalDigits(inp.value);
    const selStart = digitIndexAt(inp.selectionStart);
    const selEnd = digitIndexAt(inp.selectionEnd);
    const hasSelection = inp.selectionEnd > inp.selectionStart;
    if (ev.key.length === 1) {
      if (!/\d/.test(ev.key)) return;
      const next = d.slice(0, selStart) + ev.key + d.slice(hasSelection ? selEnd : selStart);
      if (next.length <= 10) setValue(next, selStart + 1);
      else if (!hasSelection && selStart < d.length) setValue(d.slice(0, selStart) + ev.key + d.slice(selStart + 1), selStart + 1);
    } else if (ev.key === 'Backspace') {
      if (hasSelection) setValue(d.slice(0, selStart) + d.slice(selEnd), selStart);
      else if (selStart > 0) setValue(d.slice(0, selStart - 1) + d.slice(selStart), selStart - 1);
      else if (!d.length) inp.value = '+7 (';
    } else {
      if (hasSelection) setValue(d.slice(0, selStart) + d.slice(selEnd), selStart);
      else if (selStart < d.length) setValue(d.slice(0, selStart) + d.slice(selStart + 1), selStart);
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

// --- real lead delivery: POST to send-lead.php (email + Telegram + VK) ---
const sendLead = (form, cms, onSuccess) => {
  const btn = form.querySelector('button[type="submit"]');
  const prevText = btn ? btn.textContent : '';
  if (btn) { btn.disabled = true; btn.textContent = 'Отправляем…'; }
  const data = new FormData(form);
  if (cms) data.append('cms', cms);
  data.append('page', location.pathname + location.hash);
  fetch('send-lead.php', { method: 'POST', body: data })
    .then((r) => r.json())
    .then((res) => {
      if (!res.ok) throw new Error(res.error || 'delivery');
      if (typeof ym === 'function') ym(112155075, 'reachGoal', 'lead_form');
      if (onSuccess) onSuccess();
      if (btn) {
        btn.textContent = 'Заявка отправлена ✓';
        btn.style.background = 'linear-gradient(135deg,#10b981,#34d399)';
      }
    })
    .catch(() => {
      if (btn) { btn.disabled = false; btn.textContent = prevText; }
      showError(form, 'Не удалось отправить. Позвоните нам или напишите в мессенджер.');
    });
};

// form
const form = document.getElementById('lead-form');
if (form) {
  form.addEventListener('submit', (ev) => {
    ev.preventDefault();
    if (!validateLeadForm(form)) return;
    sendLead(form, '');
  });
}

// cookie consent
const cookieBar = document.getElementById('cookie-bar');
if (cookieBar) {
  const COOKIE_KEY = 'ip_cookie_ok';
  let accepted = false;
  try { accepted = localStorage.getItem(COOKIE_KEY) === '1'; } catch (e) { accepted = false; }
  if (!accepted) {
    setTimeout(() => {
      cookieBar.classList.add('show');
      cookieBar.setAttribute('aria-hidden', 'false');
    }, 1500);
    const btn = document.getElementById('cookie-accept');
    if (btn) btn.addEventListener('click', () => {
      try { localStorage.setItem(COOKIE_KEY, '1'); } catch (e) {}
      cookieBar.classList.remove('show');
      cookieBar.setAttribute('aria-hidden', 'true');
    });
  }
}
