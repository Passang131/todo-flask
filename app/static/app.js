// Shared helpers for pages (optional enhancement)
window.apiBase = '';
window.getToken = () => localStorage.getItem('token');
window.setToken = (t) => localStorage.setItem('token', t);
window.clearToken = () => localStorage.removeItem('token');

// Toggle header buttons based on auth state
window.addEventListener('DOMContentLoaded', () => {
  const hasToken = !!getToken();
  const el = (id) => document.getElementById(id);
  const login = el('nav-login');
  const register = el('nav-register');
  const app = el('nav-app');
  const logout = el('nav-logout');
  if (login && register && app && logout) {
    login.style.display = hasToken ? 'none' : '';
    register.style.display = hasToken ? 'none' : '';
    app.style.display = hasToken ? '' : 'none';
    logout.style.display = hasToken ? '' : 'none';
    logout.addEventListener('click', (e) => {
      e.preventDefault();
      clearToken();
      location.href = '/';
    });
  }
});


