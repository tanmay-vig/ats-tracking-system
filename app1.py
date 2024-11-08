
import streamlit as st
import os
import google.generativeai as genai
from PyPDF2 import PdfReader

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Response from model 
def model_response(prompt , text , jd):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt , text , jd])
    return response.text

def input_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    
    # Loop through each page in the PDF
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        # Append the extracted text from each page
        text += page.extract_text() or ""  # Adds empty string if extract_text() returns None
    
    return text



## Prompt Template
input_prompt="""
Hey Act Like a skilled or very experience ATS (Application Tracking System)
with a deep understanding of tech field,software engineering, data science,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job descriptiom
You must consider the job market is very competitive and you should provide
best assistance for improving thd resumes. Assign the percentage Matching based

Give ats score and tell how can to improve it
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume", type="pdf",help="Please uplaod the pdf")


submit = st.button("Submit")
if uploaded_file is not None:
    text = input_pdf_text(uploaded_file)
    response = model_response(input_prompt , text , jd)
    st.subheader(response)
