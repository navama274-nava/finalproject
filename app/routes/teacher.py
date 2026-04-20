"""
Teacher Blueprint — teacher portal, class management, grade entry, attendance marking.
"""
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.models.student import StudentModel
from app.models.school  import AttendanceModel
from app.utils.helpers  import api_success, api_error
from datetime import datetime

teacher_bp = Blueprint('teacher', __name__)


@teacher_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'teacher':
        return render_template('auth/unauthorized.html'), 403
    return render_template('teacher/dashboard.html', teacher=current_user._doc)


@teacher_bp.route('/my-students')
@login_required
def my_students():
    """Returns paginated student list for the teacher's classes."""
    if current_user.role != 'teacher':
        return api_error('Unauthorized', 403)

    page     = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 25))
    search   = request.args.get('search', '')

    docs, total = StudentModel.find_all(page=page, per_page=per_page, search=search)
    return jsonify({
        'students':   docs,
        'total':      total,
        'page':       page,
        'per_page':   per_page,
        'total_pages': -(-total // per_page),  # ceiling division
    })


@teacher_bp.route('/mark-attendance', methods=['POST'])
@login_required
def mark_attendance():
    if current_user.role != 'teacher':
        return api_error('Unauthorized', 403)

    data       = request.get_json()
    student_id = data.get('student_id')
    class_name = data.get('class_name')
    status     = data.get('status', 'present')
    date_str   = data.get('date', datetime.utcnow().strftime('%Y-%m-%d'))

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return api_error('Invalid date format')

    AttendanceModel.mark(student_id, class_name, date, status)
    return api_success(message='Attendance marked successfully')


@teacher_bp.route('/update-grade', methods=['POST'])
@login_required
def update_grade():
    if current_user.role != 'teacher':
        return api_error('Unauthorized', 403)

    data       = request.get_json()
    student_id = data.get('student_id')
    subject    = data.get('subject')
    marks      = int(data.get('marks', 0))

    if not all([student_id, subject]) or not (0 <= marks <= 100):
        return api_error('Invalid input data')

    StudentModel.update_grades(student_id, subject, marks)
    return api_success(message='Grade updated successfully')


@teacher_bp.route('/today-classes')
@login_required
def today_classes():
    """Returns today's schedule for the logged-in teacher."""
    return jsonify({'schedule': []})
