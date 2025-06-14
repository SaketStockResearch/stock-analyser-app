import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI

# Init OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📊 Stock Report & Earnings Transcript Analyzer")

# Upload PDF file
uploaded_file = st.file_uploader("Upload Earnings Transcript or Quarterly Report (PDF)", type="pdf")

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def generate_gpt_summary(text):
    if not text or len(text.strip()) == 0:
        return "No text found in the document."

    prompt = f"""
    You are a financial analyst assistant. Read the following earnings call transcript and extract key information:

    1. Summary of Management Commentary
    2. Key financial metrics (Revenue, EPS, Guidance)
    3. Notable changes from previous quarter
    4. Any identified risks or opportunities
    5. Overall sentiment (positive/neutral/negative)

    Transcript:
    {text[:4000]}  # Limit to avoid token overflow
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

if uploaded_file:
    st.success("File uploaded successfully.")
    text = extract_text_from_pdf(uploaded_file)

    if st.button("🧠 Generate GPT Summary"):
        with st.spinner("Generating summary..."):
            summary = generate_gpt_summary(text)
            st.subheader("📝 GPT-Generated Summary")
            st.write(summary)
