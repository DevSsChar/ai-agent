import os

from dotenv import load_dotenv

load_dotenv()

# LangSmith tracing for LangChain/LangGraph runs (including Groq-backed calls).
os.environ.setdefault("LANGSMITH_TRACING", "true")
os.environ.setdefault("LANGSMITH_PROJECT", "ai-agent")

from langchain_groq import ChatGroq # type: ignore
from agent.prompts import *
from agent.states import *
from agent.tools import *
from langgraph.constants import END # type: ignore
from langgraph.graph import StateGraph # type: ignore

llm=ChatGroq(model="openai/gpt-oss-120b")
init_project_root()

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
    coder_state=state.get("coder_state")
    if coder_state is None:
        coder_state=CoderState(task_plan=state["task_plan"], current_step_idx=0, current_file_content=None)
    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}
    current_step_idx = coder_state.current_step_idx
    current_task = steps[current_step_idx]
    file_path = normalize_project_path(current_task.filepath)
    existing_content = read_file.run(file_path)
    system_prompt = coder_system_prompt()
    user_prompt = coder_user_prompt(
        current_task.task_description,
        file_path,
        existing_content,
    )
    resp = llm.with_structured_output(FileContent, method="json_mode").invoke(
        f"{system_prompt}\n\n{user_prompt}",
        config={"run_name": "coder_llm", "tags": ["coder", "groq"]},
    )
    if resp is None or not resp.content:
        raise ValueError(f"Coder did not return valid content for {file_path}")
    write_file.invoke({"path": file_path, "content": resp.content})
    coder_state.current_file_content = resp.content
    coder_state.current_step_idx += 1
    return {"coder_state": coder_state, "status": "IN_PROGRESS"}

graph=StateGraph(dict)
graph.add_node("planner",planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder",coder_agent)
graph.add_edge("planner","architect")
graph.add_edge("architect","coder")
graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"}
)
graph.set_entry_point("planner")
agent=graph.compile()

if __name__ == "__main__":
    user_prompt = "create a simple calculator web application"

    res = agent.invoke(
        {"user_prompt": user_prompt},
        config={"run_name": "planning_graph_run", "tags": ["langgraph", "planning"]},
    )
    print(res)