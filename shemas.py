from pydantic import BaseModel

class ToDo(BaseModel):
    id: int
    task: str