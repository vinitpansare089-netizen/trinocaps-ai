from fastapi import FastAPI
from models.knowledge_ai import get_answer

app = FastAPI()

@app.get("/")
def home():
    return {"CampusAI backend is running"}

@app.get("/test-ai")
def test_ai(): 
    return {"ai_module": "working"}

@app.get("/ask")
def ask(question: str):
    answer = get_answer(question)
    return {"answer": answer}