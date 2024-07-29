from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Pydantic model for our item
class Item(BaseModel):
    item_number: int
    item_name: str
    value: float

# In-memory storage
items = []

@app.post("/items/")
async def create_item(item: Item):
    items.append(item)
    return {"message": "Item created successfully"}

@app.get("/items/", response_model=List[Item])
async def read_items():
    return items

@app.delete("/items/{item_number}")
async def delete_item(item_number: int):
    for index, item in enumerate(items):
        if item.item_number == item_number:
            items.pop(index)
            return {"message": f"Item with number {item_number} deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)