from fastapi import FastAPI, HTTPException
from random import randint

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/random/{min_value}/{max_value}")
def get_random_number(min_value: int, max_value: int):
    if min_value >= max_value:
        raise HTTPException(status_code=400, detail="min_value should be less than max_value")
    return {"random_number": randint(min_value, max_value)}

@app.get("/random-item")
def get_random_item():
    items = ["apple", "banana", "cherry", "date", "elderberry"]
    return {"random_item": items[randint(0, len(items) + 1)]}