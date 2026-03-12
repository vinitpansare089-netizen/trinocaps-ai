import streamlit as st
import requests

st.title("Trinovous Campus AI Assistant")

tab1, tab2 = st.tabs(["Ask University Rules", "Resume Analyzer"])

with tab1:

    question = st.text_input("Ask a question about university rules")

    if st.button("Ask AI"):

      try:
        response = requests.get(
            "http://127.0.0.1:8000/ask",
            params={"question": question}
        )

        answer = response.json()["answer"]

        st.write("### AI Response")
        st.success(answer)
      except:
          st.error("Backend server is not running. Please start FastAPI.")