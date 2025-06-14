import streamlit as st
import os
from openai import OpenAI
from PyPDF2 import PdfReader

st.set_page_config(page_title="Stock Transcript Analyzer", layout="wide")
st.title("📊 Stock Earnings Transcript Analyzer")

uploaded_files = st.file_uploader("Upload earnings transcripts (PDF or TXT)", type=['pdf', 'txt'], accept_multiple_files=True)

# Store uploaded files in session state
if "documents" not in st.session_state:
    st.session_state.documents = {}

def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_gpt_summary(text):
    prompt = f"""
    You are a financial analyst assistant. Read the following earnings call transcript and extract key information:

    1. Summary of Management Commentary
    2. Key financial metrics (Revenue, EPS, Guidance)
    3. Notable changes from previous quarter
    4. Any identified risks or opportunities
    5. Overall sentiment (positive/neutral/negative)

    Transcript:
    {text[:4000]}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


# Upload and extract
if uploaded_files:
    for file in uploaded_files:
        if file.name not in st.session_state.documents:
            if file.type == "application/pdf":
                text = extract_text_from_pdf(file)
            else:
                text = file.read().decode("utf-8")
            st.session_state.documents[file.name] = {"text": text, "summary": None}
    st.success("Files uploaded and extracted!")

# Display and summarize
st.subheader("📄 Uploaded Reports")
for filename, data in st.session_state.documents.items():
    with st.expander(f"{filename}"):
        st.text_area("Transcript Preview", value=data["text"][:2000], height=250, disabled=True)

        if data["summary"] is None:
            if st.button(f"🧠 Generate GPT Summary for {filename}"):
                with st.spinner("Generating summary..."):
                    summary = generate_gpt_summary(data["text"])
                    st.session_state.documents[filename]["summary"] = summary
                    st.success("Summary generated!")

        if data["summary"]:
            st.markdown("### 📌 GPT Summary")
            st.markdown(st.session_state.documents[filename]["summary"])
