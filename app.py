import streamlit as st
import time
from models.knowledge_ai import get_answer
import pandas as pd
from datetime import datetime

# suggestions = {
#     "Attendance": [
#         "What happens if attendance is below 75%?",
#         "How is attendance calculated?",
#         "Can attendance shortage be condoned?"
#     ],

#     "Hostel": [
#         "What are hostel gate timings?",
#         "Are guests allowed in hostel?",
#         "What are hostel discipline rules?"
#     ],

#     "Exam": [
#         "What happens if a student cheats in exam?",
#         "What items are allowed in exam hall?",
#         "What are exam misconduct rules?"
#     ],

#     "Library": [
#         "What are library timings?",
#         "How many books can a student borrow?",
#         "What happens if a library book is lost?"
#     ],

#     "Mess": [
#         "What are mess timings?",
#         "Can students skip mess subscription?",
#         "Are outside guests allowed in mess?"
#     ],

#     "General": [
#         "What are university discipline rules?",
#         "How to apply for leave?",
#         "What documents are needed for exams?"
#     ]
# }


st.title("🎓 TrinoCaps AI")
st.caption("Built by Vinit • MCA Student • Trinovous")

#Message ka session chalane ke liye
if "messages" not in st.session_state:
    st.session_state.messages = []

if "analytics" not in st.session_state:
    st.session_state.analytics = []

if "categories" not in st.session_state:
    st.session_state.categories = []

#side me query history ke liye
with st.sidebar:
    st.header("🕘 Query History")

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.write("•", msg["content"])

#Analytics ke liye 
st.subheader("📊 How students are using this")

col1, col2 = st.columns(2)

total_questions = len(st.session_state.analytics)
col1.metric("Total Questions Asked", total_questions)

if st.session_state.categories:
    cat_series = pd.Series(st.session_state.categories)
    most_common = cat_series.value_counts().idxmax()
else:
    most_common = "None"

col2.metric("Most Asked Category", most_common)

st.divider()

#Quick questions wala feature
st.subheader("Try these")

colA, colB, colC = st.columns(3)

quick_question = None

if colA.button("Attendance rule"):
    quick_question = "What is the attendance rule?"

if colB.button("Hostel gate timing"):
    quick_question = "When do hostel gates close?"

if colC.button("Leave procedure"):
    quick_question = "How to apply for leave?"

#chats ki history dikhane ke liye
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#chats ka input lega
user_input = st.chat_input("Ask about university rules")

if quick_question:
    question = quick_question
elif user_input:
    question = user_input
else:
    question = None

#questions ko process karega
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

        # analytics tracking
        st.session_state.analytics.append(datetime.now())

        if "Category:" in answer:
            cat = answer.split("Category:")[1].split("\n")[0].strip()
            st.session_state.categories.append(cat)

       #Trino ka understanding panel
        st.info(f"""
AI Understanding

Detected Category: {cat if 'cat' in locals() else 'General'}
Query: {question}
Retrieval Method: Semantic Search
""")

        #Follow up questions
        st.markdown("### Related Questions")

        c1, c2, c3 = st.columns(3)

        if c1.button("Exam rules"):
            st.session_state.messages.append(
                {"role": "user", "content": "What are exam rules?"}
            )

        if c2.button("Library rules"):
            st.session_state.messages.append(
                {"role": "user", "content": "What are library rules?"}
            )

        if c3.button("Hostel rules"):
            st.session_state.messages.append(
                {"role": "user", "content": "What are hostel rules?"}
            )

#sab kuch saaf.......
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Footer 
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

st.markdown("""
👋 Hey! I built this to make university rules simple.

No PDFs. No confusion. Just ask.
""")