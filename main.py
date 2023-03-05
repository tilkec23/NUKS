from fastapi import FastAPI
from database import engine, Base, ToDo
import shemas
from typing import Union
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/add")
async def add_todo(todo: shemas.ToDo):
    """API call for adding a TODO item"""
    session = Session(engine, expire_on_commit=False)
    new_todo = ToDo(task=todo.task)
    session.add(new_todo)
    session.commit()
    id = new_todo.id
    session.close()
    return f"Created new TODO item with id {id}"

@app.get("/delete/{id}")
async def delete_todo(id: int):
    """API call for deleting a TODO item"""
    return {"message": "Delete TODO"}

@app.get("/update/{id}")
async def update_todo(id: int):
    """API call for updating a TODO item"""
    return {"message": "Update TODO"}

@app.get("/get/{id}")
async def get_todo(id: int):
    """API call for getting a TODO item"""
    return {"message": "Get TODO"}

@app.get("/list")
async def list_todo():
    """API call for listing all TODO items"""
    return {"message": "List TODO"}
