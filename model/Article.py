from pydantic import BaseModel,ConfigDict
from typing import List
from sqlalchemy import  Column,Integer,DateTime,Text,ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped
from datetime import datetime, timedelta

def get_jst_now():
    return datetime.utcnow() + timedelta(hours=9)

class Base(DeclarativeBase):
    pass

# 記事のデータモデル
class Article(Base):
    __tablename__="articles"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = Column(Text, nullable=False)
    content: Mapped[str] = Column(Text, nullable=False)
    tags: List[str]=Column(ARRAY(Text), nullable=False)  # タグは文字列のリスト
    created_at: Mapped[datetime] = Column(DateTime, default=get_jst_now)

class ArticleSchema(BaseModel):
    id:int
    title:str
    content:str
    tags:List[str]

    model_config = ConfigDict(from_attributes=True)
