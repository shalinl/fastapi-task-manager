from pydantic import BaseModel,ConfigDict

class FileCreate(BaseModel):
	name:str
	url:str
	user_id:int
	task_id:int
	comment_id:int


class FileResponse(BaseModel):
	id:int
	name:str
	url:str
	user_id:int
	task_id:int
	comment_id:int

	model_config = ConfigDict(from_attributes=True)