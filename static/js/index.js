/**
 * index.js — Home page logic
 * Dashboard, student/teacher/class/subject/award modals, timetable, auth.
 */

/* ── State ────────────────────────────────────────────────────────────── */
let teacherMode = 'login';
let studentMode = 'login';
let studentPage = 1;
let teacherPage = 1;
let studentSearch = '';
let teacherSearch = '';
let gradeChart = null;
let attendanceChart = null;

/* ── Dashboard ────────────────────────────────────────────────────────── */
async function openDashboardSection() {
    document.getElementById('dashboardSection').style.display = 'block';
    document.querySelector('.module-grid').style.display = 'none';

    try {
        const d = await API.get('/dashboard/stats');
        document.getElementById('statStudents').textContent  = d.totalStudents.toLocaleString();
        document.getElementById('statTeachers').textContent  = d.totalTeachers;
        document.getElementById('statClasses').textContent   = d.totalClasses;
        document.getElementById('statAttendance').textContent = d.attendanceRate + '%';
        document.getElementById('statSubjects').textContent  = d.totalSubjects;
        document.getElementById('statPassing').textContent   = d.passingRate + '%';
        document.getElementById('statGrade').textContent     = d.averageGrade;
        document.getElementById('statAwards').textContent    = d.totalAwards;
        document.getElementById('dashSubtitle').textContent  = `Live school-wide statistics`;
    } catch (e) {
        toast('Failed to load dashboard stats', 'error');
    }
}

function closeDashboard() {
    document.getElementById('dashboardSection').style.display = 'none';
    document.querySelector('.module-grid').style.display = 'grid';
}

/* ── Students ─────────────────────────────────────────────────────────── */
async function openStudentList() {
    Modal.open('studentListModal');
    await loadStudents(1, '');
}

function onStudentSearch(val) {
    studentSearch = val;
    studentPage = 1;
    loadStudents(1, val);
}

async function loadStudents(page, search) {
    studentPage = page;
    const container = document.getElementById('studentTableContainer');
    const pagEl     = document.getElementById('studentPagination');
    showLoader(container);

    try {
        const d = await API.get(`/api/students?page=${page}&per_page=20&search=${encodeURIComponent(search || studentSearch)}`);
        let html = `<div class="table-wrap"><table class="data-table">
            <thead><tr><th>Roll No.</th><th>Name</th><th>Class</th><th>Overall Marks</th><th>Grade</th><th>Attendance</th></tr></thead><tbody>`;
        d.students.forEach(s => {
            html += `<tr>
                <td style="font-family:'Space Grotesk',sans-serif;color:var(--text-3);">${s.roll}</td>
                <td><strong>${s.name}</strong><br><span style="font-size:0.75rem;color:var(--text-3);">${s.email}</span></td>
                <td>${s.class}</td>
                <td>${s.overall_marks}%</td>
                <td>${gradeBadge(s.overall_grade)}</td>
                <td>${s.attendance_pct}%</td>
            </tr>`;
        });
        html += '</tbody></table></div>';
        container.innerHTML = html;
        buildPagination(pagEl, page, d.total_pages, 'loadStudents');
    } catch (e) {
        container.innerHTML = `<div class="alert alert-error"><i class="fas fa-exclamation-circle"></i>Failed to load students.</div>`;
    }
}

/* ── Teachers ─────────────────────────────────────────────────────────── */
async function openTeacherList() {
    Modal.open('teacherListModal');
    await loadTeachers(1, '');
}

function onTeacherSearch(val) {
    teacherSearch = val;
    teacherPage = 1;
    loadTeachers(1, val);
}

