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

            OneHotEncoder(
                handle_unknown="ignore"
            ),

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
# 7. TRAIN MODEL
# ==========================================

pipeline.fit(
    X_train,
    y_train
)


# ==========================================
# 8. MODEL ACCURACY
# ==========================================

predictions = pipeline.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)


print("--------------------------------")
print("Career Recommendation ML Model")
print("--------------------------------")

print(
    "Model Accuracy:",
    round(accuracy * 100, 2),
    "%"
)


# ==========================================
# 9. TOP 3 CAREER PREDICTION
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

        "academic_performance": [
            academic_performance
        ],

        "programming": [
            programming
        ],

        "problem_solving": [
            problem_solving
        ],

        "communication": [
            communication
        ]

    })


    # Get probability for each career

    probabilities = pipeline.predict_proba(
        student
    )[0]


    # Get career names

    career_names = pipeline.classes_


    # Combine careers with probabilities

    career_scores = list(
        zip(
            career_names,
            probabilities
        )
    )


    # Sort from highest probability
    # to lowest probability

    career_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )


    # Take the top 3 careers

    top_three = career_scores[:3]


    recommendations = []


    if top_three:

        highest_score = top_three[0][1]


        for index, (career, probability) in enumerate(
            top_three
        ):

            # Compare each career with
            # the strongest recommendation

            if highest_score > 0:

                relative_score = (
                    probability / highest_score
                ) * 100

            else:

                relative_score = 0


            # Create a user-friendly
            # compatibility score

            if index == 0:

                score = round(
                    85 + (relative_score * 0.10)
                )

            else:

                score = round(
                    60 + (relative_score * 0.25)
                )


            # Keep score between 55 and 95

            score = min(score, 95)

            score = max(score, 55)


            recommendations.append({

                "career": career,

                "score": score

            })


    return recommendations
# ==========================================
# We keep this function so that the
# project remains compatible with any
# older code.

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


    return recommendations[0]["career"]


# ==========================================
# 11. TEST MODEL
# ==========================================

if __name__ == "__main__":

    results = predict_careers(

        "Artificial Intelligence",

        "Technical career",

        "High",

        "Advanced",

        "Advanced",

        "Intermediate"

    )


    print("\nTop Career Recommendations:")

    for result in results:

        print(
            result["career"],
            "-",
            result["score"],
            "%"
        )