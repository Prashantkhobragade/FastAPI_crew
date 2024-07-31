from dotenv import load_dotenv
import os

from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
import requests
import json

from tools.tools import delete_item


load_dotenv()

#Groq API key
try:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("Groq api key is not found")
except:
    print("Error: Groq API key is not found")

# llm
llm = ChatGroq(
    model = "llama3-groq-8b-8192-tool-use-preview",
    temperature = 0.0,
    api_key = GROQ_API_KEY
)


#Agent
data_deletion_agent = Agent(
    role = "Data Deletion",
    goal = "Delete the data from FAST API based on the given {item_number}, if {item_number} not available return No Item Found.",
    backstory = "you are expert in deleting data from the API ",
    tools = [delete_item],
    llm = llm,
    #max_iter=15,  # Optional
    #max_rpm=2,  #optional
    allow_delegation = False,
    verbose = True

)

#task
data_deletion_task = Task(
    description = "delete data from the API when item_number {item_number} is given",
    expected_output = "Return confirmation of deleted data",
    agent = data_deletion_agent
)

#crew
crew_deletion = Crew(
    agents = [data_deletion_agent],
    tasks = [data_deletion_task],
    verbose = True
)


item_number = int(input("enter item_number: "))
if item_number is not None:
    result_data_deletion = crew_deletion.kickoff(inputs = {"item_number":item_number})
else:
    print("provide valid item_number")