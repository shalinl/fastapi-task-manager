from pydantic import BaseModel,ConfigDict
from typing import Optional
from . import file_schema

class CommentCreate(BaseModel):
	description:str
	task_id:int

class CommentResponse(BaseModel):
	id:int
	description:str
	user_id:int
	task_id:int
	files:list[file_schema.FileResponse] = []
	model_config = ConfigDict(from_attributes=True)

class UpdateComment(BaseModel):
	description:Optional[str]