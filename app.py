import streamlit as st
import os
from PyPDF2 import PdfReader
import tempfile

st.set_page_config(page_title="Stock Research Assistant", layout="wide")

st.title("📊 Stock Earnings Transcript Analyzer")

st.markdown("""
Upload your earnings call transcripts or quarterly reports (PDF or TXT).  
We’ll extract and analyze them in the next step.
""")

uploaded_files = st.file_uploader("Upload Earnings Reports", type=['pdf', 'txt'], accept_multiple_files=True)

documents = {}

def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Store extracted documents in session state
if "documents" not in st.session_state:
    st.session_state.documents = {}

# Process uploaded files
if uploaded_files:
    for file in uploaded_files:
        if file.name not in st.session_state.documents:
            if file.type == "application/pdf":
                text = extract_text_from_pdf(file)
            else:
                text = file.read().decode("utf-8")
            st.session_state.documents[file.name] = text
    st.success(f"Uploaded {len(uploaded_files)} file(s).")

# Display uploaded files
st.subheader("Uploaded Files")
if st.session_state.documents:
    for filename, content in st.session_state.documents.items():
        with st.expander(filename):
            st.text_area("Extracted Text", value=content[:3000], height=300, disabled=True)
else:
    st.info("No documents uploaded yet.")
