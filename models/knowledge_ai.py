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

# simple category keywords
categories = {
    "attendance": ["attendance", "class", "lecture"],
    "hostel": ["hostel", "gate", "warden", "room"],
    "mess": ["mess", "food", "canteen"],
    "exam": ["exam", "examination", "test", "marks"],
    "discipline": ["discipline", "misconduct", "behavior"],
}


def detect_category(question):
    question = question.lower()

    for category, keywords in categories.items():
        for word in keywords:
            if word in question:
                return category

    return None


def get_answer(question):

    question = question.strip().lower()

    # detect category
    category = detect_category(question)

    filtered_chunks = chunks
    filtered_embeddings = chunk_embeddings

    if category:
        filtered_chunks = [
            c for c in chunks if category in c.lower()
        ]

        if filtered_chunks:
            filtered_embeddings = model.encode(filtered_chunks)

    # embedding search
    question_embedding = model.encode([question])

    similarity = cosine_similarity(question_embedding, filtered_embeddings)[0]

    # top 3 results
    top_indices = np.argsort(similarity)[-3:][::-1]

    results = []

    for idx in top_indices:
        score = similarity[idx]

        if score >= 0.45:
            results.append(
                f"📂 Category: {category if category else 'general'}\n"
                f"{filtered_chunks[idx]}\n"
                f"Confidence: {round(score,2)}"
            )

    if not results:
        return "Sorry, I couldn't find a relevant university rule for that question."

    return "\n\n".join(results)