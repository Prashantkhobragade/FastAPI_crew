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
    goal = "Accurately retrieve data based on the given {item_number} using the appropriate API endpoints.",
    backstory = "An expert in data retrieval, skilled in accessing and delivering accurate information from APIs. Responsible for ensuring data integrity and timely response.",
    tools = [get_by_item_number],
    llm = llm,
    #max_iter=15,  # Optional
    #max_rpm=4,  #optional
    allow_delegation = False,
    verbose = True
)

#task
data_retrival_task = Task(
    description = "Retrieve detailed data from the API using the provided {item_number}.",
    expected_output = "A dictionary containing all relevant details associated with {item_number}, including any metadata or additional information.",
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

