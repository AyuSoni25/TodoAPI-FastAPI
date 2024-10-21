from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List
from models import TodoModel
from database import engine, Sessionlocal
from sqlalchemy.orm import Session

app = FastAPI() #create an instance of FastAPI

TodoModel.metadata.create_all(bind = engine) # Create the table in the database

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int

    class Config:
        orm_mode = True

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally: 
        db.close()


@app.get('/todos', response_model = List[TodoResponse])
async def get_todos(db: Session = Depends(get_db)):
    todos = db.query(TodoModel).all()
    return todos

@app.post('/todos', response_model = TodoResponse)
async def create_todo(todo: TodoBase, db: Session = Depends(get_db)):
    db_todo = TodoModel(title = todo.title, description = todo.description, completed = todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get('/todos/{todo_id}', response_model = TodoResponse)
async def get_todo_by_id(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    return todo

@app.delete('/todos/{todo_id}', response_model = TodoResponse)
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    db.delete(todo)
    db.commit()
    return todo