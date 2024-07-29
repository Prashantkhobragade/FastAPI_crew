import requests
from crewai_tools import tool


BASE_URL = "http://localhost:8000"

@tool("save item")
def save_item(item_number:int, item_name:str, value:int)-> dict:
    """
    Saves an item to a remote server via a POST request.

    Args:
        item_number (int): The unique identifier for the item.
        item_name (str): The name of the item.
        value (float): The value or price of the item.

    Returns:
        dict: The JSON response from the server, parsed into a Python dictionary.
    """
    url = f"{BASE_URL}/items/"
    data = {"item_number": item_number, "item_name": item_name, "value": value}
    response = requests.post(url, json=data)
    return response.json()