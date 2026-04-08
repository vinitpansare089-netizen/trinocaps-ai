from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "university_rules.txt")

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

chunks = [c.strip() for c in text.split("\n") if c.strip()]
chunk_embeddings = model.encode(chunks)

categories = {
    "Attendance": ["attendance", "class", "lecture", "present", "absent"],
    "Hostel": ["hostel", "gate", "warden", "room", "entry"],
    "Exam": ["exam", "test", "cheating", "invigilator"],
    "Library": ["library", "book", "issue", "return"],
    "Mess": ["mess", "canteen", "food"],
    "Discipline": ["discipline", "misconduct", "behavior"],
    "Procedure": ["procedure", "apply", "application", "process", "leave"]
}

def detect_category(question):
    question = question.lower()

    for category, keywords in categories.items():
        for word in keywords:
            if word in question:
                return category

    return "General"

def get_answer(question):

    original_question = question
    question = question.lower()

    category = detect_category(question)

    question_embedding = model.encode([question])
    similarity = cosine_similarity(question_embedding, chunk_embeddings)[0]

    top_indices = np.argsort(similarity)[-3:][::-1]

    results = []

    for idx in top_indices:
        score = similarity[idx]

        if score >= 0.30:
            results.append(chunks[idx])

    if not results:
        return f"""
❌ No exact rule found.

Try asking:
• attendance rule  
• hostel timing  
• exam rules  
• leave procedure  
"""

    # Clean UI output
    formatted = f"📂 Category: {category}\n\n"

    for r in results:
        formatted += f"• {r}\n\n"

    return formatted