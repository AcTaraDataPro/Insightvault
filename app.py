import streamlit as st
import pandas as pd

try:
    from openai import OpenAI

    def create_client(key: str):
        return OpenAI(api_key=key)
except Exception:  # fallback for openai<1.0
    import openai

    def create_client(key: str):
        openai.api_key = key
        return openai

st.set_page_config(page_title="InsightVault", layout="wide")

SAMPLE_DATA = "sample_data.csv"

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
    st.subheader("📂 Select Data Source")
    source = st.radio("Choose data source", ["Upload CSV", "Use sample data"])

    df = None
    if source == "Upload CSV":
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv(SAMPLE_DATA)

    if df is not None:
        st.write("✅ Data Preview:")
        st.dataframe(df.head())

        query = st.text_input("🔍 Search data")
        if query:
            results = df[df.astype(str).apply(lambda row: row.str.contains(query, case=False, na=False).any(), axis=1)]
            st.write(f"Results: {len(results)} row(s)")
            st.dataframe(results)

        # AI summary
        st.subheader("🤖 AI Summary")
        openai_key = st.text_input("Enter your OpenAI API Key:", type="password")
        if openai_key and st.button("Generate AI Insight"):
            client = create_client(openai_key)
            with st.spinner("Generating insight..."):
                try:
                    summary = df.describe(include='all').to_string()
                    if len(summary) > 1000:
                        summary = summary[:1000]
                    prompt = (
                        "Analyze this dataset and summarize any patterns, trends, "
                        f"or insights:\n{summary}"
                    )

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
