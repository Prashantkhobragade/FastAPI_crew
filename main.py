from dotenv import load_dotenv
import os

from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
import requests
import json


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
    model = "llama-3.1-8b-instant",
    temperature = 0.0,
    api_key = GROQ_API_KEY
)

BASE_URL = "http://localhost:8000"

#Agent
data_manager_agent = Agent(
    role="Data Manager",
    goal="save {data} through API interactions by hitting correct endpoint",
    backstory="An efficient data manager responsible for saving {data} in FAST API.",
    #tools=[requests],
    llm = llm,
    allow_delegation = False,
    verbose=True
)


#Task
data_manager_task = Task(
    description='add given json {data} by hitting correct endpoints',
    expected_output='return saved data in Json format',
    agent=data_manager_agent
)



#crew
crew  = Crew(
    agents=[data_manager_agent],
    tasks=[data_manager_task],
    #process = Process.sequential,
    verbose=True
)

user_input = input("Enter data: ")
    
try:
    data = json.loads(user_input)
    print("Received valid JSON data:", data)
except json.JSONDecodeError:
    print("Invalid JSON data. Please try again.")


result = crew.kickoff(inputs = {"data": data})