async function loadTeachers(page, search) {
    teacherPage = page;
    const container = document.getElementById('teacherTableContainer');
    const pagEl     = document.getElementById('teacherPagination');
    showLoader(container);

    try {
        const d = await API.get(`/api/teachers?page=${page}&per_page=20&search=${encodeURIComponent(search || teacherSearch)}`);
        let html = `<div class="table-wrap"><table class="data-table">
            <thead><tr><th>Teacher ID</th><th>Name</th><th>Subject</th><th>Email</th></tr></thead><tbody>`;
        d.teachers.forEach(t => {
            html += `<tr>
                <td style="font-family:'Space Grotesk',sans-serif;color:var(--text-3);">${t.teacher_id}</td>
                <td><strong>${t.name}</strong></td>
                <td><span class="badge badge-good">${t.subject}</span></td>
                <td style="color:var(--text-3);font-size:0.82rem;">${t.email}</td>
            </tr>`;
        });
        html += '</tbody></table></div>';
        container.innerHTML = html;
        buildPagination(pagEl, page, d.total_pages, 'loadTeachers');
    } catch (e) {
        container.innerHTML = `<div class="alert alert-error"><i class="fas fa-exclamation-circle"></i>Failed to load teachers.</div>`;
    }
}

/* ── Classes ──────────────────────────────────────────────────────────── */
async function openClassList() {
    Modal.open('classListModal');
    const container = document.getElementById('classTableContainer');
    showLoader(container);

    try {
        const d = await API.get('/api/classes');
        let html = `<div class="table-wrap"><table class="data-table">
            <thead><tr><th>Class</th><th>Class Teacher</th><th>Students</th><th>Room</th></tr></thead><tbody>`;
        d.classes.forEach(c => {
            html += `<tr>
                <td><strong>${c.name}</strong></td>
                <td>${c.class_teacher}</td>
                <td><span class="badge badge-good">${c.students_count}</span></td>
                <td style="color:var(--teal);">${c.room_number}</td>
            </tr>`;
        });
        html += '</tbody></table></div>';
        container.innerHTML = html;
    } catch (e) {
        container.innerHTML = `<div class="alert alert-error"><i class="fas fa-exclamation-circle"></i>Failed to load classes.</div>`;
    }
}

/* ── Subjects ─────────────────────────────────────────────────────────── */
async function openSubjects() {
    Modal.open('subjectsModal');
    const container = document.getElementById('subjectsContainer');
    showLoader(container);

    try {
        const d = await API.get('/api/subjects');
        let html = '<div class="subjects-grid">';
        d.subjects.forEach(s => {
            html += `<div class="subject-card" onclick="openResources('${s.name}', ${JSON.stringify(s).replace(/'/g, "&#39;")})">
                <h3><i class="fas fa-book" style="color:var(--indigo-2);margin-right:8px;"></i>${s.name}</h3>
                <p><i class="fas fa-user" style="margin-right:6px;color:var(--text-3);"></i>${s.teacher}</p>
                <p><i class="fas fa-users" style="margin-right:6px;color:var(--text-3);"></i>${s.students} students</p>
            </div>`;
        });
        html += '</div>';
        container.innerHTML = html;
    } catch (e) {
        container.innerHTML = `<div class="alert alert-error"><i class="fas fa-exclamation-circle"></i>Failed to load subjects.</div>`;
    }
}

function openResources(name, subject) {
    document.getElementById('resourcesTitle').innerHTML = `<i class="fas fa-book"></i> ${name}`;
    let html = '<p class="section-title">📚 Recommended Books</p>';
    (subject.books || []).forEach(b => {
        html += `<div class="resource-item"><i class="fas fa-book-open"></i><span>${b}</span></div>`;
    });
    html += '<p class="section-title" style="margin-top:20px;">🌐 Websites</p>';
    (subject.websites || []).forEach(w => {
        html += `<div class="resource-item"><i class="fas fa-globe"></i><a href="${w}" target="_blank" rel="noopener">${w}</a></div>`;
    });
    document.getElementById('resourcesContainer').innerHTML = html;
    Modal.open('resourcesModal');
}

