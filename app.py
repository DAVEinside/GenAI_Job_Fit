import streamlit as st
from io import BytesIO
import os
from agents import define_graph
from llms import load_llm 
from langchain_core.messages import HumanMessage
from tools_1 import *
from agents import *

from dotenv import load_dotenv
import os
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


st.set_page_config(layout="wide")
st.title("Job_Fit_AI")
uploaded_file = st.sidebar.file_uploader("Upload Your CV", type="pdf")

job_description = st.text_area("Enter the job description")


if uploaded_file is not None:
    temp_dir = "tmp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    bytes_data = uploaded_file.getvalue()
    predefined_name = "cv.pdf"
    
    # To save the file, we use the 'with' statement to open a file and write the contents
    # The file will be saved with the predefined name in the /temp folder
    file_path = os.path.join(temp_dir, predefined_name)
    with open(file_path, "wb") as f:
        f.write(bytes_data)



if st.button("Generate"):
    if uploaded_file and job_description:
        
        llm = load_llm()


        graph = define_graph(llm)

        resume_text = extract_text_from_pdf(uploaded_file)

        initial_state = {"resume": resume_text,"job_description": job_description,"messages": []}

        agent_outputs = get_agent_outputs(initial_state,graph)

        resume_text_modified, cover_letter_text = get_resume_and_coverletter_text_modified(agent_outputs)


        resume_messages = resume_text_modified.get('messages', [])
        cover_letter_messages = cover_letter_text.get('messages', [])

        resume_text_content = [extract_text_from_human_message(msg) for msg in resume_messages if isinstance(msg, HumanMessage)]
        cover_letter_text_content = [extract_text_from_human_message(msg) for msg in cover_letter_messages if isinstance(msg, HumanMessage)]

        resume_text_final = '\n'.join(resume_text_content) if resume_text_content else "No content found"
        cover_letter_text_final = '\n'.join(cover_letter_text_content) if cover_letter_text_content else "No content found"



        # Generate Word documents
        resume_doc = save_text_to_docx(resume_text_final, "Tailored Resume")
        cover_letter_doc = save_text_to_docx(cover_letter_text_final, "Cover Letter")

        # Create BytesIO objects for download
        resume_file = BytesIO()
        cover_letter_file = BytesIO()
        resume_doc.save(resume_file)
        cover_letter_doc.save(cover_letter_file)
        resume_file.seek(0)
        cover_letter_file.seek(0)

        st.subheader("Tailored Resume")
        st.write(resume_text_final)
        st.download_button(
            label="Download Tailored Resume",
            data=resume_file,
            file_name="Tailored_Resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        st.subheader("Cover Letter")
        st.write(cover_letter_text_final)
        st.download_button(
            label="Download Cover Letter",
            data=cover_letter_file,
            file_name="Cover_Letter.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.error("Please upload a resume and enter the job description.")