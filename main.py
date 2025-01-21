import datetime
from typing import Union
from uuid import UUID

import database.supabase_client
from database.article import (
    add_articles,
    destroy_article,
    edit_article,
    read_descarticles,
    read_myarticle,
    read_research_article,
    read_select_article,
    research_articles,
    read_tags_article,
)
from database.bookmark import (
    favorite_article,
    read_favorite_article,
    destroy_favorite_article,
)
from database.usermemo import (
    create_memo,
    destroy_memo,
    edit_usermemo,
    read_id_usermemo,
    read_memo,
    read_memo_dates,
    read_select_memo,
    read_timeselect_memo,
)
from fastapi import Body, Depends, FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from model.Article import ArticleSchema
from model.Bookmark import BookMark, BookMarkSchema
from model.Memomodel import UserMemo, UserMemoSchema
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.supabase_client.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_auth_user_id(authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> UUID:
    # FIXME: Need to use 〇〇〇
    return UUID(authorization.credentials)


@app.get("/")
async def root():
    return {"message": "Hello World From Fast API!"}

@app.get("/articles")
async def get_articles(
    id:Union[int,None]=None,
    title: Union[str,None] = None,
    tags:Union[str,None]=None,
    db: Session = Depends(get_db),
):
    if title is not None:
        search_articles=read_research_article(db,title)
        return search_articles
    
    elif id is not None: 
        id_articles=read_select_article(db,id)
        return id_articles
    
    elif tags is not None:
        tags_articles=read_tags_article(db,tags.split(","))
        return tags_articles

    articles=research_articles(db)
    return articles

@app.get("/homearticles")
async def get_descarticles(
    db: Session = Depends(get_db),
):
    home_articles=read_descarticles(db)
    return home_articles


@app.get("/articles/{id}")
def get_select_article(
    id:int,
    db: Session = Depends(get_db),
):
    select_article=read_select_article(db,id)
    return select_article

# @app.get("/myarticle")
# def get_myarticle(
#     db:Session=Depends(get_db),
#     user_id:UUID=Depends(get_auth_user_id)
# )->list[ArticleSchema]:
#     myarticle=search_myarticle(db,user_id)
#     return myarticle

@app.get("/mypage")
async def get_mypage(
    db:Session=Depends(get_db),
    user_id: UUID = Depends(get_auth_user_id),
):
    mypage=read_myarticle(db,user_id)
    return mypage

@app.get("/mypage/bookmark")
async def get_mybookmark(
    db:Session=Depends(get_db),
    user_id:UUID=Depends(get_auth_user_id),
):
    show_bookmark=read_favorite_article(db,user_id)
    return show_bookmark

@app.get("/usermemo")
async def get_usermemo(
    title: Union[str,None] = None,
    created_at:Union[datetime.datetime,None]=None,
    db:Session=Depends(get_db),
    user_id: UUID = Depends(get_auth_user_id),
)->list[UserMemoSchema]:
    if title is not None:
        search_memo_list=read_select_memo(db,user_id,title)
        return search_memo_list
    
    elif created_at is not None:
        searchtime_memo_list=read_timeselect_memo(db,user_id,created_at)
        return searchtime_memo_list
    
    memo_list=read_memo(db, user_id)
    return [UserMemoSchema.model_validate(i) for i in memo_list]

@app.get("/usermemo/{id}")
async def get_idmemo(
    id:int,
    db:Session=Depends(get_db),
    user_id: UUID = Depends(get_auth_user_id),
):
    select_usermemo=read_id_usermemo(db,user_id,id)
    return select_usermemo


@app.get("/usermemo_dates")
async def get_usermemo_dates(
    db:Session=Depends(get_db),
    user_id: UUID = Depends(get_auth_user_id),
)->list[datetime.datetime]:
    memo_dates=read_memo_dates(db,user_id)
    return memo_dates

@app.put("/articles/{id}")
async def put_myarticle(
    id:int,
    title:str=Body(...),
    content:str=Body(...),
    tags:list[str]=Body([...]),
    db:Session=Depends(get_db),
    user_id: UUID = Depends(get_auth_user_id),
)->ArticleSchema:
    print("id",id)
    print("title",title)
    print("content",content)
    print("tags",tags)

    edit=edit_article(id,title,content,tags,db,user_id)
    return ArticleSchema.model_validate(edit)

@app.put("/usermemo/{id}")
async def put_usermemo(
    id:int,
    title:str=Body(...),
    content:str=Body(...),
    db:Session=Depends(get_db),
    user_id: UUID = Depends(get_auth_user_id),
)->UserMemoSchema:
    f=edit_usermemo(id,title,content,db,user_id)
    return UserMemoSchema.model_validate(f)


@app.post("/createarticles")
async def post_articles(
    title:str=Body(...),
    content:str=Body(...),
    tags:list[str]=Body([...]),
    user_name:str=Body(...),
    user_avatar:str=Body(...),
    user_email:str=Body(...),
    user_id:str=Body(...),
    db: Session = Depends(get_db),
)->ArticleSchema:
    f=add_articles(db,title,content,tags,user_name,user_avatar,user_email,user_id)
    return ArticleSchema.model_validate(f)

@app.post("/mypage/bookmark/{article_id}")
async def post_bookmarkarticle(
    article_id:int=None,
    db:Session=Depends(get_db),
    user_id:UUID=Depends(get_auth_user_id),
)->BookMarkSchema:
    if not article_id:
        raise HTTPException(status_code=400, detail="Question ID must be provided")
    bookmark=BookMark(article_id,user_id)
    favorite_article(db,bookmark)
    return BookMarkSchema.model_validate(bookmark)

@app.post("/usermemo")
async def post_usermemo(
    title:str=Body(...),
    content:str=Body(...),
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_auth_user_id),
)->UserMemoSchema:
    i=UserMemo(title,content,user_id)
    create_memo(db,i)
    return UserMemoSchema.model_validate(i)

@app.delete("/articles/{id}")
async def delete_article(
    id:int,
    db:Session=Depends(get_db),
)->None:
    destroy_article(id,db)


@app.delete("/usermemo/{id}")
async def delete_usermemo(
    id:int,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_auth_user_id),
) -> None:
    destroy_memo(db,user_id,id)

@app.delete("/mypage/bookmark/{id}")
async def delete_mybookmark(
    id:int,
    db:Session=Depends(get_db),
    user_id:UUID=Depends(get_auth_user_id),
)->None:
    destroy_favorite_article(db,user_id,id)