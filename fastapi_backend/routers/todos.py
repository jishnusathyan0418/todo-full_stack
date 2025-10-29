from sqlalchemy.orm import Session
import crud
import schema
from typing import List
from fastapi import Depends, HTTPException, status, APIRouter
from database import SessioLocal
import models


router = APIRouter(
    prefix="/todos"
)

def get_db():
    db = SessioLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@router.post("", status_code=status.HTTP_201_CREATED)
def create_todo(todo: schema.ToDoRequests, db:Session =Depends(get_db)):
    new_todo = crud.create_todo(db, todo)
    return new_todo

@router.get("", response_model=List[schema.ToDoResponse])
def read_todos(completed: bool=None, db:Session = Depends(get_db)):
    todos = crud.read_todos(db, completed)
    return todos

@router.get("/{id}")
def read_todo(id:int, db:Session=Depends(get_db)):
    todo = crud.read_todo(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="not found")
    return todo
    
@router.put("/{id}")
def update_todo(id:int, todo:schema.ToDoRequests, db: Session=Depends(get_db)):
    todo = crud.updated_todo(db, id, todo)
    if todo is None:
        raise HTTPException(status_code=404, detail="not found")
    return todo

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_todo(id: int, db:Session=Depends(get_db)):
    res = crud.delete_todo(db, id)
    if res is None:
        raise HTTPException(status_code=404, detail="not found")
