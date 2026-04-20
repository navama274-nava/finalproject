# 🎓 School Management System

A production-ready **Flask + MongoDB** school management platform with modular architecture, session-based auth, and Chart.js analytics.

---

## 📁 Project Structure

```
school_management/
├── run.py                        # Entry point
├── .env                          # Environment config
├── requirements.txt
│
├── app/
│   ├── __init__.py               # App factory (create_app)
│   │
│   ├── models/
│   │   ├── user.py               # Flask-Login User wrapper
│   │   ├── student.py            # Student CRUD + analytics
│   │   ├── teacher.py            # Teacher CRUD
│   │   └── school.py             # Subject, Award, Class, Timetable, Attendance models
│   │
│   ├── routes/
│   │   ├── auth.py               # /auth/* — login, register, logout
│   │   ├── dashboard.py          # /dashboard/* — school-wide stats
│   │   ├── teacher.py            # /teacher/* — teacher portal
│   │   ├── student.py            # /student/* — student portal
│   │   ├── timetable.py          # /timetable/* — schedule data
│   │   └── api.py                # /api/* — public JSON endpoints
│   │
│   └── utils/
│       └── helpers.py            # serialize_doc, paginate, marks_to_grade, api_success/error
│
├── static/
│   ├── css/main.css              # Full dark-theme stylesheet (CSS variables)
│   └── js/
│       ├── main.js               # Shared: API, Modal, toast, buildPagination, Chart defaults
│       └── index.js              # Home page logic: dashboard, auth modals, timetable
│
└── templates/
    ├── index.html                # Home page (modules + all dashboard modals)
    ├── shared/base.html          # Base layout with navbar
    ├── auth/unauthorized.html    # 403 page
    ├── teacher/dashboard.html    # Teacher portal
    └── student/dashboard.html    # Student portal
```

---

## ⚡ Quick Start

### 1. Prerequisites
- **Python 3.10+**
- **MongoDB Community Server** running on `localhost:27017`  
  Download: https://www.mongodb.com/try/download/community

### 2. Install dependencies
```bash
cd school_management
pip install -r requirements.txt
```

### 3. Configure environment
Edit `.env` if your MongoDB URI is different:
```
MONGO_URI=mongodb://localhost:27017/school_management
SECRET_KEY=change-this-in-production
```

### 4. Run the server
```bash
python run.py
```

Open: **http://localhost:5000**

---

---

## 🗄️ MongoDB Collections

| Collection   | Description                                        |
|--------------|----------------------------------------------------|
| `students`   | 1050 docs with marks, attendance, grade fields     |
| `teachers`   | 100 docs with subject, teacher_id                  |
| `classes`    | 24 docs with class_teacher, room_number            |
| `subjects`   | 15 docs with books and website resources           |
| `awards`     | 25 docs with winner, rank, year                    |
| `timetables` | 24 docs (one per class) with full weekly schedule  |
| `attendance` | Per-student per-date attendance records            |

---

## 🌐 API Endpoints

### Public (no auth required)
| Method | URL                              | Description                     |
|--------|----------------------------------|---------------------------------|
| GET    | `/dashboard/stats`               | School-wide statistics          |
| GET    | `/dashboard/attendance-analytics`| Monthly attendance chart data   |
| GET    | `/dashboard/grade-distribution`  | Grade distribution + passing    |
| GET    | `/api/students?page=1&search=`   | Paginated student directory     |
| GET    | `/api/teachers?page=1&search=`   | Paginated teacher directory     |
| GET    | `/api/subjects`                  | All 15 subjects with resources  |
| GET    | `/api/awards`                    | All 25 awards                   |
| GET    | `/api/classes`                   | All 24 classes                  |
| GET    | `/timetable/classes`             | List of class names             |
| GET    | `/timetable/class/<name>`        | Weekly schedule for a class     |

### Auth
| Method | URL                       | Body                                |
|--------|---------------------------|-------------------------------------|
| POST   | `/auth/teacher/login`     | `{email, password}`                 |
| POST   | `/auth/teacher/register`  | `{name, email, password, subject}`  |
| POST   | `/auth/student/login`     | `{email, password}`                 |
| POST   | `/auth/student/register`  | `{name, email, password, class}`    |
| GET    | `/auth/logout`            | —                                   |

### Teacher (login required)
| Method | URL                       | Description               |
|--------|---------------------------|---------------------------|
| GET    | `/teacher/dashboard`      | Teacher portal page       |
| GET    | `/teacher/my-students`    | Paginated student list    |
| GET    | `/teacher/today-classes`  | Today's schedule          |
| POST   | `/teacher/update-grade`   | Update student grade      |
| POST   | `/teacher/mark-attendance`| Mark student attendance   |

### Student (login required)
| Method | URL                   | Description             |
|--------|-----------------------|-------------------------|
| GET    | `/student/dashboard`  | Student portal page     |
| GET    | `/student/grades`     | Subject marks + grade   |
| GET    | `/student/attendance` | Last 30 attendance days |
| GET    | `/student/profile`    | Full student profile    |

---

## 🧩 Architecture Notes

- **App Factory pattern** (`create_app()`) — enables testing and multiple configs
- **Blueprint-per-module** — auth, dashboard, teacher, student, timetable, api all isolated
- **Flask-Login** — session-based auth with unified `User` wrapper for both roles
- **Flask-Bcrypt** — all passwords hashed (never stored in plain text)
- **MongoDB Indexes** — unique index on emails, compound index on (student_id, date) for attendance
- **CSS Variables** — full theming via `:root` vars, easy to retheme in one place
- **Chart.js** — attendance line chart, grade bar chart rendered client-side

---

## 🚀 Production Checklist

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Use `FLASK_ENV=production`
- [ ] Add HTTPS (nginx + certbot)
- [ ] Enable Flask-WTF CSRF protection
- [ ] Add rate limiting (Flask-Limiter)
- [ ] Use gunicorn: `gunicorn "app:create_app()" -w 4`
- [ ] Set up MongoDB auth + replica set
- [ ] Add logging (structlog / loguru)
