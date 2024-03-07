from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["tutorial"]
collections = db["todo"]

app = FastAPI()

class ToDoModel(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    done: bool = False

@app.post("/todo")
def create_todo(todo: ToDoModel):
    todo = dict(todo)
    collections.insert_one(todo)
    todo["_id"] = str(todo["_id"])
    return todo

@app.get("/todo")
def get_all_todos():
    todos = list(collections.find())
    for todo in todos:
        todo["_id"] = str(todo["_id"])
    return todos

@app.get("/todo/{id}")
def get_todo_by_id(id: str):
    todo = collections.find_one({"_id" : ObjectId(id)})
    if todo:
        todo["_id"] = str(todo["_id"])
        return todo
    else:
        raise HTTPException(404, "To-do not found")
    
@app.put("/todo/{id}")
def update_todo(id: str, todo: ToDoModel):
    todo_data = todo.dict()
    updated_todo = collections.find_one_and_replace(
        {"_id": id}, {"$set": todo_data}
    )
    if updated_todo:
        return updated_todo
    else:
        raise HTTPException(404, "To-do not found")
    
@app.delete("/todo/{id}")
def delete_todo(id: str):
    todo = collections.find_one_and_delete({"_id": id})
    if todo:
        return {"message": f"To-do {id} deleted successfully"}
    else:
        raise HTTPException(404, "To-do not found")
    
@app.put("/todo/{id}/done")
def mark_todo_as_done(id: str):
    todo = collections.find_one_and_update(
        {"_id": id}, {"$set": {"done": True}}
    )
    if todo:
        todo["_id"] = str(todo["_id"])
        return todo
    else:
        raise HTTPException(404, "To-do not found")