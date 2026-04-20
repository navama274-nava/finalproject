"""
Student model — all MongoDB operations for the students collection.
"""
from bson import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo


class StudentModel:
    COLLECTION = 'students'

    @staticmethod
    def collection():
        return mongo.db.students

    # ── Create ─────────────────────────────────────────────────────────────
    @staticmethod
    def create(name: str, email: str, password: str, student_class: str) -> dict:
        count = StudentModel.collection().count_documents({})
        roll  = f"S{str(count + 1001).zfill(4)}"

        doc = {
            'name':             name,
            'email':            email.lower().strip(),
            'password_hash':    generate_password_hash(password),
            'class':            student_class,
            'roll':             roll,
            'created_at':       datetime.utcnow(),
            # Academic data (seeded/updated separately)
            'marks':            {},
            'attendance':       [],
            'overall_marks':    0,
            'overall_grade':    'N/A',
            'attendance_pct':   0,
        }

        result = StudentModel.collection().insert_one(doc)
        doc['_id'] = result.inserted_id
        return doc

    # ── Read ───────────────────────────────────────────────────────────────
    @staticmethod
    def find_by_email(email: str):
        return StudentModel.collection().find_one({'email': email.lower().strip()})

    @staticmethod
    def find_by_id(oid):
        try:
            return StudentModel.collection().find_one({'_id': ObjectId(oid)})
        except Exception:
            return None

    @staticmethod
    def find_all(page: int = 1, per_page: int = 20, search: str = ''):
        query = {}
        if search:
            query = {'$or': [
                {'name':  {'$regex': search, '$options': 'i'}},
                {'roll':  {'$regex': search, '$options': 'i'}},
                {'class': {'$regex': search, '$options': 'i'}},
            ]}
        skip  = (page - 1) * per_page
        total = StudentModel.collection().count_documents(query)
        docs  = list(
            StudentModel.collection()
            .find(query, {'password_hash': 0})
            .skip(skip)
            .limit(per_page)
        )
        # Serialize ObjectIds
        for d in docs:
            d['_id'] = str(d['_id'])
        return docs, total

    @staticmethod
    def count() -> int:
        return StudentModel.collection().count_documents({})

    @staticmethod
    def average_attendance() -> float:
        pipeline = [
            {'$group': {'_id': None, 'avg': {'$avg': '$attendance_pct'}}}
        ]
        result = list(StudentModel.collection().aggregate(pipeline))
        return round(result[0]['avg'], 1) if result else 0.0

    @staticmethod
    def passing_rate() -> dict:
        total   = StudentModel.count()
        passed  = StudentModel.collection().count_documents({'overall_marks': {'$gte': 40}})
        failed  = total - passed
        rate    = round((passed / total) * 100, 1) if total else 0
        return {'total': total, 'passed': passed, 'failed': failed, 'rate': rate}

    @staticmethod
    def grade_distribution() -> dict:
        pipeline = [
            {'$group': {'_id': '$overall_grade', 'count': {'$sum': 1}}}
        ]
        result = {d['_id']: d['count'] for d in StudentModel.collection().aggregate(pipeline)}
        # Ensure all grade keys exist
        for g in ['A+', 'A', 'B+', 'B', 'C', 'D', 'F']:
            result.setdefault(g, 0)
        return result

    # ── Verify password ────────────────────────────────────────────────────
    @staticmethod
    def verify_password(doc, password: str) -> bool:
        return check_password_hash(doc['password_hash'], password)

    # ── Update ─────────────────────────────────────────────────────────────
    @staticmethod
    def update_grades(student_id, subject: str, marks: int):
        grade = StudentModel._marks_to_grade(marks)
        StudentModel.collection().update_one(
            {'_id': ObjectId(student_id)},
            {'$set': {f'marks.{subject}': {'score': marks, 'grade': grade}}}
        )

    @staticmethod
    def _marks_to_grade(marks: int) -> str:
        if marks >= 90: return 'A+'
        if marks >= 80: return 'A'
        if marks >= 70: return 'B+'
        if marks >= 60: return 'B'
        if marks >= 50: return 'C'
        if marks >= 40: return 'D'
        return 'F'
