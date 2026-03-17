from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "university_rules.txt")

if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

# load knowledge text
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# split rules
chunks = [c.strip() for c in text.split("\n") if c.strip()]

# convert chunks to embeddings
chunk_embeddings = model.encode(chunks)


#category ke liye keywords

categories = {
    "Attendance": ["attendance", "class", "lecture"],
    "Hostel": ["hostel", "gate", "warden", "room"],
    "Exam": ["exam", "test", "invigilator"],
    "Library": ["library", "book"],
    "Mess": ["mess", "canteen", "food"],
    "Discipline": ["discipline", "misconduct", "behavior"],
    "Procedure": ["procedure", "apply", "application", "process"]
}


def detect_category(question):

    question = question.lower()

    for category, keywords in categories.items():
        for word in keywords:
            if word in question:
                return category

    return "General"


#Main search function

def get_answer(question):

    question = question.strip().lower()

    category = detect_category(question)

    # embedding search
    question_embedding = model.encode([question])

    similarity = cosine_similarity(question_embedding, chunk_embeddings)[0]

    # get top 3
    top_indices = np.argsort(similarity)[-2:][::-1]

    results = []

    for idx in top_indices:

        score = similarity[idx]

        if score >= 0.30:  #Threshold vinit

            rule = chunks[idx]

            results.append(
                f"Category: {category}\n\n"
                f"{rule}\n"
                #f"Confidence: {round(score,2)}"
            )

    if not results:
        return """
Sorry, I couldn't find a relevant university rule.

Try asking:
• attendance rule
• hostel gate timing
• leave procedure
• library rules
"""

    return "\n\n".join(results)