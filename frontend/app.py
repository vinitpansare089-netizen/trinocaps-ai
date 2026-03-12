import streamlit as st
import requests
import time

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

    # show user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # typing effect
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("AI is thinking...")

        try:
            response = requests.get(
                "http://127.0.0.1:8000/ask",
                params={"question": question}
            )

            answer = response.json()["answer"]

            time.sleep(1)

            message_placeholder.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except:
            message_placeholder.markdown(
                "Backend server is not running."
            )

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.markdown("""
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
""", unsafe_allow_html=True)