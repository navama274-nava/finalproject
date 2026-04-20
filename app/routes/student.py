"""
Student Blueprint — student portal, grades, attendance history.
"""
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.models.school import AttendanceModel
from app.utils.helpers import api_error, serialize_doc

student_bp = Blueprint('student', __name__)


@student_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        return render_template('auth/unauthorized.html'), 403
    return render_template('student/dashboard.html', student=current_user._doc)


@student_bp.route('/grades')
@login_required
def grades():
    if current_user.role != 'student':
        return api_error('Unauthorized', 403)
    marks = current_user._doc.get('marks', {})
    return jsonify({'marks': marks, 'overall_grade': current_user._doc.get('overall_grade', 'N/A')})


@student_bp.route('/attendance')
@login_required
def attendance():
    if current_user.role != 'student':
        return api_error('Unauthorized', 403)
    records = AttendanceModel.get_student_records(current_user._id, limit=30)
    # Serialize dates
    for r in records:
        if 'date' in r and hasattr(r['date'], 'strftime'):
            r['date'] = r['date'].strftime('%Y-%m-%d')
    return jsonify({
        'records':         records,
        'attendance_pct':  current_user._doc.get('attendance_pct', 0),
    })


@student_bp.route('/profile')
@login_required
def profile():
    if current_user.role != 'student':
        return api_error('Unauthorized', 403)
    doc = serialize_doc(current_user._doc)
    doc.pop('password_hash', None)
    return jsonify(doc)
