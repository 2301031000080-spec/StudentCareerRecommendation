import os
from flask import Flask, render_template, request, redirect, url_for, session, abort

from model import predict_careers
from database import (
    init_db, get_or_create_student, get_student, update_profile,
    save_assessment, get_assessments, get_assessment, parse_recommendations,
    toggle_favorite, get_favorites, is_favorite, get_cv, save_cv
)
from resources_data import get_learning_resources

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-demo-key")

init_db()


def current_student():
    student_id = session.get("student_id")
    return get_student(student_id) if student_id else None


def require_student():
    student = current_student()
    if not student:
        return redirect(url_for("assessment"))
    return student


def render_result(assessment_row):
    recommendations = parse_recommendations(assessment_row)
    top_career = recommendations[0]["career"] if recommendations else ""
    student = current_student()

    return render_template(
        "result.html",
        name=student["name"],
        recommendations=recommendations,
        interest=assessment_row["interest"],
        career_goal=assessment_row["career_goal"],
        academic_performance=assessment_row["academic_performance"],
        programming=assessment_row["programming"],
        problem_solving=assessment_row["problem_solving"],
        communication=assessment_row["communication"],
        learning_resources=get_learning_resources(top_career),
        assessment_id=assessment_row["id"],
        favorite=is_favorite(student["id"], top_career)
    )


@app.route("/")
def home():
    return render_template("index.html", student=current_student())


@app.route("/assessment", methods=["GET", "POST"])
def assessment():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        student = get_or_create_student(name)
        session["student_id"] = student["id"]

        data = {
            "interest": request.form.get("interest", ""),
            "career_goal": request.form.get("goal", ""),
            "academic_performance": request.form.get("academic_performance", ""),
            "programming": request.form.get("programming", ""),
            "problem_solving": request.form.get("problem_solving", ""),
            "communication": request.form.get("communication", "")
        }

        recommendations = predict_careers(
            data["interest"], data["career_goal"],
            data["academic_performance"], data["programming"],
            data["problem_solving"], data["communication"]
        )

        assessment_id = save_assessment(student["id"], data, recommendations)
        return redirect(url_for("assessment_result", assessment_id=assessment_id))

    return render_template("assessment.html", student=current_student())


@app.route("/result/<int:assessment_id>")
def assessment_result(assessment_id):
    student = require_student()
    if not hasattr(student, "__getitem__"):
        return student
    row = get_assessment(student["id"], assessment_id)
    if not row:
        abort(404)
    return render_result(row)


@app.route("/history")
def history():
    student = require_student()
    if not hasattr(student, "__getitem__"):
        return student

    items = []
    for row in get_assessments(student["id"]):
        recs = parse_recommendations(row)
        items.append({
            "id": row["id"],
            "date": row["created_at"],
            "interest": row["interest"],
            "goal": row["career_goal"],
            "top_career": recs[0]["career"] if recs else "No result",
            "score": recs[0]["score"] if recs else 0
        })

    return render_template("history.html", student=student, history=items)


@app.route("/compare")
def compare():
    student = require_student()
    if not hasattr(student, "__getitem__"):
        return student

    rows = get_assessments(student["id"])
    first_id = request.args.get("first", type=int)
    second_id = request.args.get("second", type=int)
    first = get_assessment(student["id"], first_id) if first_id else None
    second = get_assessment(student["id"], second_id) if second_id else None

    comparison = None
    if first and second:
        first_recs = parse_recommendations(first)
        second_recs = parse_recommendations(second)
        a = {item["career"]: item["score"] for item in first_recs}
        b = {item["career"]: item["score"] for item in second_recs}
        careers = list(dict.fromkeys(list(a) + list(b)))
        comparison = {
            "first": first,
            "second": second,
            "first_recs": first_recs,
            "second_recs": second_recs,
            "careers": [
                {
                    "career": career,
                    "first_score": a.get(career, 0),
                    "second_score": b.get(career, 0),
                    "change": b.get(career, 0) - a.get(career, 0)
                }
                for career in careers
            ]
        }

    return render_template("compare.html", student=student, assessments=rows, comparison=comparison)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    student = require_student()
    if not hasattr(student, "__getitem__"):
        return student

    if request.method == "POST":
        update_profile(
            student["id"],
            request.form.get("education", "").strip(),
            request.form.get("interests", "").strip(),
            request.form.get("skills", "").strip()
        )
        return redirect(url_for("profile"))

    return render_template("profile.html", student=get_student(student["id"]))


@app.route("/favorites")
def favorites():
    student = require_student()
    if not hasattr(student, "__getitem__"):
        return student
    return render_template("favorites.html", student=student, favorites=get_favorites(student["id"]))


@app.route("/favorite/<path:career>", methods=["POST"])
def favorite(career):
    student = require_student()
    if not hasattr(student, "__getitem__"):
        return student
    toggle_favorite(student["id"], career)
    return redirect(request.referrer or url_for("favorites"))


@app.route("/career/<path:career>")
def career_details(career):
    student = current_student()
    return render_template(
        "career_detail.html",
        student=student,
        career=career,
        learning_resources=get_learning_resources(career),
        favorite=is_favorite(student["id"], career) if student else False
    )


@app.route("/resume", methods=["GET", "POST"])
def resume():
    student = require_student()
    if not hasattr(student, "__getitem__"):
        return student

    if request.method == "POST":
        data = {
            key: request.form.get(key, "").strip()
            for key in [
                "phone", "email", "location", "summary", "education",
                "skills", "projects", "certifications", "experience"
            ]
        }
        save_cv(student["id"], data)
        return redirect(url_for("resume"))

    return render_template("resume.html", student=student, cv=get_cv(student["id"]))


@app.route("/resume/preview")
def resume_preview():
    student = require_student()
    if not hasattr(student, "__getitem__"):
        return student

    cv = get_cv(student["id"])
    if not cv:
        return redirect(url_for("resume"))
    return render_template("resume_preview.html", student=student, cv=cv)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
