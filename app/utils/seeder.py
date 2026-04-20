"""
Database seeder — runs once on first startup when collections are empty.
Generates 1050 students, 100 teachers, 24 classes, 15 subjects, 25 awards,
and full timetable data matching the original frontend.
"""
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app import mongo


FIRST_NAMES = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer',
               'Michael', 'Linda', 'William', 'Elizabeth', 'David', 'Barbara',
               'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah',
               'Charles', 'Karen']

LAST_NAMES  = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia',
               'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez',
               'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore',
               'Jackson', 'Martin']

CLASSES = [
    'Grade 1A',  'Grade 1B',  'Grade 2A',  'Grade 2B',
    'Grade 3A',  'Grade 3B',  'Grade 4A',  'Grade 4B',
    'Grade 5A',  'Grade 5B',  'Grade 6A',  'Grade 6B',
    'Grade 7A',  'Grade 7B',  'Grade 8A',  'Grade 8B',
    'Grade 9A',  'Grade 9B',  'Grade 10A', 'Grade 10B',
    'Grade 11A', 'Grade 11B', 'Grade 12A', 'Grade 12B',
]

SUBJECTS_DATA = [
    {'name': 'Mathematics',          'teacher': 'Dr. Sarah Johnson',     'students': 450,
     'books': ['NCERT Mathematics', 'RD Sharma'],
     'websites': ['https://www.khanacademy.org/math', 'https://brilliant.org']},
    {'name': 'Physics',              'teacher': 'Prof. Michael Chen',     'students': 380,
     'books': ['NCERT Physics', 'HC Verma'],
     'websites': ['https://www.physicsclassroom.com', 'https://hyperphysics.phy-astr.gsu.edu']},
    {'name': 'Chemistry',            'teacher': 'Dr. Emily Brown',        'students': 420,
     'books': ['NCERT Chemistry', 'OP Tandon'],
     'websites': ['https://byjus.com/chemistry', 'https://www.chemguide.co.uk']},
    {'name': 'Biology',              'teacher': 'Prof. David Wilson',     'students': 400,
     'books': ['NCERT Biology', 'Trueman Biology'],
     'websites': ['https://www.biologyonline.com', 'https://www.khanacademy.org/science/biology']},
    {'name': 'English',              'teacher': 'Ms. Jessica Taylor',     'students': 520,
     'books': ['NCERT English', 'Wren & Martin'],
     'websites': ['https://www.grammarly.com', 'https://www.bbc.co.uk/learningenglish']},
    {'name': 'Computer Science',     'teacher': 'Dr. James Lee',          'students': 300,
     'books': ['NCERT Computer Science', 'Sumita Arora'],
     'websites': ['https://www.w3schools.com', 'https://cs50.harvard.edu']},
    {'name': 'History',              'teacher': 'Prof. Robert Anderson',  'students': 350,
     'books': ['NCERT History', 'World History by H.G. Wells'],
     'websites': ['https://www.history.com', 'https://www.britannica.com/topic/history']},
    {'name': 'Geography',            'teacher': 'Ms. Patricia Martinez',  'students': 340,
     'books': ['NCERT Geography', 'Certificate Physical Geography'],
     'websites': ['https://www.nationalgeographic.com', 'https://geography.name']},
    {'name': 'Economics',            'teacher': 'Dr. William Harris',     'students': 280,
     'books': ['NCERT Economics', 'Indian Economy by Ramesh Singh'],
     'websites': ['https://www.economicshelp.org', 'https://www.investopedia.com']},
    {'name': 'Political Science',    'teacher': 'Prof. George Scott',     'students': 260,
     'books': ['NCERT Political Science', 'Indian Constitution'],
     'websites': ['https://www.legislative.gov.in', 'https://iaspaper.net/polity']},
    {'name': 'Psychology',           'teacher': 'Dr. Lisa King',          'students': 230,
     'books': ['NCERT Psychology', 'Introduction to Psychology by Atkinson'],
     'websites': ['https://www.psychologytoday.com', 'https://simplypsychology.org']},
    {'name': 'Sociology',            'teacher': 'Prof. Brian Wright',     'students': 210,
     'books': ['NCERT Sociology', 'Indian Society by Ram Ahuja'],
     'websites': ['https://www.sociologygroup.com', 'https://www.thoughtco.com/sociology']},
    {'name': 'Business Studies',     'teacher': 'Ms. Margaret Clark',     'students': 270,
     'books': ['NCERT Business Studies', 'Principles of Management'],
     'websites': ['https://www.businessnewsdaily.com', 'https://hbr.org']},
    {'name': 'Accountancy',          'teacher': 'Dr. Edward Adams',       'students': 290,
     'books': ['NCERT Accountancy', 'Financial Accounting by Grewal'],
     'websites': ['https://www.accountingcoach.com', 'https://corporatefinanceinstitute.com']},
    {'name': 'Environmental Science','teacher': 'Prof. Stephanie Baker',  'students': 310,
     'books': ['NCERT Environmental Science', 'Ecology by Odum'],
     'websites': ['https://www.epa.gov', 'https://www.nationalgeographic.com/environment']},
]

