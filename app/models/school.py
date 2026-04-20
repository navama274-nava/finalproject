"""
Supporting models: Subject, Award, ClassInfo, Timetable.
All are plain MongoDB collection wrappers — no auth needed.
"""
from bson import ObjectId
from app import mongo


class SubjectModel:
    @staticmethod
    def find_all():
        docs = list(mongo.db.subjects.find())
        for d in docs:
            d['_id'] = str(d['_id'])
        return docs

    @staticmethod
    def find_by_name(name: str):
        return mongo.db.subjects.find_one({'name': {'$regex': name, '$options': 'i'}})

    @staticmethod
    def count() -> int:
        return mongo.db.subjects.count_documents({})


class AwardModel:
    @staticmethod
    def find_all():
        docs = list(mongo.db.awards.find())
        for d in docs:
            d['_id'] = str(d['_id'])
        return docs

    @staticmethod
    def count() -> int:
        return mongo.db.awards.count_documents({})


class ClassInfoModel:
    @staticmethod
    def find_all():
        docs = list(mongo.db.classes.find())
        for d in docs:
            d['_id'] = str(d['_id'])
        return docs

    @staticmethod
    def find_by_name(name: str):
        return mongo.db.classes.find_one({'name': name})

    @staticmethod
    def count() -> int:
        return mongo.db.classes.count_documents({})


class TimetableModel:
    @staticmethod
    def find_by_class(class_name: str):
        doc = mongo.db.timetables.find_one({'class_name': class_name})
        if doc:
            doc['_id'] = str(doc['_id'])
        return doc

    @staticmethod
    def find_all_class_names():
        return [d['class_name'] for d in mongo.db.timetables.find({}, {'class_name': 1})]

    @staticmethod
    def upsert(class_name: str, schedule: dict):
        mongo.db.timetables.update_one(
            {'class_name': class_name},
            {'$set': {'class_name': class_name, 'schedule': schedule}},
            upsert=True
        )


class AttendanceModel:
    """
    Attendance document structure:
    {
        student_id: ObjectId,
        class: str,
        date: datetime,
        status: 'present' | 'absent' | 'late'
    }
    """
    @staticmethod
    def mark(student_id, class_name: str, date, status: str):
        mongo.db.attendance.update_one(
            {'student_id': ObjectId(student_id), 'date': date},
            {'$set': {
                'student_id': ObjectId(student_id),
                'class':      class_name,
                'date':       date,
                'status':     status,
            }},
            upsert=True
        )

    @staticmethod
    def get_student_records(student_id, limit: int = 30):
        docs = list(
            mongo.db.attendance
            .find({'student_id': ObjectId(student_id)})
            .sort('date', -1)
            .limit(limit)
        )
        for d in docs:
            d['_id']        = str(d['_id'])
            d['student_id'] = str(d['student_id'])
        return docs

    @staticmethod
    def monthly_summary():
        """Aggregate attendance count per month for analytics."""
        pipeline = [
            {'$group': {
                '_id':     {'$month': '$date'},
                'present': {'$sum': {'$cond': [{'$eq': ['$status', 'present']}, 1, 0]}},
                'absent':  {'$sum': {'$cond': [{'$eq': ['$status', 'absent']},  1, 0]}},
                'late':    {'$sum': {'$cond': [{'$eq': ['$status', 'late']},    1, 0]}},
                'total':   {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        return list(mongo.db.attendance.aggregate(pipeline))
