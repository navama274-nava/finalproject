"""
Auth Blueprint — handles teacher and student login / register / logout.
"""
from flask import Blueprint, request, redirect, url_for, flash, render_template, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.teacher import TeacherModel
from app.models.student import StudentModel
from app.models.user import User

auth_bp = Blueprint('auth', __name__)


# ── Login page (shared render) ──────────────────────────────────────────────

@auth_bp.route('/login')
def login_page():
    return render_template('auth/login.html')


# ── Teacher register ────────────────────────────────────────────────────────

@auth_bp.route('/teacher/register', methods=['POST'])
def teacher_register():
    data     = request.get_json() or request.form
    name     = data.get('name', '').strip()
    email    = data.get('email', '').strip()
    password = data.get('password', '')
    subject  = data.get('subject', 'Mathematics')

    if not all([name, email, password]):
        return {'success': False, 'message': 'All fields are required'}, 400

    if TeacherModel.find_by_email(email):
        return {'success': False, 'message': 'Email already registered'}, 409

    teacher = TeacherModel.create(name, email, password, subject)
    return {'success': True, 'message': 'Registration successful! Please login.'}, 201


# ── Teacher login ───────────────────────────────────────────────────────────

@auth_bp.route('/teacher/login', methods=['POST'])
def teacher_login():
    data     = request.get_json() or request.form
    email    = data.get('email', '').strip()
    password = data.get('password', '')

    teacher_doc = TeacherModel.find_by_email(email)
    if not teacher_doc or not TeacherModel.verify_password(teacher_doc, password):
        return {'success': False, 'message': 'Invalid email or password'}, 401

    user = User(teacher_doc, 'teacher')
    login_user(user, remember=True)

    return {
        'success': True,
        'message': 'Login successful',
        'redirect': url_for('teacher.dashboard'),
        'user': user.to_dict()
    }, 200


# ── Student register ────────────────────────────────────────────────────────

@auth_bp.route('/student/register', methods=['POST'])
def student_register():
    data          = request.get_json() or request.form
    name          = data.get('name', '').strip()
    email         = data.get('email', '').strip()
    password      = data.get('password', '')
    student_class = data.get('class', 'Grade 10A')

    if not all([name, email, password]):
        return {'success': False, 'message': 'All fields are required'}, 400

    if StudentModel.find_by_email(email):
        return {'success': False, 'message': 'Email already registered'}, 409

    StudentModel.create(name, email, password, student_class)
    return {'success': True, 'message': 'Registration successful! Please login.'}, 201


# ── Student login ───────────────────────────────────────────────────────────

@auth_bp.route('/student/login', methods=['POST'])
def student_login():
    data     = request.get_json() or request.form
    email    = data.get('email', '').strip()
    password = data.get('password', '')

    student_doc = StudentModel.find_by_email(email)
    if not student_doc or not StudentModel.verify_password(student_doc, password):
        return {'success': False, 'message': 'Invalid email or password'}, 401

    user = User(student_doc, 'student')
    login_user(user, remember=True)

    return {
        'success': True,
        'message': 'Login successful',
        'redirect': url_for('student.dashboard'),
        'user': user.to_dict()
    }, 200


# ── Logout ──────────────────────────────────────────────────────────────────

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
