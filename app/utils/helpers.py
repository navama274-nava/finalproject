"""
Utility helpers shared across the application.
"""
from bson import ObjectId
from flask import jsonify
import math


def serialize_doc(doc: dict) -> dict:
    """Recursively convert ObjectId and datetime to JSON-serializable types."""
    if doc is None:
        return {}
    result = {}
    for k, v in doc.items():
        if isinstance(v, ObjectId):
            result[k] = str(v)
        elif hasattr(v, 'isoformat'):
            result[k] = v.isoformat()
        elif isinstance(v, dict):
            result[k] = serialize_doc(v)
        elif isinstance(v, list):
            result[k] = [serialize_doc(i) if isinstance(i, dict) else i for i in v]
        else:
            result[k] = v
    return result


def paginate(data: list, page: int, per_page: int) -> dict:
    total      = len(data)
    total_pages = math.ceil(total / per_page)
    start      = (page - 1) * per_page
    end        = start + per_page
    return {
        'items':       data[start:end],
        'total':       total,
        'page':        page,
        'per_page':    per_page,
        'total_pages': total_pages,
        'has_prev':    page > 1,
        'has_next':    page < total_pages,
    }


def api_success(data=None, message='Success', status=200):
    return jsonify({'success': True, 'message': message, 'data': data}), status


def api_error(message='Error', status=400):
    return jsonify({'success': False, 'message': message}), status


def marks_to_grade(marks: int) -> str:
    if marks >= 90: return 'A+'
    if marks >= 80: return 'A'
    if marks >= 70: return 'B+'
    if marks >= 60: return 'B'
    if marks >= 50: return 'C'
    if marks >= 40: return 'D'
    return 'F'
