from fastapi import APIRouter, Request, HTTPException, Depends
from app import models
from app.db import SessionLocal
from app.auth import verify_token, get_current_user


router = APIRouter( prefix = "/users",tags =["Users"], dependencies=[Depends(get_current_user)])

@router.get("/profile")
def profile(user_id: int = Depends(get_current_user)):

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Create DB session
    db = SessionLocal()
    data = db.query(models.User).filter(models.User.id == user_id).first()
    if not data:
        raise HTTPException(status_code=400, detail="User not found")

    return {"data": data}
