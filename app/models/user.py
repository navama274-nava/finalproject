"""
User model — wraps both Teacher and Student documents for Flask-Login.
"""
from flask_login import UserMixin
from bson import ObjectId
from app import mongo


class User(UserMixin):
    """
    Unified user class used by Flask-Login.
    Works for both teachers and students.
    """

    def __init__(self, user_doc, role: str):
        self._id   = str(user_doc['_id'])
        self.name  = user_doc.get('name', '')
        self.email = user_doc.get('email', '')
        self.role  = role  # 'teacher' | 'student'
        self._doc  = user_doc  # full raw document

    # Flask-Login requires get_id() to return a unique string
    def get_id(self):
        return f"{self.role}:{self._id}"

    def to_dict(self):
        return {
            'id':    self._id,
            'name':  self.name,
            'email': self.email,
            'role':  self.role,
        }


def load_user_by_id(user_id: str):
    """
    Flask-Login user_loader callback.
    user_id format: "teacher:<mongo_id>" or "student:<mongo_id>"
    """
    if not user_id or ':' not in user_id:
        return None

    role, oid = user_id.split(':', 1)

    try:
        oid = ObjectId(oid)
    except Exception:
        return None

    if role == 'teacher':
        doc = mongo.db.teachers.find_one({'_id': oid})
        return User(doc, 'teacher') if doc else None
    elif role == 'student':
        doc = mongo.db.students.find_one({'_id': oid})
        return User(doc, 'student') if doc else None

    return None
