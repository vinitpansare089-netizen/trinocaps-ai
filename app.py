import streamlit as st
import time
from models.knowledge_ai import get_answer
import pandas as pd
import altair as alt
from datetime import datetime

st.title("TrinoCaps AI")

# -----------------------------
# CHAT MEMORY
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# ANALYTICS MEMORY
# -----------------------------

if "analytics" not in st.session_state:
    st.session_state.analytics = []

if "categories" not in st.session_state:
    st.session_state.categories = []

st.header("Ask about Medicaps university rules...")

# -----------------------------
# DISPLAY OLD MESSAGES
# -----------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# QUICK QUESTIONS
# -----------------------------

st.subheader("Quick Questions")

col1, col2, col3 = st.columns(3)

quick_question = None

if col1.button("Attendance rule"):
    quick_question = "What is the attendance rule?"

if col2.button("Hostel gate timing"):
    quick_question = "When do hostel gates close?"

if col3.button("Leave procedure"):
    quick_question = "How to apply for leave?"

# -----------------------------
# CHAT INPUT
# -----------------------------

user_input = st.chat_input("Ask about university rules")

if quick_question:
    question = quick_question
elif user_input:
    question = user_input
else:
    question = None

# -----------------------------
# PROCESS QUESTION
# -----------------------------

if question:

    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        message_placeholder = st.empty()
        message_placeholder.markdown("Trino is thinking...")

        time.sleep(1)

        answer = get_answer(question)

        message_placeholder.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        # save analytics
        st.session_state.analytics.append(datetime.now())

        if "Category:" in answer:
            cat = answer.split("Category:")[1].split("\n")[0].strip()
            st.session_state.categories.append(cat)

# -----------------------------
# CLEAR CHAT
# -----------------------------

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# -----------------------------
# ANALYTICS PANEL
# -----------------------------

st.divider()
st.subheader("📊 TrinoCaps Analytics Panel")

# total questions
total_questions = len(st.session_state.analytics)
st.metric("Total Questions Asked", total_questions)

# most asked category
if st.session_state.categories:
    cat_series = pd.Series(st.session_state.categories)
    most_common = cat_series.value_counts().idxmax()
    st.metric("Most Asked Category", most_common)

# queries per hour chart
if st.session_state.analytics:

    df = pd.DataFrame({"time": st.session_state.analytics})
    df["hour"] = df["time"].dt.hour

    chart_data = df.groupby("hour").size().reset_index(name="queries")

    chart = alt.Chart(chart_data).mark_bar().encode(
        x="hour:O",
        y="queries:Q",
        tooltip=["hour", "queries"]
    )

    st.subheader("Queries in Last 24 Hours")

    st.altair_chart(chart, use_container_width=True)

# -----------------------------
# FOOTER
# -----------------------------

st.markdown(
"""
<style>
.corner-credit {
position: fixed;
bottom: 10px;
right: 15px;
font-size: 13px;
color: #9aa0a6;
background-color: transparent;
z-index: 100;
}
</style>

<div class="corner-credit">
TrinoCaps AI • Built by Vinit | Powered by Trinovous
</div>
""",
unsafe_allow_html=True
)