from fastapi import FastAPI,HTTPException
from .db import SessionLocal, engine, Base
from .routers import user_router, task_router, comment_router, file_router
from app import models, auth
from app.auth import authMiddleware
from app.schemas import user_schema
from fastapi.middleware.cors import CORSMiddleware
import datetime


app = FastAPI()

## create all tables
Base.metadata.create_all(bind=engine)

## include all routers ##
app.include_router(user_router)
app.include_router(task_router)
app.include_router(comment_router)
app.include_router(file_router)

origins = [
    "http://localhost:3000",  # your frontend URL
    "http://127.0.0.1:3000",  # sometimes used
    "http://localhost:8000",  # if frontend served from backend
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # or ["*"] for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware('http')(authMiddleware)

@app.get('/')
def home():
	return {"message":"FAST api is running"}


@app.post('/register')
def createUser(user:user_schema.UserCreate):
	db = SessionLocal()
	hashedpw = auth.hash_password(user.password)
	newuser = models.User(
		name=user.name,
		email=user.email,
		password=hashedpw,
		created_at=datetime.datetime.utcnow())
	db.add(newuser)
	db.commit()
	return {"message":"user created successfully"}


@app.post('/login')
def apiLogin(user:user_schema.UserLogin):
	db = SessionLocal()

	getuser = db.query(models.User).filter(models.User.email==user.email).first()
	if not getuser:
		raise HTTPException(status_code=400,detail="User not exists")
	if not auth.verify_password(user.password,getuser.password):
		raise HTTPException(status_code=400,detail="Entered wrong password")

	token = auth.create_token({"user_id":getuser.id})

	return {"token":token}







	