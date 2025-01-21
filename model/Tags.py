from model.Article import Base

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import Mapped

class Tags(Base):
    __tablename__="tags"
    id:Mapped[int]=Column(Integer, primary_key=True, autoincrement=True)
    tagname:Mapped[str]=Column(Text,unique=True,nullable=False)

class TagsSchema(BaseModel):
    id:int
    tagname:str

    model_config = ConfigDict(from_attributes=True,arbitrary_types_allowed = True)

