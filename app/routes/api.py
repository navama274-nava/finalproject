"""
API Blueprint — public and protected JSON endpoints consumed by the frontend JS.
"""
from flask import Blueprint, jsonify, request
from app.models.student import StudentModel
from app.models.teacher import TeacherModel
from app.models.school  import SubjectModel, AwardModel, ClassInfoModel
from app.utils.helpers  import api_error

api_bp = Blueprint('api', __name__)


# ── Students ────────────────────────────────────────────────────────────────

@api_bp.route('/students')
def students():
    page     = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    search   = request.args.get('search', '')

    docs, total = StudentModel.find_all(page=page, per_page=per_page, search=search)
    return jsonify({
        'students':    docs,
        'total':       total,
        'page':        page,
        'total_pages': -(-total // per_page),
    })


@api_bp.route('/students/stats')
def student_stats():
    passing = StudentModel.passing_rate()
    dist    = StudentModel.grade_distribution()
    return jsonify({'passing': passing, 'grade_distribution': dist})


# ── Teachers ────────────────────────────────────────────────────────────────

@api_bp.route('/teachers')
def teachers():
    page     = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    search   = request.args.get('search', '')

    docs, total = TeacherModel.find_all(page=page, per_page=per_page, search=search)
    return jsonify({
        'teachers':    docs,
        'total':       total,
        'page':        page,
        'total_pages': -(-total // per_page),
    })


# ── Subjects ────────────────────────────────────────────────────────────────

@api_bp.route('/subjects')
def subjects():
    return jsonify({'subjects': SubjectModel.find_all()})


# ── Awards ──────────────────────────────────────────────────────────────────

@api_bp.route('/awards')
def awards():
    return jsonify({'awards': AwardModel.find_all()})


# ── Classes ─────────────────────────────────────────────────────────────────

@api_bp.route('/classes')
def classes():
    return jsonify({'classes': ClassInfoModel.find_all()})