AWARDS_DATA = [
    {'name': 'National Science Olympiad',    'winner': 'Alice Johnson',    'class': 'Grade 10A', 'rank': 'Gold Medal',   'year': 2024},
    {'name': 'International Math Competition','winner': 'Bob Smith',       'class': 'Grade 9B',  'rank': 'Silver Medal', 'year': 2024},
    {'name': 'Robotics Championship',         'winner': 'Charlie Brown',   'class': 'Grade 11A', 'rank': 'Gold Medal',   'year': 2024},
    {'name': 'Essay Writing Competition',     'winner': 'Diana Prince',    'class': 'Grade 8A',  'rank': '1st Prize',    'year': 2024},
    {'name': 'Coding Hackathon',              'winner': 'Julia Roberts',   'class': 'Grade 11A', 'rank': 'Winner',       'year': 2024},
    {'name': 'Science Fair',                  'winner': 'Laura Wilson',    'class': 'Grade 10A', 'rank': '1st Prize',    'year': 2024},
    {'name': 'Debate Competition',            'winner': 'Michael Johnson', 'class': 'Grade 12B', 'rank': 'Champion',     'year': 2024},
    {'name': 'Art Exhibition',                'winner': 'Sophia Martinez', 'class': 'Grade 9A',  'rank': 'Best Artist',  'year': 2024},
    {'name': 'Music Festival',                'winner': 'Daniel Brown',    'class': 'Grade 8B',  'rank': '1st Prize',    'year': 2024},
    {'name': 'Sports Championship',           'winner': 'Emma Davis',      'class': 'Grade 10B', 'rank': 'Gold Medal',   'year': 2024},
    {'name': 'Chess Tournament',              'winner': 'Oliver Wilson',   'class': 'Grade 7A',  'rank': 'Champion',     'year': 2024},
    {'name': 'Spelling Bee',                  'winner': 'Isabella Garcia', 'class': 'Grade 6B',  'rank': 'Winner',       'year': 2024},
    {'name': 'Drama Competition',             'winner': 'Ethan Rodriguez', 'class': 'Grade 11B', 'rank': 'Best Actor',   'year': 2024},
    {'name': 'Photography Contest',           'winner': 'Mia Anderson',    'class': 'Grade 9B',  'rank': 'Winner',       'year': 2024},
    {'name': 'Quiz Competition',              'winner': 'Liam Thomas',     'class': 'Grade 10A', 'rank': 'Champion',     'year': 2024},
    {'name': 'Innovation Award',              'winner': 'Ava Taylor',      'class': 'Grade 12A', 'rank': 'Gold Medal',   'year': 2024},
    {'name': 'Young Scientist Award',         'winner': 'Noah Moore',      'class': 'Grade 11A', 'rank': 'Winner',       'year': 2024},
    {'name': 'Literature Award',              'winner': 'Charlotte Jackson','class':'Grade 8A',  'rank': '1st Prize',    'year': 2024},
    {'name': 'Mathematics Olympiad',          'winner': 'Amelia Martin',   'class': 'Grade 10B', 'rank': 'Gold Medal',   'year': 2024},
    {'name': 'Physics Challenge',             'winner': 'Elijah Lee',      'class': 'Grade 9A',  'rank': 'Silver Medal', 'year': 2024},
    {'name': 'Chemistry Excellence',          'winner': 'Harper Perez',    'class': 'Grade 11B', 'rank': 'Gold Medal',   'year': 2024},
    {'name': 'Biology Research',              'winner': 'Benjamin White',  'class': 'Grade 12B', 'rank': 'Winner',       'year': 2024},
    {'name': 'English Literature',            'winner': 'Evelyn Harris',   'class': 'Grade 10A', 'rank': '1st Prize',    'year': 2024},
    {'name': 'Computer Programming',          'winner': 'Alexander Clark', 'class': 'Grade 11A', 'rank': 'Champion',     'year': 2024},
    {'name': 'Environmental Award',           'winner': 'Sofia Lewis',     'class': 'Grade 9B',  'rank': 'Gold Medal',   'year': 2024},
]

