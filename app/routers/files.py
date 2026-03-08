from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from pathlib import Path
import shutil

from app import models
from app.auth import get_current_user
from app.db import SessionLocal

router = APIRouter(
    prefix="/files",
    tags=["Files"],
    dependencies=[Depends(get_current_user)]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)  # create if not exists


@router.post("/upload-file")
def upload_file(file: UploadFile = File(...), task_id: int = 0, user: int = Depends(get_current_user)):

    db: Session = SessionLocal()

    # Create comment
    new_comment = models.Comment(
        description="",
        task_id=task_id,
        user_id=user
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    # Save the file to uploads folder
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create file record in DB
    new_file = models.UploadFile(
        name=file.filename,
        url=str(file_path),
        comment_id=new_comment.id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    if not new_file:
    	raise HTTPException(status_code=500,detail="Error Uploading file")  

    return {
        "file_id": new_file.id,
        "comment_id": new_comment.id,
        "file_path": str(file_path)
    }