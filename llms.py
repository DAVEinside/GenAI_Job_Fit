from langchain_openai import ChatOpenAI
import os 


from dotenv import load_dotenv
import os

from dotenv import load_dotenv
import os
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


def load_llm(): #gpt-4-0125-preview  gpt-4-turbo-2024-04-09
    llm = ChatOpenAI(model_name="gpt-4-0125-preview", openai_api_key=openai_api_key, temperature = 0.1, streaming=True) # type: ignore
    return llm
    