/* ── Awards ───────────────────────────────────────────────────────────── */
async function openAwards() {
    Modal.open('awardsModal');
    const container = document.getElementById('awardsContainer');
    showLoader(container);

    try {
        const d = await API.get('/api/awards');
        const rankBadge = r => {
            if (r.includes('Gold'))   return 'badge-gold';
            if (r.includes('Silver')) return 'badge-silver';
            if (r === 'Winner' || r === 'Champion') return 'badge-present';
            return 'badge-good';
        };
        let html = '<div class="awards-grid">';
        d.awards.forEach(a => {
            html += `<div class="award-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
                    <div class="trophy">🏆</div>
                    <span class="badge ${rankBadge(a.rank)}">${a.rank}</span>
                </div>
                <h3>${a.name}</h3>
                <p><i class="fas fa-user" style="margin-right:6px;color:var(--text-3);"></i>${a.winner}</p>
                <p><i class="fas fa-door-open" style="margin-right:6px;color:var(--text-3);"></i>${a.class}</p>
                <p style="margin-top:8px;font-size:0.75rem;color:var(--indigo-2);">Year ${a.year}</p>
            </div>`;
        });
        html += '</div>';
        container.innerHTML = html;
    } catch (e) {
        container.innerHTML = `<div class="alert alert-error"><i class="fas fa-exclamation-circle"></i>Failed to load awards.</div>`;
    }
}

/* ── Passing Rate ─────────────────────────────────────────────────────── */
async function openPassingRate() {
    Modal.open('passingModal');
    const container = document.getElementById('passingContainer');
    showLoader(container);

    try {
        const d = await API.get('/dashboard/grade-distribution');
        const p = d.passing;
        let html = `<div class="stat-grid" style="margin-bottom:24px;">
            <div class="stat-card green"><div class="icon"><i class="fas fa-check-circle"></i></div><div class="stat-value">${p.rate}%</div><div class="stat-label">Passing Rate</div></div>
            <div class="stat-card teal"><div class="icon"><i class="fas fa-users"></i></div><div class="stat-value">${p.passed.toLocaleString()}</div><div class="stat-label">Passed</div></div>
            <div class="stat-card rose"><div class="icon"><i class="fas fa-times-circle"></i></div><div class="stat-value">${p.failed.toLocaleString()}</div><div class="stat-label">Failed</div></div>
        </div>
        <p class="section-title">Grade Breakdown</p>
        <div class="table-wrap"><table class="data-table"><thead><tr><th>Grade</th><th>Students</th><th>Percentage</th></tr></thead><tbody>`;
        Object.entries(d.distribution).forEach(([g, c]) => {
            html += `<tr><td>${gradeBadge(g)}</td><td>${c.toLocaleString()}</td><td>${((c/p.total)*100).toFixed(1)}%</td></tr>`;
        });
        html += '</tbody></table></div>';
        container.innerHTML = html;
    } catch (e) {
        container.innerHTML = `<div class="alert alert-error"><i class="fas fa-exclamation-circle"></i>Failed to load data.</div>`;
    }
}

/* ── Grade Distribution Chart ─────────────────────────────────────────── */
async function openGradeDistribution() {
    Modal.open('gradeModal');
    const container = document.getElementById('gradeContainer');
    container.innerHTML = `<div class="chart-card"><canvas id="gradeChartCanvas" height="100"></canvas></div>`;

    try {
        const d = await API.get('/dashboard/grade-distribution');
        const dist  = d.distribution;
        const labels = ['A+', 'A', 'B+', 'B', 'C', 'D', 'F'];
        const values = labels.map(l => dist[l] || 0);
        const colors = ['#22c55e','#4ade80','#a3e635','#fbbf24','#fb923c','#f87171','#f43f5e'];

        if (gradeChart) gradeChart.destroy();
        gradeChart = new Chart(document.getElementById('gradeChartCanvas'), {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label: 'Number of Students',
                    data: values,
                    backgroundColor: colors.map(c => c + '33'),
                    borderColor: colors,
                    borderWidth: 2,
                    borderRadius: 6,
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false }, title: { display: true, text: 'Student Grade Distribution 2024', color: '#f1f5f9', font: { size: 14, weight: '700' } } },
                scales: {
                    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b' } },
                    x: { grid: { display: false }, ticks: { color: '#64748b' } }
                }
            }
        });
    } catch (e) {
        container.innerHTML = `<div class="alert alert-error"><i class="fas fa-exclamation-circle"></i>Failed to load chart.</div>`;
    }
}

