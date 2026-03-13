import streamlit as st
import time
from models.knowledge_ai import get_answer

st.title("TrinoCaps AI")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

st.header("Ask about Medicaps university rules...")

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input("Ask about university rules")

if question:

    # Show user message
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    # AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("AI is thinking...")

        time.sleep(1)

        answer = get_answer(question)

        message_placeholder.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

# Clear chat button
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