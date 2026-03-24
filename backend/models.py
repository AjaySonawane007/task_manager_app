from sqlalchemy import Column, Integer, String, Boolean, Date
from database import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255))
    priority = Column(String(50))
    due_date = Column(Date)
    completed = Column(Boolean, default=False)