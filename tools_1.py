from ast import List
from langchain.agents import tool
import PyPDF2
import asyncio
from langchain.pydantic_v1 import BaseModel, Field
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from docx import Document

def tavily():
    tavily_tool = TavilySearchResults(max_results=5)
    return tavily_tool



def get_job_description():
    return input("""
    Enter the job description:

    """)

def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

def get_agent_outputs(initial_state,graph):
    agent_outputs = []
    for s in graph.stream(
        {
            "messages": [HumanMessage(content=initial_state["resume"], name="resume"),
                        HumanMessage(content=initial_state["job_description"], name="job_description")
                        ]
        }
):
        if "__end__" not in s:
            agent_outputs.append(s)
    return agent_outputs

def get_resume_and_coverletter_text_modified(agent_outputs):
    resume_text = []
    cover_letter_text = []
    for output in agent_outputs:

        if 'Resume Editor' in output:
            resume_text.append(output['Resume Editor'])


        elif 'CoverLetter Generator' in output:
            cover_letter_text.append(output['CoverLetter Generator'])




    resume_text = resume_text[-1]
    cover_letter_text = cover_letter_text[-1]

    return resume_text, cover_letter_text


def save_text_to_docx(text, filename):
    doc = Document()
    for line in text.split('\n'):
        doc.add_paragraph(line)
    return doc

# Function to extract text from HumanMessage content
def extract_text_from_human_message(message):
    if isinstance(message.content, str):
        return message.content
    elif isinstance(message.content, list):
        extracted_text = []
        for item in message.content:
            if isinstance(item, str):
                extracted_text.append(item)
            elif isinstance(item, dict) and 'content' in item:
                extracted_text.append(item['content'])
        return '\n'.join(extracted_text)
    return ""
