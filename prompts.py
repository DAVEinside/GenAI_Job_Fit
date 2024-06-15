from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def routing_prompt(options, members):

    system_prompt = get_system_prompt()

    prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
    (
        "system",  "Given the conversation above, who should act next?" \
            " Or is the task complete and should we FINISH?  Select one of: {options}",
    ),
    ]
).partial(options=str(options), members=", ".join(members))

    return prompt


def get_system_prompt():

    SYSTEM_PROMPT = "You are a supervisor tasked with managing a conversation between the"
    " following workers:  {members}. User will provide a Job description"
    "and his Resume and wants a edited resume with keywords included based "
    "on the provided Job Description and a presonalizer Cover Letter Beased"
    "on Job Description and Resume. Given the above sequence of events ,"
    " respond with the worker to act next, when finished "
    " respond with FINISH."

    return SYSTEM_PROMPT

def get_keyword_generator_agent_prompt():
    keyword_agent = "You are an ATS software. Extract relevant keywords and skills from the following job description."
    "Respond with a list of keywords separated by commas."              
    return keyword_agent

def get_resume_generator_agent_prompt():
    resume_agent = "You are a resume enhancement assistant. Your task is to enhance the user's resume by integrating relevant keywords and skills."
    " Ensure that the keywords are added naturally and improve the overall quality of the resume,do not use any tools provided just mofidy the resume as instructed, in your response Just provide the final resume and do not write anything else."
    return resume_agent

def get_coverletter_generator_agent_prompt():
    coverletter_agent = "You are a cover letter generator. Your task is to generate a personalized cover letter based on the job description and the enhanced resume."
    " Highlight the candidate's suitability for the job by emphasizing the skills and experiences mentioned in the resume and job description, in your response just provide the final cover letter."
    return coverletter_agent




