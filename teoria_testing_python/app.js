const navBtn = document.getElementById('navToggle');
if (navBtn) {
  navBtn.addEventListener('click', () => {
    document.querySelector('.nav-links')?.classList.toggle('open');
  });
}

function copyCode(btn) {
  const code = btn.closest('.code-block').querySelector('pre code');
  if (!code) return;
  navigator.clipboard.writeText(code.innerText).then(() => {
    const old = btn.textContent;
    btn.textContent = 'Copiado';
    setTimeout(() => (btn.textContent = old), 1300);
  });
}

window.copyCode = copyCode;
