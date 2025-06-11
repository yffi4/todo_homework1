from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional

# Change these from relative imports to absolute imports
from database import get_db, engine
from models import Base
from schemas import UserCreate, User, Token, TaskCreate, Task
from crud import (
    create_user,
    authenticate_user,
    get_current_user,
    create_access_token,
    get_user_tasks,
    create_user_task
)
from tasks import sample_task

Base.metadata.create_all(bind=engine)   

app = FastAPI(title="Todo App API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication endpoints
@app.post("/api/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@app.post("/api/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Protected endpoints
@app.get("/api/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/api/tasks", response_model=Task)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_user_task(db=db, task=task, user_id=current_user.id)

@app.get("/api/tasks", response_model=List[Task])
def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_tasks(db=db, user_id=current_user.id)

@app.get("/api/test-celery/{x}/{y}")
async def test_celery(x: int, y: int):
    result = sample_task.delay(x, y)
    return {"task_id": result.id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)