import json
import sqlite3
from datetime import datetime

DB_NAME = "careerguide.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        education TEXT DEFAULT '',
        interests TEXT DEFAULT '',
        skills TEXT DEFAULT '',
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        interest TEXT,
        career_goal TEXT,
        academic_performance TEXT,
        programming TEXT,
        problem_solving TEXT,
        communication TEXT,
        recommendations TEXT NOT NULL,
        FOREIGN KEY(student_id) REFERENCES students(id)
    );

    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        career TEXT NOT NULL,
        created_at TEXT NOT NULL,
        UNIQUE(student_id, career),
        FOREIGN KEY(student_id) REFERENCES students(id)
    );

    CREATE TABLE IF NOT EXISTS cvs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER UNIQUE NOT NULL,
        phone TEXT DEFAULT '',
        email TEXT DEFAULT '',
        location TEXT DEFAULT '',
        summary TEXT DEFAULT '',
        education TEXT DEFAULT '',
        skills TEXT DEFAULT '',
        projects TEXT DEFAULT '',
        certifications TEXT DEFAULT '',
        experience TEXT DEFAULT '',
        updated_at TEXT NOT NULL,
        FOREIGN KEY(student_id) REFERENCES students(id)
    );
    """)
    conn.commit()
    conn.close()


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def get_or_create_student(name):
    name = (name or "Student").strip()
    conn = get_connection()
    student = conn.execute("SELECT * FROM students WHERE name = ?", (name,)).fetchone()

    if student is None:
        conn.execute(
            "INSERT INTO students (name, created_at) VALUES (?, ?)",
            (name, now())
        )
        conn.commit()
        student = conn.execute(
            "SELECT * FROM students WHERE name = ?", (name,)
        ).fetchone()

    conn.close()
    return student


def get_student(student_id):
    conn = get_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (student_id,)
    ).fetchone()
    conn.close()
    return student


def update_profile(student_id, education, interests, skills):
    conn = get_connection()
    conn.execute(
        "UPDATE students SET education=?, interests=?, skills=? WHERE id=?",
        (education, interests, skills, student_id)
    )
    conn.commit()
    conn.close()


def save_assessment(student_id, data, recommendations):
    conn = get_connection()
    cursor = conn.execute(
        """INSERT INTO assessments
        (student_id, created_at, interest, career_goal, academic_performance,
         programming, problem_solving, communication, recommendations)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            student_id,
            now(),
            data["interest"],
            data["career_goal"],
            data["academic_performance"],
            data["programming"],
            data["problem_solving"],
            data["communication"],
            json.dumps(recommendations)
        )
    )
    conn.commit()
    assessment_id = cursor.lastrowid
    conn.close()
    return assessment_id


def get_assessments(student_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM assessments WHERE student_id=? ORDER BY id DESC",
        (student_id,)
    ).fetchall()
    conn.close()
    return rows


def get_assessment(student_id, assessment_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM assessments WHERE id=? AND student_id=?",
        (assessment_id, student_id)
    ).fetchone()
    conn.close()
    return row


def parse_recommendations(row):
    return json.loads(row["recommendations"]) if row else []


def toggle_favorite(student_id, career):
    conn = get_connection()
    existing = conn.execute(
        "SELECT id FROM favorites WHERE student_id=? AND career=?",
        (student_id, career)
    ).fetchone()

    if existing:
        conn.execute("DELETE FROM favorites WHERE id=?", (existing["id"],))
        saved = False
    else:
        conn.execute(
            "INSERT OR IGNORE INTO favorites (student_id, career, created_at) VALUES (?, ?, ?)",
            (student_id, career, now())
        )
        saved = True

    conn.commit()
    conn.close()
    return saved


def get_favorites(student_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM favorites WHERE student_id=? ORDER BY id DESC",
        (student_id,)
    ).fetchall()
    conn.close()
    return rows


def is_favorite(student_id, career):
    conn = get_connection()
    row = conn.execute(
        "SELECT id FROM favorites WHERE student_id=? AND career=?",
        (student_id, career)
    ).fetchone()
    conn.close()
    return row is not None


def get_cv(student_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM cvs WHERE student_id=?", (student_id,)
    ).fetchone()
    conn.close()
    return row


def save_cv(student_id, data):
    conn = get_connection()
    existing = conn.execute(
        "SELECT id FROM cvs WHERE student_id=?", (student_id,)
    ).fetchone()

    values = (
        data.get("phone", ""),
        data.get("email", ""),
        data.get("location", ""),
        data.get("summary", ""),
        data.get("education", ""),
        data.get("skills", ""),
        data.get("projects", ""),
        data.get("certifications", ""),
        data.get("experience", ""),
        now(),
    )

    if existing:
        conn.execute(
            """UPDATE cvs SET phone=?, email=?, location=?, summary=?, education=?,
            skills=?, projects=?, certifications=?, experience=?, updated_at=?
            WHERE student_id=?""",
            values + (student_id,)
        )
    else:
        conn.execute(
            """INSERT INTO cvs
            (student_id, phone, email, location, summary, education, skills,
             projects, certifications, experience, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (student_id,) + values
        )

    conn.commit()
    conn.close()
