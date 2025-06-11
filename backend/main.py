from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from redis_app import RedisService
from datetime import datetime

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
    new_task = create_user_task(db=db, task=task, user_id=current_user.id)
    
    # Invalidate the cached task list
    RedisService.delete_key(f"user_tasks:{current_user.id}")
    
    return new_task

@app.get("/api/tasks", response_model=List[Task])
def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Try to get tasks from cache
    cache_key = f"user_tasks:{current_user.id}"
    cached_tasks = RedisService.get_key(cache_key)
    if cached_tasks:
        return cached_tasks

    # If not in cache, get from database
    tasks = get_user_tasks(db=db, user_id=current_user.id)
    
    # Cache the tasks for 5 minutes
    RedisService.set_key(cache_key, [task.to_dict() for task in tasks])
    
    return tasks

@app.get("/api/test-celery/{x}/{y}")
async def test_celery(x: int, y: int):
    result = sample_task.delay(x, y)
    return {"task_id": result.id}

@app.get("/api/redis-test")
async def test_redis():
    """
    Test Redis connectivity and basic operations
    Returns:
        dict: Status of different Redis operations
    """
    test_key = "test:connection"
    test_value = {"message": "Hello Redis!", "timestamp": str(datetime.now())}
    
    results = {
        "connection": False,
        "write": False,
        "read": False,
        "delete": False
    }
    
    try:
        # Test writing to Redis
        write_success = RedisService.set_key(test_key, test_value)
        results["write"] = write_success
        results["connection"] = True
        
        # Test reading from Redis
        read_value = RedisService.get_key(test_key)
        results["read"] = read_value is not None and read_value.get("message") == test_value["message"]
        
        # Test deleting from Redis
        delete_success = RedisService.delete_key(test_key)
        results["delete"] = delete_success
        
        return {
            "status": "success",
            "message": "Redis is working properly" if all(results.values()) else "Some Redis operations failed",
            "details": results,
            "read_value": read_value
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Redis test failed: {str(e)}"
        )

@app.post("/api/redis-test/{key}")
async def set_redis_value(key: str, value: dict):
    """
    Set a custom key-value pair in Redis
    Args:
        key: The key to set
        value: The value to store
    """
    success = RedisService.set_key(f"custom:{key}", value)
    return {
        "status": "success" if success else "error",
        "message": f"Value for key '{key}' was {'saved' if success else 'not saved'}"
    }

@app.get("/api/redis-test/{key}")
async def get_redis_value(key: str):
    """
    Get a value from Redis by key
    Args:
        key: The key to retrieve
    """
    value = RedisService.get_key(f"custom:{key}")
    if value is None:
        raise HTTPException(
            status_code=404,
            detail=f"No value found for key '{key}'"
        )
    return {
        "status": "success",
        "key": key,
        "value": value
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)