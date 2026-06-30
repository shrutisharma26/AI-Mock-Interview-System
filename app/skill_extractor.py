import re

SKILLS = [
    "python",
    "c++",
    "java",
    "sql",
    "machine learning",
    "deep learning",
    "data science",
    "nlp",
    "pandas",
    "numpy",
    "matplotlib",
    "streamlit",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "flask",
    "fastapi",
    "git",
    "github",
    "docker",
    "aws",
    "react",
    "javascript",
    "html",
    "css",
    "dsa"
]


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found_skills.append(skill)

    return list(set(found_skills))