from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI() #create an instance of FastAPI

todos = [] #creating an in-memory db for storing todos

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

@app.get('/todos')
async def get_todos():
    return todos

@app.post('/todos')
async def create_todo(todo: Todo):
    todos.append(todo.dict()) # append the todo to the list
    return { "Todo created ": todos[-1] } # return the last element

@app.get('/todos/{todo_id}')
async def get_todo_by_id(todo_id: int):
    for todo in todos :
        if todo['id'] == todo_id :
            return {"Todo found ": todo}
    return {"Error": "Todo not found"}

@app.delete('/todos/{todo_id}')
async def delete_todo(todo_id: int):
    for todo in todos :
        if todo['id'] == todo_id :
            todos.remove(todo)
            return {"message ": "Todo deleted successfully"}
    return {"Error": "Todo not found"}