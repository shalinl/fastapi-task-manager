from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=True, default="")
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    # Relationships
    task = relationship("Task", back_populates="comments")   # Comment belongs to Task
    files = relationship("UploadFile", back_populates="comment", cascade="all, delete-orphan")  # Comment has many files