import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="InsightVault", layout="wide")

st.title("🔐 InsightVault: Your AI-Powered Data Vault")

# Sidebar login form
with st.sidebar:
    st.header("User Login")
    user_email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if user_email and password:
        st.success(f"Welcome, {user_email}!")
    else:
        st.warning("Please log in to continue.")

# Check user session
if user_email and password:
    st.subheader("📂 Upload Your Data (CSV)")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("✅ Data Preview:")
        st.dataframe(df.head())

        # AI summary
        st.subheader("🤖 AI Summary")
        openai_key = st.text_input("Enter your OpenAI API Key:", type="password")
        if openai_key:
            client = OpenAI(api_key=openai_key)
            if st.button("Generate AI Insight"):
                try:
                    summary = df.describe(include='all').to_string()
                    prompt = f"Analyze this user-uploaded dataset and summarize any patterns, trends, or insights:\n{summary}"

                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful data analyst."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    st.success("🧠 Insight:")
                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"OpenAI error: {str(e)}")
else:
    st.info("Login required to access the vault.")
