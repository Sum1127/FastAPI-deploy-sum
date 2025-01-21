from model.Bookmark import BookMark
from model.Article import Article
from sqlalchemy.orm import Session

def read_favorite_article(db:Session,user_id:str):
    bookmarks=db.query(BookMark).join(Article).all()
    return [
        {
            "id":bookmark.id,
            "article_id":bookmark.article_id,
            "user_id":bookmark.user_id,
            "article":{
                "id":bookmark.article.id,
                "title":bookmark.article.title,
                "content":bookmark.article.content,
                "tags":bookmark.article.tags,
                "user_name":bookmark.article.user_name,
                "user_avatar":bookmark.article.user_avatar,
                "user_email":bookmark.article.user_email
            }
        }
        for bookmark in bookmarks
    ]

def favorite_article(db:Session,bookmark:BookMark):
    # existing_bookmark = (
    #     db.query(BookMark)
    #     .filter(BookMark.user_id == bookmark.user_id, BookMark.article_id == BookMark.article_id)
    #     .first()
    # )
    # if existing_bookmark:
    #     return existing_bookmark
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)

def destroy_favorite_article(db:Session,user_id:str,id:int):
    db.query(BookMark).filter(BookMark.user_id==user_id,BookMark.id==id).delete()
    db.commit()