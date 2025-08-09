"""
Agent Factory for Dynamic Lead Generation

Reusable agent creation pattern for LangChain agents with OpenAI.
"""

from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_agent(
    llm: ChatOpenAI,
    tools: list,
    system_prompt: str,
) -> AgentExecutor:
    """Create a function-calling agent and add it to the graph."""
    system_prompt += ("\nWork autonomously according to your specialty, using the tools available to you."
    " Do not ask for clarification."
    " Your other team members (and other teams) will collaborate with you with their own specialties."
    " You are chosen for a reason!")
    
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
    
    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor

def create_llm(model: str = "gpt-4o-mini", temperature: float = 0.7) -> ChatOpenAI:
    """Create a ChatOpenAI instance with default settings"""
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=os.getenv('OPENAI_API_KEY')
    )