/* ── Attendance Analytics ─────────────────────────────────────────────── */
async function openAttendanceAnalytics() {
    Modal.open('attendanceModal');
    if (attendanceChart) { attendanceChart.destroy(); attendanceChart = null; }

    try {
        const d = await API.get('/dashboard/attendance-analytics');
        attendanceChart = new Chart(document.getElementById('attendanceChart'), {
            type: 'line',
            data: {
                labels: d.labels,
                datasets: [{
                    label: 'Monthly Attendance (%)',
                    data: d.rates,
                    borderColor: '#4f6ef7',
                    backgroundColor: 'rgba(79,110,247,0.08)',
                    borderWidth: 2.5,
                    pointBackgroundColor: '#4f6ef7',
                    pointBorderColor: '#0a0e1a',
                    pointRadius: 5,
                    tension: 0.35,
                    fill: true,
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'top', labels: { color: '#94a3b8' } },
                    title: { display: true, text: 'Monthly Attendance Overview 2024', color: '#f1f5f9', font: { size: 14, weight: '700' } }
                },
                scales: {
                    y: { min: 70, max: 100, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b', callback: v => v + '%' } },
                    x: { grid: { display: false }, ticks: { color: '#64748b' } }
                }
            }
        });

        const months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
        const statuses = [92,88,95,91,93,89,94,96,92,90,93,95];
        let html = `<p class="section-title" style="margin-top:24px;">Monthly Summary</p>
        <div class="table-wrap"><table class="data-table">
            <thead><tr><th>Month</th><th>Rate</th><th>Status</th><th>Trend</th></tr></thead><tbody>`;
        months.forEach((m, i) => {
            const rate = d.rates[i];
            const status = rate >= 92 ? 'Excellent' : 'Good';
            const badge  = rate >= 92 ? 'badge-present' : 'badge-good';
            const trend  = i > 0 ? (rate > d.rates[i-1] ? '⬆️ +' + (rate - d.rates[i-1]).toFixed(1) + '%' : '⬇️ ' + (rate - d.rates[i-1]).toFixed(1) + '%') : '—';
            html += `<tr><td>${m}</td><td>${rate}%</td><td><span class="badge ${badge}">${status}</span></td><td style="font-size:0.8rem;">${trend}</td></tr>`;
        });
        html += '</tbody></table></div>';
        document.getElementById('attendanceTable').innerHTML = html;
    } catch (e) {
        toast('Failed to load attendance data', 'error');
    }
}

/* ── Timetable ────────────────────────────────────────────────────────── */
async function openTimetable() {
    Modal.open('timetableModal');
    const btnsEl = document.getElementById('timetableClassBtns');
    if (btnsEl.children.length === 0) {
        try {
            const d = await API.get('/timetable/classes');
            btnsEl.innerHTML = d.classes.map(c =>
                `<button class="class-btn" onclick="loadTimetable('${c}')">${c}</button>`
            ).join('');
            if (d.classes.length) loadTimetable(d.classes.indexOf('Grade 10A') >= 0 ? 'Grade 10A' : d.classes[0]);
        } catch (e) {
            toast('Failed to load class list', 'error');
        }
    }
}

async function loadTimetable(className) {
    document.querySelectorAll('#timetableClassBtns .class-btn').forEach(b => {
        b.classList.toggle('active', b.textContent === className);
    });

    const grid = document.getElementById('timetableGrid');
    showLoader(grid);

    try {
        const d = await API.get(`/timetable/class/${encodeURIComponent(className)}`);
        const days = ['Monday','Tuesday','Wednesday','Thursday','Friday'];
        let html = '<div class="timetable-grid">';
        days.forEach(day => {
            const slots = (d.schedule[day] || []);
            html += `<div class="tt-day-col"><div class="tt-day-head">${day}</div>`;
            slots.forEach(slot => {
                const isLunch = slot.subject === 'Lunch Break';
                html += `<div class="tt-slot ${isLunch ? 'lunch' : ''}">
                    <div class="tt-subject">${slot.subject}</div>
                    <div class="tt-teacher">${slot.teacher}</div>
                    <div class="tt-time"><i class="fas fa-clock" style="margin-right:3px;"></i>${slot.time}</div>
                    <div class="tt-room"><i class="fas fa-map-marker-alt" style="margin-right:3px;"></i>${slot.room}</div>
                </div>`;
            });
            html += '</div>';
        });
        html += '</div>';
        grid.innerHTML = html;
    } catch (e) {
        grid.innerHTML = `<div class="alert alert-error"><i class="fas fa-exclamation-circle"></i>Failed to load timetable.</div>`;
    }
}

/* ── Teacher Auth ─────────────────────────────────────────────────────── */
function toggleTeacherMode() {
    teacherMode = teacherMode === 'login' ? 'register' : 'login';
    const isReg = teacherMode === 'register';
    document.getElementById('teacherModalTitle').innerHTML = `<i class="fas fa-chalkboard-user"></i> ${isReg ? 'Teacher Registration' : 'Teacher Login'}`;
    document.getElementById('teacherActionBtn').textContent = isReg ? 'Register →' : 'Login →';
    document.getElementById('teacherSwitchText').textContent = isReg ? 'Already have an account? ' : 'New user? ';
    document.querySelector('#teacherLoginModal .login-switch a').textContent = isReg ? 'Login' : 'Create Account';
    document.getElementById('teacherMsg').innerHTML = '';
}

async function handleTeacherAuth() {
    const body = {
        name:     document.getElementById('tName').value.trim(),
        email:    document.getElementById('tEmail').value.trim(),
        password: document.getElementById('tPass').value,
        subject:  document.getElementById('tSubject').value,
    };
    const msgEl = document.getElementById('teacherMsg');
    const url   = teacherMode === 'login' ? '/auth/teacher/login' : '/auth/teacher/register';
    const { ok, data } = await authPost(url, body, msgEl);

    if (ok && teacherMode === 'register') {
        msgEl.innerHTML = `<div class="alert alert-success"><i class="fas fa-check-circle"></i>${data.message}</div>`;
        setTimeout(() => toggleTeacherMode(), 1600);
    }
}

/* ── Student Auth ─────────────────────────────────────────────────────── */
function toggleStudentMode() {
    studentMode = studentMode === 'login' ? 'register' : 'login';
    const isReg = studentMode === 'register';
    document.getElementById('studentModalTitle').innerHTML = `<i class="fas fa-user-graduate"></i> ${isReg ? 'Student Registration' : 'Student Login'}`;
    document.getElementById('studentActionBtn').textContent = isReg ? 'Register →' : 'Login →';
    document.getElementById('studentSwitchText').textContent = isReg ? 'Already have an account? ' : 'New user? ';
    document.querySelector('#studentLoginModal .login-switch a').textContent = isReg ? 'Login' : 'Create Account';
    document.getElementById('studentMsg').innerHTML = '';
}

async function handleStudentAuth() {
    const body = {
        name:     document.getElementById('sName').value.trim(),
        email:    document.getElementById('sEmail').value.trim(),
        password: document.getElementById('sPass').value,
        class:    document.getElementById('sClass').value,
    };
    const msgEl = document.getElementById('studentMsg');
    const url   = studentMode === 'login' ? '/auth/student/login' : '/auth/student/register';
    const { ok, data } = await authPost(url, body, msgEl);

    if (ok && studentMode === 'register') {
        msgEl.innerHTML = `<div class="alert alert-success"><i class="fas fa-check-circle"></i>${data.message}</div>`;
        setTimeout(() => toggleStudentMode(), 1600);
    }
}

/* ── Expose globals for pagination callbacks ──────────────────────────── */
window.loadStudents   = loadStudents;
window.loadTeachers   = loadTeachers;
window.openResources  = openResources;
window.loadTimetable  = loadTimetable;
