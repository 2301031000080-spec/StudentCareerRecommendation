from flask import Flask, render_template, request

from model import predict_careers


app = Flask(__name__)


# =========================
# LEARNING RESOURCES
# =========================

RESOURCE_CATALOG = {

    "Machine Learning Engineer": {
        "courses": [
            {"name": "Coursera – Machine Learning Specialization", "url": "https://www.coursera.org/specializations/machine-learning"},
            {"name": "IBM SkillsBuild – AI & Machine Learning", "url": "https://skillsbuild.org/"},
            {"name": "AWS Skill Builder – Machine Learning", "url": "https://skillbuilder.aws/"}
        ],
        "videos": [
            {"name": "Machine Learning with Python & Scikit-learn – practical full course", "url": "https://www.youtube.com/watch?v=hDKCxebp88A"}
        ],
        "skills": ["Python", "Statistics", "Machine Learning", "Scikit-learn", "Model Deployment"],
        "project": "Build an ML prediction system using a real dataset and deploy it as a web application."
    },

    "Data Scientist": {
        "courses": [
            {"name": "Coursera – Machine Learning Specialization", "url": "https://www.coursera.org/specializations/machine-learning"},
            {"name": "IBM SkillsBuild – Data & Analytics", "url": "https://skillsbuild.org/"},
            {"name": "AWS Skill Builder – Data & Machine Learning", "url": "https://skillbuilder.aws/"}
        ],
        "videos": [
            {"name": "Practical Machine Learning with Python – projects and real-world datasets", "url": "https://www.youtube.com/watch?v=hDKCxebp88A"}
        ],
        "skills": ["Python", "SQL", "Statistics", "Data Visualization", "Machine Learning"],
        "project": "Analyze a real-world dataset, create visualizations, build a prediction model and explain the findings."
    },

    "AI Engineer": {
        "courses": [
            {"name": "Coursera – IBM AI Engineering", "url": "https://www.coursera.org/browse/computer-science/machine-learning"},
            {"name": "IBM SkillsBuild – Artificial Intelligence", "url": "https://skillsbuild.org/"},
            {"name": "AWS Skill Builder – AI & Machine Learning", "url": "https://skillbuilder.aws/"}
        ],
        "videos": [
            {"name": "Practical AI / Machine Learning project with Python", "url": "https://www.youtube.com/watch?v=hDKCxebp88A"}
        ],
        "skills": ["Python", "AI", "Machine Learning", "Deep Learning", "APIs"],
        "project": "Build an AI-powered application that solves a practical problem and expose it through an API."
    },

    "AI Researcher": {
        "courses": [
            {"name": "Coursera – Machine Learning Specialization", "url": "https://www.coursera.org/specializations/machine-learning"},
            {"name": "IBM SkillsBuild – AI Learning", "url": "https://skillsbuild.org/"}
        ],
        "videos": [
            {"name": "Machine Learning concepts and practical project workflow", "url": "https://www.youtube.com/watch?v=hDKCxebp88A"}
        ],
        "skills": ["Python", "Mathematics", "Statistics", "Deep Learning", "Research"],
        "project": "Reproduce a small ML experiment using a public dataset and compare multiple approaches."
    },

    "Data Analyst": {
        "courses": [
            {"name": "Coursera – Data Science & Analytics courses", "url": "https://www.coursera.org/browse/data-science"},
            {"name": "IBM SkillsBuild – Data & Analytics", "url": "https://skillsbuild.org/"}
        ],
        "videos": [
            {"name": "Practical data analysis and machine learning workflow", "url": "https://www.youtube.com/watch?v=hDKCxebp88A"}
        ],
        "skills": ["Excel", "SQL", "Python", "Power BI", "Statistics"],
        "project": "Take a public dataset, clean it, build a dashboard and present business insights from the data."
    },

    "Web Developer": {
        "courses": [
            {"name": "Coursera – Web Development courses", "url": "https://www.coursera.org/browse/computer-science/web-development"},
            {"name": "IBM SkillsBuild – Software Development", "url": "https://skillsbuild.org/"}
        ],
        "videos": [
            {"name": "Practical web development project tutorials", "url": "https://www.youtube.com/results?search_query=web+development+real+world+project+tutorial"}
        ],
        "skills": ["HTML", "CSS", "JavaScript", "Git", "Responsive Design"],
        "project": "Build and deploy a responsive portfolio or small business website from scratch."
    },

    "Full Stack Developer": {
        "courses": [
            {"name": "Coursera – Full Stack / Web Development", "url": "https://www.coursera.org/browse/computer-science/web-development"},
            {"name": "IBM SkillsBuild – Software Development", "url": "https://skillsbuild.org/"}
        ],
        "videos": [
            {"name": "Full-stack real-world project tutorials", "url": "https://www.youtube.com/results?search_query=full+stack+web+development+real+world+project"}
        ],
        "skills": ["HTML/CSS", "JavaScript", "React", "Backend", "Databases"],
        "project": "Build a complete web application with frontend, backend, database and deployment."
    },

    "Cyber Security Analyst": {
        "courses": [
            {"name": "Coursera – Cybersecurity courses", "url": "https://www.coursera.org/browse/information-technology/cybersecurity"},
            {"name": "IBM SkillsBuild – Cybersecurity", "url": "https://skillsbuild.org/"},
            {"name": "AWS Skill Builder – Security learning", "url": "https://skillbuilder.aws/"}
        ],
        "videos": [
            {"name": "Practical cybersecurity labs and projects", "url": "https://www.youtube.com/results?search_query=cybersecurity+practical+lab+real+world+project"}
        ],
        "skills": ["Networking", "Linux", "Cybersecurity", "Python", "Security Tools"],
        "project": "Create a safe local security lab and practice log analysis, network monitoring and defensive techniques."
    },

    "Security Researcher": {
        "courses": [
            {"name": "Coursera – Cybersecurity courses", "url": "https://www.coursera.org/browse/information-technology/cybersecurity"},
            {"name": "IBM SkillsBuild – Cybersecurity", "url": "https://skillsbuild.org/"}
        ],
        "videos": [
            {"name": "Practical cybersecurity research and lab tutorials", "url": "https://www.youtube.com/results?search_query=cybersecurity+research+lab+tutorial"}
        ],
        "skills": ["Cybersecurity", "Networking", "Linux", "Research", "Cryptography"],
        "project": "Study a public vulnerability case, reproduce it only in a safe lab, and document defensive lessons."
    },

    "Security Engineer": {
        "courses": [
            {"name": "Coursera – Cybersecurity courses", "url": "https://www.coursera.org/browse/information-technology/cybersecurity"},
            {"name": "AWS Skill Builder – Security", "url": "https://skillbuilder.aws/"},
            {"name": "IBM SkillsBuild – Cybersecurity", "url": "https://skillsbuild.org/"}
        ],
        "videos": [
            {"name": "Practical cloud and cybersecurity engineering projects", "url": "https://www.youtube.com/results?search_query=cloud+security+engineering+real+world+project"}
        ],
        "skills": ["Networking", "Linux", "Cloud Security", "Python", "Security Tools"],
        "project": "Design a secure cloud architecture for a small application and document its security controls."
    },

    "Mobile App Developer": {
        "courses": [
            {"name": "Coursera – Mobile App Development", "url": "https://www.coursera.org/browse/computer-science/mobile-development"},
            {"name": "IBM SkillsBuild – Software Development", "url": "https://skillsbuild.org/"}
        ],
        "videos": [
            {"name": "Mobile app development real-world project tutorials", "url": "https://www.youtube.com/results?search_query=mobile+app+development+real+world+project+tutorial"}
        ],
        "skills": ["Flutter", "Android", "Java/Kotlin", "UI Design", "APIs"],
        "project": "Build and deploy a small mobile app that solves a real student or community problem."
    },

    "Accountant": {
        "courses": [
            {"name": "Coursera – Accounting courses", "url": "https://www.coursera.org/browse/business/accounting"}
        ],
        "videos": [
            {"name": "Practical accounting and bookkeeping projects", "url": "https://www.youtube.com/results?search_query=accounting+bookkeeping+real+world+project"}
        ],
        "skills": ["Accounting", "Excel", "Financial Statements", "Tax Basics", "Attention to Detail"],
        "project": "Create a sample business ledger, prepare financial statements and analyze monthly transactions."
    },

    "Financial Analyst": {
        "courses": [
            {"name": "Coursera – Finance & Financial Analysis", "url": "https://www.coursera.org/browse/business/finance"}
        ],
        "videos": [
            {"name": "Practical financial analysis and Excel projects", "url": "https://www.youtube.com/results?search_query=financial+analysis+real+world+project+excel"}
        ],
        "skills": ["Excel", "Financial Modeling", "Statistics", "Data Analysis", "Communication"],
        "project": "Build a financial model for a sample company and create a data-backed investment report."
    },

    "Investment Analyst": {
        "courses": [
            {"name": "Coursera – Investment & Finance", "url": "https://www.coursera.org/browse/business/finance"}
        ],
        "videos": [
            {"name": "Practical investment analysis projects", "url": "https://www.youtube.com/results?search_query=investment+analysis+practical+project"}
        ],
        "skills": ["Financial Analysis", "Excel", "Valuation", "Research", "Risk Analysis"],
        "project": "Analyze a public company's financial reports and create a structured investment research report."
    },

    "Banking Professional": {
        "courses": [
            {"name": "Coursera – Banking & Finance", "url": "https://www.coursera.org/browse/business/finance"}
        ],
        "videos": [
            {"name": "Practical banking and finance concepts", "url": "https://www.youtube.com/results?search_query=banking+finance+practical+career+tutorial"}
        ],
        "skills": ["Finance", "Excel", "Customer Service", "Risk Awareness", "Communication"],
        "project": "Prepare a sample loan analysis and customer financial profile using fictional data."
    },

    "Chartered Accountant": {
        "courses": [
            {"name": "Coursera – Accounting & Finance", "url": "https://www.coursera.org/browse/business/accounting"}
        ],
        "videos": [
            {"name": "Practical accounting and financial reporting tutorials", "url": "https://www.youtube.com/results?search_query=chartered+accountancy+practical+accounting+tutorial"}
        ],
        "skills": ["Accounting", "Auditing", "Taxation", "Financial Reporting", "Excel"],
        "project": "Prepare a fictional company's accounts and practice basic audit and financial reporting workflows."
    },

    "Business Analyst": {
        "courses": [
            {"name": "Coursera – Business Analysis", "url": "https://www.coursera.org/browse/business/business-strategy"}
        ],
        "videos": [
            {"name": "Business analyst real-world case study projects", "url": "https://www.youtube.com/results?search_query=business+analyst+real+world+case+study+project"}
        ],
        "skills": ["Requirements Analysis", "Excel", "SQL", "Communication", "Problem Solving"],
        "project": "Analyze a fictional business problem, gather requirements and propose a data-backed solution."
    },

    "Financial Planner": {
        "courses": [
            {"name": "Coursera – Personal Finance", "url": "https://www.coursera.org/browse/business/finance"}
        ],
        "videos": [
            {"name": "Practical personal finance planning examples", "url": "https://www.youtube.com/results?search_query=personal+financial+planning+real+world+example"}
        ],
        "skills": ["Budgeting", "Financial Planning", "Excel", "Communication", "Risk Awareness"],
        "project": "Create a fictional five-year financial plan including budgeting, savings and investment assumptions."
    },

    "Digital Marketing Specialist": {
        "courses": [
            {"name": "Coursera – Digital Marketing", "url": "https://www.coursera.org/browse/business/marketing"}
        ],
        "videos": [
            {"name": "Real-world digital marketing campaign projects", "url": "https://www.youtube.com/results?search_query=digital+marketing+real+world+campaign+project"}
        ],
        "skills": ["SEO", "Content", "Analytics", "Social Media", "Communication"],
        "project": "Create a small digital campaign, define a target audience and measure sample campaign metrics."
    }
}


