from pydantic import BaseModel, Field


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
