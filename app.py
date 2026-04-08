import streamlit as st
import time
from models.knowledge_ai import get_answer
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Medicaps AI", layout="wide")

# ================= CUSTOM CSS =================
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: white;
}

h1, h2, h3 {
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #020617;
}

.stButton>button {
    background-color: #1e3a8a;
    color: white;
    border-radius: 8px;
}

.stChatMessage {
    background-color: #020617;
    border-radius: 10px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
col_logo, col_title = st.columns([1, 5])

with col_logo:
    st.image("assets/logo.png", width=100)

with col_title:
    st.title("🎓 Medicaps AI Assistant")
    st.caption("Built by Vinit • Trinovous")

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "analytics" not in st.session_state:
    st.session_state.analytics = []

if "categories" not in st.session_state:
    st.session_state.categories = []

# ================= SIDEBAR =================
with st.sidebar:
    st.header("🕘 Query History")

    if st.session_state.messages:
        for msg in reversed(st.session_state.messages):
            if msg["role"] == "user":
                st.write("•", msg["content"])
    else:
        st.write("No queries yet")

# ================= ANALYTICS =================
col1, col2 = st.columns(2)

col1.metric("📊 Total Questions", len(st.session_state.analytics))

if st.session_state.categories:
    most_common = pd.Series(st.session_state.categories).value_counts().idxmax()
else:
    most_common = "None"

col2.metric("🔥 Most Asked", most_common)

st.divider()

# ================= QUICK BUTTONS =================
colA, colB, colC = st.columns(3)

quick_question = None

if colA.button("Attendance"):
    quick_question = "attendance rule"

if colB.button("Hostel"):
    quick_question = "hostel timing"

if colC.button("Leave"):
    quick_question = "leave procedure"

st.divider()

# ================= CHAT =================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ================= INPUT =================
user_input = st.chat_input("Ask anything about Medicaps rules...")

if quick_question:
    question = quick_question
elif user_input:
    question = user_input
else:
    question = None

# ================= RESPONSE =================
if question:

    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        placeholder = st.empty()
        placeholder.markdown("Thinking...")

        time.sleep(1)

        answer = get_answer(question)

        placeholder.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        st.session_state.analytics.append(datetime.now())

        if "Category:" in answer:
            cat = answer.split("Category:")[1].split("\n")[0].strip()
            st.session_state.categories.append(cat)

# ================= CLEAR =================
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ================= FOOTER =================
st.markdown("""
---
💡 Built for Medicaps students — No PDFs. Just ask.
""")