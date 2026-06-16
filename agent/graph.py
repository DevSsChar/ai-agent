from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

from langchain_groq import ChatGroq

class Schema(BaseModel):
    name: str
    age: int
llm=ChatGroq(model="openai/gpt-oss-120b")
resp=llm.with_structured_output(Schema).invoke("Extract name and age: Dev 20yrs old")
print(resp)