def get_learning_resources(career):
    """Return career-specific learning resources with a safe generic fallback."""
    return RESOURCE_CATALOG.get(
        career,
        {
            "courses": [
                {"name": "Coursera – Explore relevant courses", "url": "https://www.coursera.org/"},
                {"name": "IBM SkillsBuild – Career learning", "url": "https://skillsbuild.org/"}
            ],
            "videos": [
                {"name": f"Practical {career} tutorials and projects", "url": f"https://www.youtube.com/results?search_query={career.replace(' ', '+')}+real+world+project"}
            ],
            "skills": ["Communication", "Problem Solving", "Digital Skills"],
            "project": f"Complete a beginner-friendly practical project related to {career}."
        }
    )


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

        name = request.form.get("name")
        interest = request.form.get("interest")
        career_goal = request.form.get("goal")
        academic_performance = request.form.get("academic_performance")
        programming = request.form.get("programming")
        problem_solving = request.form.get("problem_solving")
        communication = request.form.get("communication")

        recommendations = predict_careers(
            interest,
            career_goal,
            academic_performance,
            programming,
            problem_solving,
            communication
        )

        top_career = recommendations[0]["career"] if recommendations else ""
        learning_resources = get_learning_resources(top_career)

        return render_template(
            "result.html",
            name=name,
            recommendations=recommendations,
            interest=interest,
            career_goal=career_goal,
            academic_performance=academic_performance,
            programming=programming,
            problem_solving=problem_solving,
            communication=communication,
            learning_resources=learning_resources
        )

    return render_template("assessment.html")


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(debug=True)