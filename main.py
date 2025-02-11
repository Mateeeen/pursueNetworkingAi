from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, Base

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get user by ID
@app.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    Users = Base.classes.users  # Access the reflected table
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name}

# Update user name
@app.get("/update/{user_id}")
async def update_user(user_id: int, db: Session = Depends(get_db)):
    Users = Base.classes.users  # Access the reflected table
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Update the name
    user.name = "new_name"
    db.commit()
    db.refresh(user)
    
    return {"id": user.id, "name": user.name}