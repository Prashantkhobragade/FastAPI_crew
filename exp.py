"""
import json

user_input = input("Enter data: ")
    
try:
    data = json.loads(user_input)
    print("Received valid JSON data:", data)
except json.JSONDecodeError:
    print("Invalid JSON data. Please try again.")
"""
import requests

BASE_URL = "http://localhost:8000"
"""
def save_item(item_number:int, item_name:str, value:float):
    url = f"{BASE_URL}/items/"
    data = {"item_number": item_number, "item_name": item_name, "value": value}
    response = requests.post(url, json=data)
    return response.json()

result = save_item(item_number=111, item_name="fgbcvgf", value=898)
print(result)"""

def get_by_item_number(item_number:str):
    url = f"{BASE_URL}/items/{item_number}"
    response = requests.get(url)
    return response.json()

result = get_by_item_number(111)
print(result)
"""
"Efficiently manage data by saving {data} through API interactions with appropriate endpoints.",
"A meticulous data manager skilled in handling data storage using FAST API. Responsible for ensuring accurate and efficient data transactions.",
item_number = int(input("enter item_number: "))
print(item_number)
print(type(item_number))"""