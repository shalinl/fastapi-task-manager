from fastapi import APIRouter, Request, HTTPException, Depends
from app import models
from app.db import SessionLocal
from app.auth import get_current_user
from app.schemas import comment_schema

router = APIRouter(prefix="/comments",tags=["Comments"],dependencies=[Depends(get_current_user)])

@router.get('/getall/{task_id}')
def getAllComments(taskid:int,user:int = Depends(get_current_user)):

	if not user:
		raise HTTPException(status_code=401,detail="unauthorised")

	db = SessionLocal()
	data = db.query(models.Comment).filter(models.Comment.user_id==user,models.Comment.task_id==taskid).all()

	if not data:
		raise HTTPException(status_code=400,detail="data not found")

	return { "data": data}


@router.post('/create')
def createComment(comment:comment_schema.CommentCreate,user:int=Depends(get_current_user)):

	if not user:
		raise HTTPException(status_code=401,detail="unauthorised")

	db = SessionLocal()

	newComment = models.Comment(
			description=comment.description,
			task_id=comment.task_id,
			user_id= user
		)
	db.add(newComment)
	db.commit()

	return {
		"message":"Comment created successfully"
	}

@router.put("/update/{commentid}")
def updateComment(commentid: int, comment: comment_schema.UpdateComment, user: int = Depends(get_current_user)):

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    db = SessionLocal()

    getComment = db.query(models.Comment).filter(
        models.Comment.id == commentid,
        models.Comment.user_id == user
    ).first()

    if not getComment:
        db.close()
        raise HTTPException(status_code=404, detail="Comment not found")

    # Update only fields sent by client
    for field, value in comment.dict(exclude_unset=True).items():
        setattr(getComment, field, value)

    db.commit()
    db.refresh(getComment)
    db.close()

    return {"data": getComment}

@router.delete("/delete/{commentid}")
def deleteComment(commentid: int, user: int = Depends(get_current_user)):

    if not user:
        raise HTTPException(status_code=400, detail="Unauthorized")

    db = SessionLocal()

    getComment = db.query(models.Comment).filter(
        models.Comment.id == commentid,
        models.Comment.user_id == user
    ).first()

    if not getComment:
        db.close()
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(getComment)
    db.commit()  # don't forget to commit the delete
    db.close()

    return {"message": "Comment Deleted successfully"}

@router.get('/get')
def getCommentById(commentid:int,user:int = Depends(get_current_user)):

    if not user:
        raise HTTPException(status_code=401,detail="unauthorised")

    db = SessionLocal()
    data = db.query(models.Comment,models.UploadFile)\
    .join(models.UploadFile, models.Comment.id == models.UploadFile.comment_id,isouter=True)\
    .filter(models.Comment.user_id==user, models.Comment.id==commentid).all()

    if not data:
        raise HTTPException(status_code=400,detail="data not found")

    return { "data": data}