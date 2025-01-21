import uuid

from model.Article import Base,Article
from pydantic import BaseModel, ConfigDict
from sqlalchemy import UUID, Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped,relationship


class BookMark(Base):
    __tablename__="bookmark"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    article_id:Mapped[int]=Column(Integer,ForeignKey("articles.id",ondelete="CASCADE"),nullable=False)
    user_id:Mapped[str]=Column(UUID,nullable=False, index=True)
        # リレーションを追加
    article: Mapped[Article] = relationship("Article", backref="bookmarks", lazy="joined")

    def __init__(self,article_id:int,user_id:uuid.UUID):
        self.article_id=article_id
        self.user_id=user_id

class BookMarkSchema(BaseModel):
    id:int
    article_id:int

    model_config = ConfigDict(from_attributes=True)
