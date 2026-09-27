# Career-specific resources grouped by professional domain.
# The links intentionally vary by field instead of showing the same
# engineering platforms to every student.

DOMAIN_RESOURCES = {
    "Technology & IT": {
        "courses": [
            ("Microsoft Learn", "https://learn.microsoft.com/training/"),
            ("freeCodeCamp", "https://www.freecodecamp.org/"),
            ("Coursera - Computer Science", "https://www.coursera.org/browse/computer-science")
        ],
        "skills": ["Programming", "Git", "Problem Solving", "Portfolio Building"],
        "project": "Build a practical application, publish the source code, and deploy a working demo."
    },
    "Commerce & Finance": {
        "courses": [
            ("ICAI - The Institute of Chartered Accountants of India", "https://www.icai.org/"),
            ("Tally Education", "https://tallyeducation.com/"),
            ("Coursera - Finance", "https://www.coursera.org/browse/business/finance")
        ],
        "skills": ["Excel", "Financial Analysis", "Accounting", "Communication"],
        "project": "Create a fictional company financial workbook with statements, ratios and a short business analysis."
    },
    "Medical & Healthcare": {
        "courses": [
            ("World Health Organization", "https://www.who.int/"),
            ("National Medical Commission", "https://www.nmc.org.in/"),
            ("Coursera - Healthcare", "https://www.coursera.org/browse/health")
        ],
        "skills": ["Medical Knowledge", "Communication", "Documentation", "Research"],
        "project": "Prepare a structured healthcare case-study portfolio using fictional or public educational data."
    },
    "Law & Public Services": {
        "courses": [
            ("eCourts Services", "https://ecourts.gov.in/"),
            ("UPSC", "https://upsc.gov.in/"),
            ("SWAYAM", "https://swayam.gov.in/")
        ],
        "skills": ["Legal Research", "Writing", "Public Policy", "Communication"],
        "project": "Write a short policy or legal case-study report with sources, arguments and a clear conclusion."
    },
    "Management & Business": {
        "courses": [
            ("PMI - Project Management Institute", "https://www.pmi.org/"),
            ("HubSpot Academy", "https://academy.hubspot.com/"),
            ("Coursera - Business", "https://www.coursera.org/browse/business")
        ],
        "skills": ["Communication", "Leadership", "Planning", "Business Analysis"],
        "project": "Create a business case for a small product or service, including target users, costs and marketing."
    },
    "Science & Research": {
        "courses": [
            ("Nature Masterclasses", "https://masterclasses.nature.com/"),
            ("Coursera - Physical and Life Sciences", "https://www.coursera.org/browse/physical-science-and-engineering"),
            ("SWAYAM", "https://swayam.gov.in/")
        ],
        "skills": ["Research Methodology", "Statistics", "Scientific Writing", "Data Analysis"],
        "project": "Choose a public dataset or published study and prepare a reproducible mini research report."
    },
    "Engineering & Technology": {
        "courses": [
            ("Autodesk Education", "https://www.autodesk.com/education/home"),
            ("MathWorks Learning", "https://www.mathworks.com/learn.html"),
            ("Coursera - Engineering", "https://www.coursera.org/browse/physical-science-and-engineering")
        ],
        "skills": ["Engineering Fundamentals", "CAD/Simulation", "Problem Solving", "Technical Documentation"],
        "project": "Design a small engineering solution, document the calculations or simulation, and present the result."
    },
    "Education": {
        "courses": [
            ("UNESCO Education", "https://www.unesco.org/en/education"),
            ("SWAYAM", "https://swayam.gov.in/"),
            ("Coursera - Education", "https://www.coursera.org/browse/social-sciences/education")
        ],
        "skills": ["Teaching", "Communication", "Lesson Planning", "Digital Learning"],
        "project": "Create a short lesson plan, learning activity and assessment for a real student audience."
    }
}

CAREER_DOMAIN = {}

for career in [
    "Machine Learning Engineer", "AI Researcher", "AI Engineer", "Data Scientist",
    "Data Analyst", "Web Developer", "UI UX Developer", "Full Stack Developer",
    "Cyber Security Analyst", "Security Researcher", "Security Engineer", "Mobile App Developer"
]:
    CAREER_DOMAIN[career] = "Technology & IT"

for career in [
    "Accountant", "Financial Analyst", "Investment Analyst", "Banking Professional",
    "Chartered Accountant", "Business Analyst", "Financial Planner", "Digital Marketing Specialist"
]:
    CAREER_DOMAIN[career] = "Commerce & Finance"

for career in [
    "Doctor", "Pharmacist", "Physiotherapist", "Nurse",
    "Medical Laboratory Technologist", "Healthcare Administrator", "Dietitian"
]:
    CAREER_DOMAIN[career] = "Medical & Healthcare"

for career in [
    "Lawyer", "Legal Advisor", "Civil Services Officer",
    "Public Policy Analyst", "Government Administrative Officer"
]:
    CAREER_DOMAIN[career] = "Law & Public Services"

for career in [
    "Business Manager", "Marketing Manager", "Human Resources Manager",
    "Operations Manager", "Project Manager", "Entrepreneur"
]:
    CAREER_DOMAIN[career] = "Management & Business"

for career in [
    "Research Scientist", "Biotechnologist", "Environmental Scientist",
    "Research Analyst", "Laboratory Researcher"
]:
    CAREER_DOMAIN[career] = "Science & Research"

for career in [
    "Mechanical Engineer", "Civil Engineer", "Electrical Engineer",
    "Electronics Engineer", "Chemical Engineer", "Robotics Engineer"
]:
    CAREER_DOMAIN[career] = "Engineering & Technology"

for career in [
    "School Teacher", "College Lecturer", "Academic Researcher",
    "Educational Consultant"
]:
    CAREER_DOMAIN[career] = "Education"


def get_learning_resources(career):
    domain = CAREER_DOMAIN.get(career, "Technology & IT")
    base = DOMAIN_RESOURCES[domain]

    practical_url = (
        "https://www.youtube.com/results?search_query="
        + career.replace(" ", "+")
        + "+practical+project"
    )

    return {
        "domain": domain,
        "courses": [
            {"name": name, "url": url}
            for name, url in base["courses"]
        ],
        "videos": [
            {"name": f"Practical {career} projects and tutorials", "url": practical_url}
        ],
        "skills": base["skills"],
        "project": base["project"]
    }
