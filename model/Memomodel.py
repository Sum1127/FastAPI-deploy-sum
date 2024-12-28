import uuid

from pydantic import BaseModel, ConfigDict
from sqlalchemy import UUID, Column, Integer,Text,DateTime

from model.Article import Base,get_jst_now

class UserMemo(Base):
    __tablename__="usermemo"
    id = Column(Integer,primary_key=True,autoincrement=True)
    title=Column(Text,nullable=False)
    content=Column(Text,nullable=False)
    user_id=Column(UUID,nullable=False, index=True)
    created_at= Column(DateTime, default=get_jst_now)

    def __init__(self,title:str,content:str,user_id:uuid.UUID):
        self.title=title
        self.content=content
        self.user_id=user_id

class UserMemoSchema(BaseModel):
    id:int
    title:str
    content:str

    model_config = ConfigDict(from_attributes=True)



