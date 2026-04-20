"""
Timetable Blueprint — serves timetable data by class.
"""
from flask import Blueprint, render_template, jsonify, request
from app.models.school import TimetableModel

timetable_bp = Blueprint('timetable', __name__)


@timetable_bp.route('/')
def index():
    return render_template('timetable/index.html')


@timetable_bp.route('/classes')
def class_list():
    """Returns all class names that have a timetable."""
    names = TimetableModel.find_all_class_names()
    return jsonify({'classes': names})


@timetable_bp.route('/class/<class_name>')
def class_timetable(class_name):
    """Returns full weekly schedule for a given class."""
    doc = TimetableModel.find_by_class(class_name)
    if not doc:
        return jsonify({'error': 'Timetable not found'}), 404
    return jsonify({'class_name': class_name, 'schedule': doc.get('schedule', {})})
