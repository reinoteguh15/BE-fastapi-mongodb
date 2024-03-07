from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client["tutorial"]
collections = db["users"]

class User(BaseModel):
    username: str
    email: str
    age: int
    is_active: bool = True

app = FastAPI()

@app.post("/user")
def create_user(user: User):
    collections.insert_one(user.dict())
    return user

@app.get("/user")
def get_all_users():
    users = list(collections.find())
    for user in users:
        user["_id"] = str(user["_id"])
    return users