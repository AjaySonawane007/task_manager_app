from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from pydantic import BaseModel
from datetime import date

app = FastAPI()
@app.get("/")
def home():
    return {"message": "FastAPI is running successfully"}

# DB connection dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schema
class TaskSchema(BaseModel):
    title: str
    description: str
    priority: str
    due_date: date
    completed: bool

#CREATE TASK
@app.post("/tasks")
def create_task(task: TaskSchema, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# GET ALL TASKS
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

# UPDATE TASK
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated: TaskSchema, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        return {"error": "Task not found"}

    for key, value in updated.dict().items():
        setattr(db_task, key, value)

    db.commit()
    return db_task

# DELETE TASK
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        return {"error": "Task not found"}

    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted"}