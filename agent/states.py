from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class File(BaseModel):
    path: str=Field(description="The path to be created or modified")
    purpose: str=Field(description="The purpose of the file, e.g, 'main application logic', 'data processing module', etc.")

class Plan(BaseModel):
    name: str
    description: str=Field(
        description="A online description of the app to be built, e.g, 'A web application for managing personal finance'"
    )
    techstack: str=Field(
        description="The tech stack to be used for the app, e.g, 'python', 'javascript', 'react', 'flask', etc"
    )
    features: list[str]=Field(
        description="A list of features that the app should have, e.g, 'user authentication', 'oauth login', 'admin access', 'role based authentication', etc."
    )
    files: list[str]=Field(
        description="A list of file to be created, each with a 'path' and 'purpose'"
    )

class ImplementationTask(BaseModel):
    filepath: str = Field(description="The path to the file to be modified")
    task_description: str = Field(description="A detailed description of the task to be performed on the file, e.g. 'add user authentication', 'implement data processing logic', etc.")

class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask] = Field(description="A list of steps to be taken to implement the task")
    # to allow additional elements in class, even though not defined here
    model_config = ConfigDict(extra="allow")

class FileContent(BaseModel):
    content: str = Field(description="The complete file content to write")

class CoderState(BaseModel):
    task_plan: TaskPlan = Field(description="The plan for the task to be implemented")
    current_step_idx: int = Field(0, description="The index of the current step in the implementation steps")
    current_file_content: Optional[str] = Field(None, description="The content of the file currently being edited or created")