from pydantic import BaseModel,ConfigDict

class UserCreate(BaseModel):
	name:str
	email:str
	password:str

class UserLogin(BaseModel):
	email:str
	password:str

	model_config = ConfigDict(from_attributes=True)