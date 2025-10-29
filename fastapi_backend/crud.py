from sqlalchemy.orm import Session

import schema, models


def create_todo(db:Session, todo:schema.ToDoRequests):
    db_todo = models.Todo(name=todo.name, completed = todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def read_todos(db:Session, completed:bool=None):
    if completed is None:
        return db.query(models.Todo).all()
    else:
        return db.query(models.Todo).filter(models.Todo.completed == completed).all()
   
def read_todo(db:Session, id:int):
    return db.query(models.Todo).filter(models.Todo.id==id).first()

def updated_todo(db:Session, id:int, todo:schema.ToDoRequests):
    db_todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if db_todo is None:
        return None
    db.query(models.Todo).filter(models.Todo.id==id).update({'name': todo.name, 'completed': todo.completed})
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db:Session, id:int):
    db_todo = db.query(models.Todo).filter(models.Todo.id== id).first()
    if db_todo is None:
        return None
    db.query(models.Todo).filter(models.Todo.id == id).delete()
    db.commit()
    return True

    