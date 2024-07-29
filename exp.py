import json

user_input = input("Enter data: ")
    
try:
    data = json.loads(user_input)
    print("Received valid JSON data:", data)
except json.JSONDecodeError:
    print("Invalid JSON data. Please try again.")
