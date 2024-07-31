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


@tool("get item by item number")
def get_by_item_number(item_number:str) -> dict:
    """
    Retrieve item details from the API based on the item number.

    Args:
        item_number (str): The item number of the desired item.

    Returns:
        dict: The JSON response containing the item's details.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the request (e.g., network problems, invalid URL).
        ValueError: If the response contains invalid JSON or the item is not found.
    """
    url = f"{BASE_URL}/items/{item_number}"
    response = requests.get(url)
    return response.json()


@tool("delete data by item number")
def delete_item(item_number):
    """
    Deletes an item by its item number from the specified endpoint.

    Args:
        item_number (str): The unique identifier for the item to be deleted.

    Returns:
        dict: A dictionary containing the response message and status:
            - If the item is successfully deleted, returns the JSON response from the server.
            - If the item is not found (HTTP 404), returns a message indicating the item was not found.
            - If an error occurs, returns a message indicating an error occurred along with the HTTP status code.

    Example:
        >>> delete_item("12345")
        {'message': 'Item not found'}
    """
    url = f"{BASE_URL}/items/{item_number}"
    response = requests.delete(url)
    
    if response.status_code == 404:
        return {"message": "Item not found"}
    elif response.status_code == 200:
        return response.json()
    else:
        return {"message": "An error occurred", "status_code": response.status_code}
