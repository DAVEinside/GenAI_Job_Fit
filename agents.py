from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
import operator
from typing import Annotated, Any, Dict, List, Optional, Sequence, TypedDict
import functools
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
import os
from tools_1 import *
from prompts import *



def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str):
    # Each worker node will be given a name and some tools.
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor

def agent_node(state, agent, name):
    result = agent.invoke(state)
    # Ensure name adheres to the pattern '^[a-zA-Z0-9_-]+$'
    clean_name = ''.join(e for e in name if e.isalnum() or e in ['_', '-'])
    return {"messages": [HumanMessage(content=result["output"], name=clean_name)]}


def define_graph(llm):
    members = ["KeyWord Generator", "Resume Editor","CoverLetter Generator"]
    system_prompt = (get_system_prompt())
    # Our team supervisor is an LLM node. It just picks the next agent to process
    # and decides when the work is completed
    options = ["FINISH"] + members
    # Using openai function calling can make output parsing easier for us
    function_def = {
    "name": "route",
    "description": "Select the next role.",
    "parameters": {
        "title": "routeSchema",
        "type": "object",
        "properties": {
            "next": {
                "title": "Next",
                "anyOf": [
                    {"enum": options},
                ],
            }
        },
        "required": ["next"],
    },
    }
    prompt = routing_prompt(options, members)


    supervisor_chain = (
        prompt
        | llm.bind_functions(functions=[function_def], function_call="route")
        | JsonOutputFunctionsParser()
    )

    KeyWord_Generator_agent = create_agent(llm,[tavily()],get_keyword_generator_agent_prompt())
    KeyWord_Generator_node = functools.partial(agent_node, agent=KeyWord_Generator_agent, name="KeyWord Generator")


    Resume_Editor_agent = create_agent(llm,[tavily()],get_resume_generator_agent_prompt())
    Resume_Editor_node = functools.partial(agent_node, agent=Resume_Editor_agent, name="Resume Editor")

    CoverLetter_Generator_agent = create_agent(llm,[tavily()],get_coverletter_generator_agent_prompt())
    CoverLetter_Generator_node = functools.partial(agent_node, agent=CoverLetter_Generator_agent, name="CoverLetter Generator")


    workflow = StateGraph(AgentState)
    workflow.add_node("KeyWord Generator", KeyWord_Generator_node)
    workflow.add_node("Resume Editor", Resume_Editor_node)
    workflow.add_node("CoverLetter Generator", CoverLetter_Generator_node)
    workflow.add_node("supervisor", supervisor_chain)

    # Add edges for the workflow
    workflow.add_edge("KeyWord Generator", "Resume Editor")
    workflow.add_edge("Resume Editor", "CoverLetter Generator")
    workflow.add_edge("CoverLetter Generator", "supervisor")

    for member in members:
        # We want our workers to ALWAYS "report back" to the supervisor when done
        workflow.add_edge(member, "supervisor")
    # The supervisor populates the "next" field in the graph state
    # which routes to a node or finishes
    conditional_map = {k: k for k in members}
    conditional_map["FINISH"] = END
    workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
# Finally, add entrypoint
    workflow.set_entry_point("supervisor")

    graph = workflow.compile()

    return graph

# The agent state is the input to each node in the graph
class AgentState(TypedDict):
    # The annotation tells the graph that new messages will always
    # be added to the current states
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # The 'next' field indicates where to route to next
    next: str


