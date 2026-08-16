from flask import Flask, render_template, request

from model import predict_careers


app = Flask(__name__)


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    return render_template("index.html")


# =========================
# ASSESSMENT PAGE
# =========================

@app.route("/assessment", methods=["GET", "POST"])
def assessment():

    if request.method == "POST":

        # Get information from the form

        name = request.form.get("name")

        interest = request.form.get("interest")

        career_goal = request.form.get("goal")

        academic_performance = request.form.get(
            "academic_performance"
        )

        programming = request.form.get(
            "programming"
        )

        problem_solving = request.form.get(
            "problem_solving"
        )

        communication = request.form.get(
            "communication"
        )


        # =========================
        # GET TOP 3 RECOMMENDATIONS
        # =========================

        recommendations = predict_careers(

            interest,
            career_goal,
            academic_performance,
            programming,
            problem_solving,
            communication

        )


        # =========================
        # SHOW RESULT
        # =========================

        return render_template(

            "result.html",

            name=name,

            recommendations=recommendations,

            interest=interest,

            career_goal=career_goal,

            academic_performance=academic_performance,

            programming=programming,

            problem_solving=problem_solving,

            communication=communication

        )


    return render_template("assessment.html")


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(debug=True)