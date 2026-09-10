/* =========================================================
   app.js — LabelSetu frontend
   Connects to the Express backend (Render deployment).
   All mock/localStorage logic replaced with real API calls.
   Function names preserved so existing HTML pages work.

   API_BASE resolution order:
     1. window.LABELSETU_API_BASE  (set via inline <script> per page)
     2. RENDER_BACKEND_URL constant below  (updated after Render deploy)
   ========================================================= */

// ✅ Updated to the Render deployment URL after free-cloud deploy.
// Change this value once you have your Render service URL.
const RENDER_BACKEND_URL = 'https://labelsetu-backend.onrender.com/api';

const API_BASE = (typeof window !== 'undefined' && window.LABELSETU_API_BASE)
  ? window.LABELSETU_API_BASE
  : RENDER_BACKEND_URL;

/* =========================================================
   TOKEN HELPERS
   ========================================================= */

function getToken() {
  return localStorage.getItem('labelsetu_token');
}

function saveToken(token) {
  localStorage.setItem('labelsetu_token', token);
}

function clearToken() {
  localStorage.removeItem('labelsetu_token');
}

/* =========================================================
   REUSABLE FETCH HELPERS
   ========================================================= */

async function apiFetch(path, options = {}) {
  const res = await fetch(API_BASE + path, options);
  const json = await res.json();
  return { status: res.status, json };
}

async function apiGet(path) {
  const token = getToken();
  return apiFetch(path, {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${token}` },
  });
}

async function apiPost(path, body) {
  return apiFetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
}

/* =========================================================
   SIGNUP
   Replaces: mockSignup(name, email, password)
   ========================================================= */

async function mockSignup(name, email, password) {
  try {
    const { json } = await apiPost('/auth/register', { name, email, password });
    if (!json.success) {
      return { ok: false, error: json.error?.message || 'Registration failed.' };
    }
    saveToken(json.data.token);
    return { ok: true };
  } catch {
    return { ok: false, error: 'Could not reach the server. Please try again.' };
  }
}

/* =========================================================
   LOGIN
   Replaces: mockLogin(email, password)
   ========================================================= */

async function mockLogin(email, password) {
  try {
    const { json } = await apiPost('/auth/login', { email, password });
    if (!json.success) {
      return { ok: false, error: json.error?.message || 'Login failed.' };
    }
    saveToken(json.data.token);
    return { ok: true };
  } catch {
    return { ok: false, error: 'Could not reach the server. Please try again.' };
  }
}

/* =========================================================
   CURRENT USER
   Replaces: getCurrentUser()
   ========================================================= */

let _cachedUser = null;

function getCurrentUser() {
  return _cachedUser;
}

/* =========================================================
   LOGOUT
   ========================================================= */

function logout() {
  clearToken();
  _cachedUser = null;
  window.location.href = 'login.html';
}

/* =========================================================
   AUTH PROTECTION
   Replaces: requireAuth()
   ========================================================= */

async function requireAuth() {
  const token = getToken();
  if (!token) {
    window.location.href = 'login.html';
    return;
  }
  try {
    const { json } = await apiGet('/auth/me');
    if (!json.success) {
      clearToken();
      window.location.href = 'login.html';
      return;
    }
    _cachedUser = json.data.user;
  } catch {
    console.warn('[LabelSetu] Could not verify session with backend.');
  }
}

/* =========================================================
   UPLOAD AND VERIFY
   Replaces: mockRunCheck()
   Call this with the real File object, NOT a data URL.
   ========================================================= */

async function runCheck(file, category) {
  const token = getToken();
  const formData = new FormData();
  formData.append('image', file);
  formData.append('category', category);

  const res = await fetch(`${API_BASE}/verify/upload`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    // DO NOT set Content-Type — browser sets multipart boundary automatically
    body: formData,
  });

  const json = await res.json();
  if (!json.success) {
    throw new Error(json.error?.message || 'Upload failed.');
  }
  return json.data;
}

/* =========================================================
   GET ONE SCAN
   Replaces: getScanById(id)
   ========================================================= */

async function getScanById(id) {
  const { json } = await apiGet(`/dashboard/scan/${id}`);
  if (!json.success) return null;
  return json.data.scan;
}

/* =========================================================
   GET ALL SCANS
   Replaces: getAllScans()
   ========================================================= */

async function getAllScans() {
  const { json } = await apiGet('/dashboard/history');
  if (!json.success) return [];
  return json.data.scans;
}

/* =========================================================
   NAVIGATION HIGHLIGHT
   ========================================================= */

function highlightActiveNav() {
  const page = window.location.pathname.split('/').pop();
  document.querySelectorAll('.nav-links a').forEach(a => {
    if (a.getAttribute('href') === page) a.classList.add('active');
  });
}

/* =========================================================
   PAGE INITIALIZATION
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {
  highlightActiveNav();

  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', logout);
  }
});