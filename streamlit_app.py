import streamlit as st
import requests

st.set_page_config(page_title="E-commerce Data Assistant", layout="centered")

st.title("🛍️ E-commerce Data Q&A")

question = st.text_input("Ask your question:", placeholder="e.g., What is the total sales?")

if st.button("Submit") and question:
    try:
        response = requests.post("http://127.0.0.1:5000/ask", json={"question": question})
        data = response.json()
        if "results" in data:
            st.success("Query Executed Successfully ✅")
            st.code(data.get("query", ""), language="sql")
            st.dataframe(data["results"])
        else:
            st.error(f"❌ Error: {data.get('error')}")
            st.code(data.get("query", ""), language="sql")
    except Exception as e:
        st.error(f"Request failed: {e}")