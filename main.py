from fastapi import FastAPI, HTTPException
from database import engine, Base, ToDo
import shemas
from typing import Union
from sqlalchemy.orm import Session
from fastapi_versioning import VersionedFastAPI, version


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
@version(1)
async def root():
    return {"message": "Hello World"}

@app.post("/add")
@version(1)
async def add_todo(todo: shemas.ToDo):
    """API call for adding a TODO item"""
    session = Session(engine, expire_on_commit=False)
    new_todo = ToDo(task=todo.task)
    print(new_todo)
    session.add(new_todo)
    session.commit()
    id = new_todo.id
    session.close()
    return f"Created new TODO item with id {id}"


@app.delete("/delete/{id}")
@version(1)
async def delete_todo(id: int):
    """API call for deleting a TODO item"""
    session = Session(engine, expire_on_commit=False)
    if not session.query(ToDo).filter(ToDo.id == id).first():
        raise HTTPException(status_code=404, detail="TODO item not found")
    todo = session.query(ToDo).filter(ToDo.id == id).first()
    session.delete(todo)
    session.commit()
    id = todo.id
    session.close()
    return f"Deleted TODO item with id {id}"

@app.put("/update/{id}")
@version(1)
async def update_todo(id: int, todo: shemas.ToDo):
    """API call for updating a TODO item"""
    session = Session(engine, expire_on_commit=False)
    if not session.query(ToDo).filter(ToDo.id == id).first():
        raise HTTPException(status_code=404, detail="TODO item not found")
    existing_todo = session.query(ToDo).filter(ToDo.id == id).first()
    existing_todo.task = todo.task
    session.commit()
    id = existing_todo.id
    session.close()
    return f"Updated TODO item with id {id} with content {todo.task}"

@app.get("/get/{id}")
@version(1)
async def get_todo(id: int):
    """API call for getting a TODO item"""
    session = Session(engine, expire_on_commit=False)
    if not session.query(ToDo).filter(ToDo.id == id).first():
        raise HTTPException(status_code=404, detail="TODO item not found")
    todo = session.query(ToDo).filter(ToDo.id == id).first()
    session.close()
    return f"The TODO item with the ID:{id} is {todo.task}"

@app.get("/list")
@version(1)
async def list_todo():
    """API call for listing all TODO items"""
    session = Session(engine, expire_on_commit=False)
    todos = session.query(ToDo).all()
    session.close()
    return f"The TODO items are {todos}"

app = VersionedFastAPI(app, version_format="{major}", prefix_format="/v{major}")