DAYS    = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
ROOMS   = ['Room 101', 'Lab 2', 'Lab 1', 'Room 103', 'Computer Lab',
           'Room 104', 'Room 105', 'Room 106']
TIMETABLE_SUBJECTS = [
    ('Mathematics',      'Dr. Sarah Johnson'),
    ('Physics',          'Prof. Michael Chen'),
    ('Chemistry',        'Dr. Emily Brown'),
    ('English',          'Ms. Jessica Taylor'),
    ('Computer Science', 'Dr. James Lee'),
    ('Biology',          'Prof. David Wilson'),
    ('History',          'Prof. Robert Anderson'),
    ('Geography',        'Ms. Patricia Martinez'),
]


def _marks_to_grade(m: int) -> str:
    if m >= 90: return 'A+'
    if m >= 80: return 'A'
    if m >= 70: return 'B+'
    if m >= 60: return 'B'
    if m >= 50: return 'C'
    if m >= 40: return 'D'
    return 'F'


def seed_if_empty():
    """Only seeds when all core collections are empty."""
    db = mongo.db
    if db.students.count_documents({}) > 0:
        print("[Seeder] Data already exists. Skipping seed.")
        return

    print("[Seeder] Seeding database …")

    # ── Subjects ───────────────────────────────────────────────────────────
    db.subjects.insert_many(SUBJECTS_DATA)
    print(f"[Seeder] Inserted {len(SUBJECTS_DATA)} subjects.")

    # ── Awards ─────────────────────────────────────────────────────────────
    db.awards.insert_many(AWARDS_DATA)
    print(f"[Seeder] Inserted {len(AWARDS_DATA)} awards.")

    # ── Teachers (100) ─────────────────────────────────────────────────────
    teacher_docs = []
    subject_names = [s['name'] for s in SUBJECTS_DATA]
    for i in range(1, 101):
        fn = random.choice(FIRST_NAMES)
        ln = random.choice(LAST_NAMES)
        teacher_docs.append({
            'name':          f"{fn} {ln}",
            'email':         f"{fn.lower()}.{ln.lower()}{i}@teacher.school.com",
            'password_hash': generate_password_hash('teacher123'),
            'subject':       random.choice(subject_names),
            'teacher_id':    f"T{str(i).zfill(3)}",
            'created_at':    datetime.utcnow(),
            'classes':       random.sample(CLASSES, random.randint(1, 3)),
        })
    db.teachers.insert_many(teacher_docs)
    print(f"[Seeder] Inserted {len(teacher_docs)} teachers.")

    # ── Students (1050) ────────────────────────────────────────────────────
    student_docs = []
    base_date    = datetime(2024, 1, 1)

    for i in range(1, 1051):
        fn          = random.choice(FIRST_NAMES)
        ln          = random.choice(LAST_NAMES)
        cls         = random.choice(CLASSES)
        overall_m   = random.randint(35, 98)
        att_pct     = random.randint(65, 99)

        # Per-subject marks
        subj_marks = {}
        for subj in SUBJECTS_DATA[:8]:
            m = random.randint(35, 98)
            subj_marks[subj['name']] = {'score': m, 'grade': _marks_to_grade(m)}

        # Attendance records (last 30 days)
        att_records = []
        for day_offset in range(30):
            status = random.choices(
                ['present', 'absent', 'late'],
                weights=[att_pct, 100 - att_pct - 3, 3]
            )[0]
            att_records.append({
                'date':   base_date + timedelta(days=day_offset),
                'status': status,
            })

        student_docs.append({
            'name':           f"{fn} {ln}",
            'email':          f"{fn.lower()}.{ln.lower()}{i}@student.school.com",
            'password_hash':  generate_password_hash('student123'),
            'class':          cls,
            'roll':           f"S{str(i + 1000).zfill(4)}",
            'created_at':     datetime.utcnow(),
            'marks':          subj_marks,
            'attendance':     att_records,
            'overall_marks':  overall_m,
            'overall_grade':  _marks_to_grade(overall_m),
            'attendance_pct': att_pct,
        })

        # Batch inserts every 200 for memory efficiency
        if len(student_docs) == 200:
            db.students.insert_many(student_docs)
            student_docs = []

    if student_docs:
        db.students.insert_many(student_docs)
    print(f"[Seeder] Inserted 1050 students.")

    # ── Classes ────────────────────────────────────────────────────────────
    teacher_list = list(db.teachers.find({}, {'name': 1}))
    class_docs   = []
    for idx, cls in enumerate(CLASSES):
        ct = teacher_list[idx % len(teacher_list)]
        class_docs.append({
            'name':          cls,
            'class_teacher': ct['name'],
            'room_number':   f"Room {100 + idx + 1}",
            'students_count': db.students.count_documents({'class': cls}),
        })
    db.classes.insert_many(class_docs)
    print(f"[Seeder] Inserted {len(class_docs)} classes.")

    # ── Timetables ─────────────────────────────────────────────────────────
    timetable_docs = []
    for cls in CLASSES:
        schedule = {}
        for day in DAYS:
            slots = []
            for period in range(5):
                subj_idx   = random.randint(0, len(TIMETABLE_SUBJECTS) - 1)
                subj, teacher = TIMETABLE_SUBJECTS[subj_idx]
                start_h    = 9 + period
                slots.append({
                    'subject': subj,
                    'teacher': teacher,
                    'time':    f"{start_h:02d}:00 - {start_h+1:02d}:00",
                    'room':    random.choice(ROOMS),
                })
            # Insert lunch at index 3
            slots.insert(3, {
                'subject': 'Lunch Break',
                'teacher': '-',
                'time':    '12:30 - 01:30',
                'room':    'Cafeteria',
            })
            schedule[day] = slots
        timetable_docs.append({'class_name': cls, 'schedule': schedule})

    db.timetables.insert_many(timetable_docs)
    print(f"[Seeder] Inserted {len(timetable_docs)} timetables.")

    # ── Indexes ────────────────────────────────────────────────────────────
    db.students.create_index('email', unique=True, background=True)
    db.students.create_index('class', background=True)
    db.teachers.create_index('email', unique=True, background=True)
    db.attendance.create_index([('student_id', 1), ('date', 1)], unique=True, background=True)

    print("[Seeder] ✅ Database seeding complete!")
