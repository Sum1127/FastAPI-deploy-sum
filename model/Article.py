from datetime import datetime
from typing import List

import pytz
from pydantic import BaseModel, ConfigDict
from sqlalchemy import ARRAY, Column, DateTime, Integer, Text
from sqlalchemy.orm import DeclarativeBase, Mapped


def get_jst_now():
    return datetime.now(pytz.timezone('Asia/Tokyo'))

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
    user_name: Mapped[str] = Column(Text, nullable=True)
    user_avatar: Mapped[str] = Column(Text, nullable=True)
    user_email:Mapped[str]=Column(Text,nullable=True)

class ArticleSchema(BaseModel):
    id:int
    title:str
    content:str
    tags:List[str]
    user_name:str
    user_avatar:str
    user_email:str

    model_config = ConfigDict(from_attributes=True)
