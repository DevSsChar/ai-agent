from dotenv import load_dotenv
from pydantic import BaseModel, Field
load_dotenv()
from langchain_groq import ChatGroq
from prompts import *
from states import *
from langgraph.constants import END
from langgraph.graph import StateGraph

llm=ChatGroq(model="openai/gpt-oss-120b")

# planner agent
def planner_agent(state: dict) -> dict:
    user_prompt = state["user_prompt"]  # user prompt fetched from state
    resp = llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))
    return {"plan": resp}

graph=StateGraph(dict)
graph.add_node("planner",planner_agent)
graph.set_entry_point("planner")
agent=graph.compile()

user_prompt="create a simple calculator web application"

res = agent.invoke({"user_prompt": user_prompt})
print(res)