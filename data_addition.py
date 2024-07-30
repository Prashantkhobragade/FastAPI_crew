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
data_manager_agent = Agent(
    role="Data Manager",
    goal="Efficiently manage data by saving {data} through API interactions with appropriate endpoints.",
    backstory = "A meticulous data manager skilled in handling data storage using FAST API. Responsible for ensuring accurate and efficient data transactions.",
    tools=[save_item],
    llm = llm,
    max_iter=15,  # Optional
    max_rpm=2, # Optional
    #max_execution_time=, # Optional
    allow_delegation = False,
    verbose=True
)


#Task
data_manager_task = Task(
    description='Manage given JSON {data} by saving it through the correct API endpoints and ensuring its accurate storage.',
    expected_output='Return confirmation of saved data, and if requested, retrieve and return the stored data in JSON format.',
    agent=data_manager_agent
)

#crew
crew_data  = Crew(
    agents=[data_manager_agent],
    tasks=[data_manager_task],
    #process = Process.sequential,
    verbose=True
)

user_input = input("Enter data: ")

data = None
    
try:
    data = json.loads(user_input)
    print("Received valid JSON data:", data)
except json.JSONDecodeError:
    print("Invalid JSON data. Please try again.")

if data is not None:
    result_data_addition = crew_data.kickoff(inputs = {"data": data})
else:
    print("No valid data")
