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

# split text into chunks
chunks = [c.strip() for c in text.split("\n") if c.strip()]

# convert chunks to embeddings
chunk_embeddings = model.encode(chunks)


def get_answer(question):

    question = question.strip().lower()

    for chunk in chunks:
        if question in chunk.lower():
            return chunk

    question_embedding = model.encode([question])

    similarity = cosine_similarity(question_embedding, chunk_embeddings)

    best_match_index = similarity.argmax()
    best_score = similarity[0][best_match_index]

    # confidence threshold
    if best_score < 0.45:
        return "Sorry, I couldn't find a relevant university rule for that question."

    return chunks[best_match_index]