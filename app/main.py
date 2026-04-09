from app.database import *
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse 
from models.user import *
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
@app.get("/api/users")
def get_people(db: Session = Depends(get_db)):
    return db.query(Students).all()

@app.post('/api/user', response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    new_user = Students(
        name = user.name,
        course = user.course,
        age = user.age,
        start_date = user.start_date or datetime.now()
    )
    
    is_exists = db.query(Students).filter(Students.name == user.name).first()
    
    if is_exists:
        raise HTTPException(
        status_code=400,
        detail="Такой студент уже существует"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.delete('/api/user/{id}')
def delete_user(id: int, db: Session = Depends(get_db)):
    
    user =  db.query(Students).filter(Students.id == id).first()
    
    if not user: 
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": "Пользователь удалён"}