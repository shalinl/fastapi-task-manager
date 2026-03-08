from fastapi import APIRouter, Request, HTTPException, Depends
from app import models
from app.db import SessionLocal
from app.auth import get_current_user
from app.schemas import task_schema
from sqlalchemy.orm import selectinload

router = APIRouter( prefix = "/tasks",tags =["Tasks"], dependencies=[Depends(get_current_user)])

@router.get('/getall')
def getAllTasks(page:int =1,size:int =10, user:int = Depends(get_current_user)):

    if not user:
        raise HTTPException(status_code=401,detail="unauthorised")

    db = SessionLocal()
    
    offset = (page - 1) * size

    data = db.query(models.Task)\
    .filter(models.Task.user_id==user)\
    .offset(offset)\
    .limit(size)\
    .all()

    if not data:
        raise HTTPException(status_code=400,detail="data not found")

    return { "data": data,"page":page,"size":size}



@router.post('/create')
def createTask(task:task_schema.TaskCreate,user:int=Depends(get_current_user)):

	if not user:
		raise HTTPException(status_code=401,detail="unauthorised")

	db = SessionLocal()

	newTask = models.Task(
			name=task.name,
			description=task.description,
			user_id= user
		)
	db.add(newTask)
	db.commit()

	return {
		"message":"Task created successfully"
	}


@router.put("/update/{taskid}")
def updateTask(taskid: int, task: task_schema.UpdateTask, user: int = Depends(get_current_user)):

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    db = SessionLocal()

    getTask = db.query(models.Task).filter(
        models.Task.id == taskid,
        models.Task.user_id == user
    ).first()

    if not getTask:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    # Update only fields sent by client
    for field, value in task.dict(exclude_unset=True).items():
        setattr(getTask, field, value)

    db.commit()
    db.refresh(getTask)
    db.close()

    return {"data": getTask}

@router.delete("/delete/{taskid}")
def deleteTask(taskid: int, user: int = Depends(get_current_user)):

    if not user:
        raise HTTPException(status_code=400, detail="Unauthorized")

    db = SessionLocal()

    getTask = db.query(models.Task).filter(
        models.Task.id == taskid,
        models.Task.user_id == user
    ).first()

    if not getTask:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(getTask)
    db.commit()  # don't forget to commit the delete
    db.close()

    return {"message": "Task Deleted successfully"}

@router.get('/get')
def getTaskById(taskid:int,user:int = Depends(get_current_user)):

    if not user:
        raise HTTPException(status_code=401,detail="unauthorised")

    db = SessionLocal()
    data = db.query(models.Task)\
    .options(
        selectinload(models.Task.comments)
        .selectinload(models.Comment.files)
    )\
    .filter(models.Task.id == taskid)\
    .all()


    if not data:
        raise HTTPException(status_code=400,detail="data not found")

    return data