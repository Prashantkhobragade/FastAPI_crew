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
    tools=[save_item],
    llm = llm,
    allow_delegation = False,
    verbose=True
)

data_retrival_agent = Agent(
    role = "Data Retrival",
    goal = "Retrive the data based on the given {item_number}",
    backstory = "you are expert in retriving data from the API ",
    tools = [get_by_item_number],
    llm = llm,
    allow_delegation = False,
    verbose = True
)




#Task
data_manager_task = Task(
    description='add given json {data} by hitting correct endpoints',
    expected_output='return saved data in Json format',
    agent=data_manager_agent
)

data_retrival_task = Task(
    description = "retrive data from the API when {item_number} is given",
    expected_output = "dict containing all the details related to {item_number}",
    agent = data_retrival_agent
)

def add_data():
    #crew for data store
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


def data_retrival():
#crew for data retrival
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


if __name__ == "__main__":
    #for adding ddata
    #data_add = add_data()

    #for data retrival
    retrival = data_retrival()