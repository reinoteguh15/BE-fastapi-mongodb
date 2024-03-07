from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    age: int
    is_active: bool = True

app = FastAPI()

@app.post("/user")
def create_user(user: User):
    return user