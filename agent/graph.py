import os

from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

load_dotenv()

# LangSmith tracing for LangChain/LangGraph runs (including Groq-backed calls).
os.environ.setdefault("LANGSMITH_TRACING", "true")
os.environ.setdefault("LANGSMITH_PROJECT", "ai-agent")

from langchain_groq import ChatGroq # type: ignore
from prompts import *
from states import *
from tools import *
from langgraph.constants import END # type: ignore
from langgraph.graph import StateGraph # type: ignore

llm=ChatGroq(model="openai/gpt-oss-120b")

# planner agent
def planner_agent(state: dict) -> dict:
    user_prompt = state["user_prompt"]  # user prompt fetched from state
    resp = llm.with_structured_output(Plan, method="json_mode").invoke(
        planner_prompt(user_prompt),
        config={"run_name": "planner_llm", "tags": ["planner", "groq"]},
    )
    if resp is None:
        raise ValueError("Planner did not return a valid response")
    return {"plan": resp}

def architect_agent(state: dict) -> dict:
    plan: Plan = state["plan"] # type the o/p we are getting from state as Plan class
    resp = llm.with_structured_output(TaskPlan, method="json_mode").invoke(
        architect_prompt(plan.model_dump_json(indent=2)),
        config={"run_name": "architect_llm", "tags": ["architect", "groq"]},
    )
    if resp is None:
        raise ValueError("Architect did not return a valid response")
    resp.plan=plan
    return {"task_plan":resp}

def coder_agent(state: dict) -> dict:
    steps = state["task_plan"].implementation_steps
    current_step_idx = 0
    current_task = steps[current_step_idx]
    existing_content = read_file.run(current_task.filepath)
    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n"
        "Use write_file(path, content) to save your changes."
    )
    system_prompt = coder_system_prompt()
    coder_tools=[read_file, write_file, get_current_directory, list_files, run_cmd]
    react_agent=create_react_agent(llm, coder_tools)
    react_agent.invoke({"messages": [{"role": "system", "content": system_prompt},
                                     {"role": "user", "content": user_prompt}]})
    return {}

graph=StateGraph(dict)
graph.add_node("planner",planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder",coder_agent)
graph.add_edge("planner","architect")
graph.add_edge("architect","coder")
graph.set_entry_point("planner")
agent=graph.compile()

if __name__ == "__main__":
    user_prompt = "create a simple calculator web application"

    res = agent.invoke(
        {"user_prompt": user_prompt},
        config={"run_name": "planning_graph_run", "tags": ["langgraph", "planning"]},
    )
    print(res)