from dotenv import load_dotenv
import os

from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
import requests
import json

from tools.tools import save_item, get_by_item_number


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
data_retrival_agent = Agent(
    role = "Data Retrival",
    goal = "Retrieve the data from FAST API based on the given {item_number}",
    backstory = "you are expert in retrieving data from the API ",
    tools = [get_by_item_number],
    llm = llm,
    #max_iter=15,  # Optional
    #max_rpm=2,  #optional
    allow_delegation = False,
    verbose = True
)

#task
data_retrival_task = Task(
    description = "retrieve data from the API when item_number {item_number} is given",
    expected_output = "dict containing all the details related to {item_number}",
    agent = data_retrival_agent
)


#Crew
crew_retrival = Crew(
    agents = [data_retrival_agent],
    tasks = [data_retrival_task],
    verbose = True
)

item_number = int(input("enter item_number: "))
if item_number is not None:
    result_data_retrival = crew_retrival.kickoff(inputs = {"item_number":item_number})
else:
    print("provide valid item_number")

