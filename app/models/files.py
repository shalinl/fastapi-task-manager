from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class UploadFile(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    url = Column(String(255))
    comment_id = Column(Integer, ForeignKey("comments.id"))
    
    # Relationships
    comment = relationship("Comment", back_populates="files")  # File belongs to a Comment