from pydantic import BaseModel, ConfigDict
from typing import Optional
from . import comment_schema

class TaskCreate(BaseModel):
	name:str
	description:str

class TaskResponse(BaseModel):
	id:int
	name:str
	description:str
	user_id:int
	comments:list[comment_schema.CommentResponse] = []
	model_config = ConfigDict(from_attributes=True)

class UpdateTask(BaseModel):
	name:Optional[str]
	description:Optional[str]