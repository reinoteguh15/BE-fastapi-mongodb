from fastapi import FastAPI
from pydantic import BaseModel, Field
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client["tutorial"]
collections = db["users"]

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=50)
    age: int = Field(..., gt=17, lt=100)
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