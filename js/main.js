(function () {
  const cfg = window.SITE_CONFIG || {};
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  document.querySelectorAll('[data-phone-href]').forEach((el) => {
    if (cfg.phoneTel) el.setAttribute('href', cfg.phoneTel);
  });
  document.querySelectorAll('[data-sms-href]').forEach((el) => {
    if (cfg.smsHref) el.setAttribute('href', cfg.smsHref);
  });
  document.querySelectorAll('[data-email-href]').forEach((el) => {
    if (cfg.email) el.setAttribute('href', 'mailto:' + cfg.email);
  });
  document.querySelectorAll('[data-phone-label]').forEach((el) => {
    if (cfg.phone) el.textContent = cfg.phone;
  });
  document.querySelectorAll('[data-email-label]').forEach((el) => {
    if (cfg.email) el.textContent = cfg.email;
  });

  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    const closeMenu = () => {
      links.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open menu');
      document.body.classList.remove('nav-open');
    };
    toggle.addEventListener('click', () => {
      const open = links.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.body.classList.toggle('nav-open', open);
    });
    links.querySelectorAll('a').forEach((a) => a.addEventListener('click', closeMenu));
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeMenu();
    });
  }

  const form = document.getElementById('booking-form');
  if (form) {
    if (cfg.formEndpoint) form.setAttribute('action', cfg.formEndpoint);
    const subject = form.querySelector('input[name="_subject"]');
    const next = form.querySelector('input[name="_next"]');
    const auto = form.querySelector('input[name="_autoresponse"]');
    if (subject && cfg.formSubject) subject.value = cfg.formSubject;
    if (next && cfg.formNext) next.value = cfg.formNext;
    if (auto && cfg.formAutoresponse) auto.value = cfg.formAutoresponse;

    const email = form.querySelector('#email');
    const replyto = form.querySelector('#form-replyto');
    const syncReplyto = () => {
      if (email && replyto) replyto.value = email.value.trim();
    };
    if (email) email.addEventListener('input', syncReplyto);

    const typeField = form.querySelector('#document_type');
    if (typeField) {
      const params = new URLSearchParams(window.location.search);
      const typeMap = {
        loan: 'Loan / real estate closing',
        hospital: 'Hospital / home visit',
        i9: 'Workplace / I-9',
        general: 'Affidavit / general notary',
        estate: 'Estate planning (will, trust, directive)',
        poa: 'Power of attorney'
      };
      const preset = typeMap[params.get('type') || ''];
      if (preset) typeField.value = preset;
    }

    form.addEventListener('submit', (e) => {
      syncReplyto();
      if (!form.checkValidity()) {
        e.preventDefault();
        form.reportValidity();
        return;
      }
      const btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.disabled = true;
        btn.textContent = 'Sending…';
        window.setTimeout(() => {
          btn.disabled = false;
          btn.textContent = 'Send Appointment Request';
        }, 8000);
      }
    });
  }
})();
