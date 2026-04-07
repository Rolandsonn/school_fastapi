from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    course: str
    age: int
    start_date: Optional[datetime] = None 
    
    class Config:
        orm_mode = True 

class UserOut(BaseModel):
    id: int
    name: str
    course: str
    age: int
    start_date: Optional[datetime]

    class Config:
        orm_mode = True  # 🔑 позволяет сериализовать SQLAlchemy объекты