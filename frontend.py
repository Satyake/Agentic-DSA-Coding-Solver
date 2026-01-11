import streamlit as st
from agent-be import team
st.title("AlgoGenie- The Agentic DSA Problem Solver [LOCAL]")
st.write("Welcome to AlgoGenie, your personal DSA problem solver!, you can ask for code and run it locally!")

task=st.text_input("Enter your DSA problem")
if st.button("Run"):
    st.write("Running the task...")

