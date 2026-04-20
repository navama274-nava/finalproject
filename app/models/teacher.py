"""
Teacher model — all MongoDB operations for the teachers collection.
"""
from bson import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo


class TeacherModel:
    COLLECTION = 'teachers'

    @staticmethod
    def collection():
        return mongo.db.teachers

    # ── Create ─────────────────────────────────────────────────────────────
    @staticmethod
    def create(name: str, email: str, password: str, subject: str) -> dict:
        count = TeacherModel.collection().count_documents({})
        tid   = f"T{str(count + 1).zfill(3)}"

        doc = {
            'name':          name,
            'email':         email.lower().strip(),
            'password_hash': generate_password_hash(password),
            'subject':       subject,
            'teacher_id':    tid,
            'created_at':    datetime.utcnow(),
            'classes':       [],
        }

        result = TeacherModel.collection().insert_one(doc)
        doc['_id'] = result.inserted_id
        return doc

    # ── Read ───────────────────────────────────────────────────────────────
    @staticmethod
    def find_by_email(email: str):
        return TeacherModel.collection().find_one({'email': email.lower().strip()})

    @staticmethod
    def find_by_id(oid):
        try:
            return TeacherModel.collection().find_one({'_id': ObjectId(oid)})
        except Exception:
            return None

    @staticmethod
    def find_all(page: int = 1, per_page: int = 20, search: str = ''):
        query = {}
        if search:
            query = {'$or': [
                {'name':    {'$regex': search, '$options': 'i'}},
                {'subject': {'$regex': search, '$options': 'i'}},
            ]}
        skip  = (page - 1) * per_page
        total = TeacherModel.collection().count_documents(query)
        docs  = list(
            TeacherModel.collection()
            .find(query, {'password_hash': 0})
            .skip(skip)
            .limit(per_page)
        )
        for d in docs:
            d['_id'] = str(d['_id'])
        return docs, total

    @staticmethod
    def count() -> int:
        return TeacherModel.collection().count_documents({})

    # ── Verify password ────────────────────────────────────────────────────
    @staticmethod
    def verify_password(doc, password: str) -> bool:
        return check_password_hash(doc['password_hash'], password)
