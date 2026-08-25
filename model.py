# ==========================================
# STUDENT CAREER RECOMMENDATION SYSTEM
# Machine Learning Model
# ==========================================

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


# ==========================================
# 1. LOAD DATASET
# ==========================================

data = pd.read_csv("career_data.csv")


# ==========================================
# 2. INPUT FEATURES
# ==========================================

features = [
    "interest",
    "career_goal",
    "academic_performance",
    "programming",
    "problem_solving",
    "communication"
]

X = data[features]
y = data["career"]


# ==========================================
# 3. PREPROCESSING
# ==========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            features
        )
    ]
)


# ==========================================
# 4. MACHINE LEARNING MODEL
# ==========================================

model = DecisionTreeClassifier(
    max_depth=6,
    random_state=42
)


# ==========================================
# 5. PIPELINE
# ==========================================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ==========================================
# 6. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ==========================================
# 7. MODEL EVALUATION
# ==========================================

evaluation_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", DecisionTreeClassifier(
            max_depth=6,
            random_state=42
        ))
    ]
)

evaluation_pipeline.fit(X_train, y_train)
predictions = evaluation_pipeline.predict(X_test)

accuracy = accuracy_score(y_test, predictions)


# ==========================================
# 8. FINAL MODEL
# ==========================================

pipeline.fit(X, y)

print("--------------------------------")
print("Career Recommendation ML Model")
print("--------------------------------")
print("Model Accuracy:", round(accuracy * 100, 2), "%")
print("Career Categories:", len(pipeline.classes_))


# ==========================================
# 9. CAREER-FIELD RESTRICTIONS
# ==========================================
# The ML model calculates probabilities for all careers.
# For a career recommendation system, however, the selected
# field must be respected. A Medical & Healthcare student
# should not receive an AI Engineer recommendation simply
# because some profile values happen to look similar.
#
# These groups restrict the final Top 3 to careers that belong
# to the student's selected professional field.

CAREER_GROUPS = {
    "Artificial Intelligence": [
        "Machine Learning Engineer", "AI Researcher", "AI Engineer", "Data Scientist"
    ],
    "Machine Learning": [
        "Machine Learning Engineer", "AI Researcher", "Data Scientist", "AI Engineer"
    ],
    "Data Science": [
        "Data Scientist", "Data Analyst", "Research Analyst"
    ],
    "Web Development": [
        "Web Developer", "UI UX Developer", "Full Stack Developer"
    ],
    "Cyber Security": [
        "Cyber Security Analyst", "Security Researcher", "Security Engineer"
    ],
    "App Development": [
        "Mobile App Developer", "UI UX Developer"
    ],
    "Commerce & Finance": [
        "Accountant", "Financial Analyst", "Investment Analyst",
        "Banking Professional", "Chartered Accountant", "Business Analyst",
        "Financial Planner", "Digital Marketing Specialist"
    ],
    "Medical & Healthcare": [
        "Doctor", "Pharmacist", "Physiotherapist", "Nurse",
        "Medical Laboratory Technologist", "Healthcare Administrator", "Dietitian"
    ],
    "Law & Public Services": [
        "Lawyer", "Legal Advisor", "Civil Services Officer",
        "Public Policy Analyst", "Government Administrative Officer"
    ],
    "Management & Business": [
        "Business Manager", "Marketing Manager", "Human Resources Manager",
        "Operations Manager", "Project Manager", "Entrepreneur",
        "Digital Marketing Specialist"
    ],
    "Science & Research": [
        "Research Scientist", "Biotechnologist", "Environmental Scientist",
        "Research Analyst", "Laboratory Researcher"
    ],
    "Engineering & Technology": [
        "Mechanical Engineer", "Civil Engineer", "Electrical Engineer",
        "Electronics Engineer", "Chemical Engineer", "Robotics Engineer"
    ],
    "Education": [
        "School Teacher", "College Lecturer", "Academic Researcher",
        "Educational Consultant"
    ]
}


# ==========================================
# 10. TOP 3 CAREER PREDICTION
# ==========================================

def predict_careers(
    interest,
    career_goal,
    academic_performance,
    programming,
    problem_solving,
    communication
):

    student = pd.DataFrame({
        "interest": [interest],
        "career_goal": [career_goal],
        "academic_performance": [academic_performance],
        "programming": [programming],
        "problem_solving": [problem_solving],
        "communication": [communication]
    })

    probabilities = pipeline.predict_proba(student)[0]
    career_names = pipeline.classes_

    career_scores = list(zip(career_names, probabilities))

    # Keep only careers belonging to the selected professional field.
    allowed_careers = CAREER_GROUPS.get(interest)

    if allowed_careers:
        career_scores = [
            item for item in career_scores
            if item[0] in allowed_careers
        ]

    career_scores.sort(key=lambda x: x[1], reverse=True)
    top_three = career_scores[:3]

    recommendations = []

    if top_three:
        highest_score = top_three[0][1]

        for index, (career, probability) in enumerate(top_three):

            if highest_score > 0:
                relative_score = (probability / highest_score) * 100
            else:
                relative_score = 0

            if index == 0:
                score = round(85 + (relative_score * 0.10))
            else:
                score = round(60 + (relative_score * 0.25))

            score = min(score, 95)
            score = max(score, 55)

            recommendations.append({
                "career": career,
                "score": score
            })

    return recommendations


# ==========================================
# 11. COMPATIBILITY FUNCTION
# ==========================================

def predict_career(
    interest,
    career_goal,
    academic_performance,
    programming,
    problem_solving,
    communication
):

    recommendations = predict_careers(
        interest,
        career_goal,
        academic_performance,
        programming,
        problem_solving,
        communication
    )

    return recommendations[0]["career"] if recommendations else "No suitable career found"


# ==========================================
# 12. TEST MODEL
# ==========================================

if __name__ == "__main__":

    test_profiles = [
        (
            "Artificial Intelligence", "Technical career", "High",
            "Advanced", "Advanced", "Intermediate"
        ),
        (
            "Commerce & Finance", "High salary", "High",
            "Beginner", "Advanced", "Advanced"
        ),
        (
            "Medical & Healthcare", "Stable career", "High",
            "Beginner", "Advanced", "Advanced"
        )
    ]

    for profile in test_profiles:
        results = predict_careers(*profile)
        print("\nTop Career Recommendations:")
        for result in results:
            print(result["career"], "-", result["score"], "%")
