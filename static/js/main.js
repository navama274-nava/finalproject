/**
 * School Management System — Main JS
 * Shared utilities: API calls, modal management, pagination, toast.
 */

/* ── API helpers ──────────────────────────────────────────────────────── */
const API = {
    async get(url) {
        const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
        if (!res.ok) throw new Error(`API ${url} failed: ${res.status}`);
        return res.json();
    },
    async post(url, body) {
        const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            body: JSON.stringify(body)
        });
        return { ok: res.ok, status: res.status, data: await res.json() };
    }
};

/* ── Toast notifications ──────────────────────────────────────────────── */
function toast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9999;display:flex;flex-direction:column;gap:8px;';
        document.body.appendChild(container);
    }

    const colors = { info: '#4f6ef7', success: '#22c55e', error: '#f43f5e', warning: '#f59e0b' };
    const icons  = { info: 'circle-info', success: 'check-circle', error: 'triangle-exclamation', warning: 'exclamation-circle' };

    const el = document.createElement('div');
    el.style.cssText = `background:${colors[type]};color:white;padding:12px 18px;border-radius:10px;
        font-size:0.875rem;font-weight:500;display:flex;align-items:center;gap:10px;
        box-shadow:0 8px 24px rgba(0,0,0,0.4);animation:slideInRight 0.3s ease;
        max-width:320px;font-family:'DM Sans',sans-serif;`;
    el.innerHTML = `<i class="fas fa-${icons[type]}"></i><span>${message}</span>`;
    container.appendChild(el);
    setTimeout(() => { el.style.opacity = '0'; el.style.transform = 'translateX(20px)'; el.style.transition = '0.3s'; setTimeout(() => el.remove(), 300); }, 3500);
}

/* ── Modal system ─────────────────────────────────────────────────────── */
const Modal = {
    open(id) {
        document.getElementById(id)?.classList.add('active');
        document.body.style.overflow = 'hidden';
    },
    close(id) {
        document.getElementById(id)?.classList.remove('active');
        document.body.style.overflow = '';
    },
    closeAll() {
        document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('active'));
        document.body.style.overflow = '';
    }
};

// Close modal on backdrop click
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) Modal.closeAll();
});

// Close on Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') Modal.closeAll();
});

/* ── Loader helpers ───────────────────────────────────────────────────── */
function showLoader(container) {
    container.innerHTML = `<div class="loader"><div class="spinner"></div><span>Loading data…</span></div>`;
}

/* ── Pagination builder ───────────────────────────────────────────────── */
function buildPagination(container, current, total, onPageClick) {
    if (total <= 1) { container.innerHTML = ''; return; }
    let html = '';
    if (current > 1) html += `<button class="page-btn" onclick="${onPageClick}(${current - 1})"><i class="fas fa-chevron-left"></i></button>`;
    const start = Math.max(1, current - 2);
    const end   = Math.min(total, current + 2);
    if (start > 1) html += `<button class="page-btn" onclick="${onPageClick}(1)">1</button>${start > 2 ? '<span style="color:var(--text-3);padding:0 4px;">…</span>' : ''}`;
    for (let i = start; i <= end; i++) html += `<button class="page-btn ${i === current ? 'active' : ''}" onclick="${onPageClick}(${i})">${i}</button>`;
    if (end < total) html += `${end < total - 1 ? '<span style="color:var(--text-3);padding:0 4px;">…</span>' : ''}<button class="page-btn" onclick="${onPageClick}(${total})">${total}</button>`;
    if (current < total) html += `<button class="page-btn" onclick="${onPageClick}(${current + 1})"><i class="fas fa-chevron-right"></i></button>`;
    container.innerHTML = html;
}

/* ── Badge helper ─────────────────────────────────────────────────────── */
function gradeBadge(grade) {
    const map = { 'A+': 'badge-present', 'A': 'badge-good', 'B+': 'badge-good',
                  'B': 'badge-good', 'C': 'badge-late', 'D': 'badge-late', 'F': 'badge-absent' };
    return `<span class="badge ${map[grade] || 'badge-good'}">${grade}</span>`;
}

function statusBadge(status) {
    const map = { present: 'badge-present', absent: 'badge-absent', late: 'badge-late' };
    return `<span class="badge ${map[status] || 'badge-good'}">${status}</span>`;
}

/* ── Auth helpers (used by login pages) ───────────────────────────────── */
async function authPost(url, body, msgEl) {
    msgEl.innerHTML = '';
    try {
        const { ok, data } = await API.post(url, body);
        if (ok) {
            if (data.redirect) { window.location.href = data.redirect; }
            return { ok: true, data };
        } else {
            msgEl.innerHTML = `<div class="alert alert-error"><i class="fas fa-exclamation-circle"></i>${data.message || 'An error occurred'}</div>`;
            return { ok: false, data };
        }
    } catch (err) {
        msgEl.innerHTML = `<div class="alert alert-error"><i class="fas fa-exclamation-circle"></i>Network error. Please try again.</div>`;
        return { ok: false };
    }
}

/* ── Chart defaults ───────────────────────────────────────────────────── */
Chart.defaults.color             = '#64748b';
Chart.defaults.font.family       = "'DM Sans', sans-serif";
Chart.defaults.borderColor       = 'rgba(255,255,255,0.06)';
Chart.defaults.plugins.legend.labels.boxWidth = 12;
