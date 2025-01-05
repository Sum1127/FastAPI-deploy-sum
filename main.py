import datetime
import os
from typing import Union
from uuid import UUID

import database.supabase_client
from database.article import (
    add_articles,
    read_research_article,
    read_select_article,
    research_articles,
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
from dotenv import load_dotenv
from fastapi import Body, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from model.Article import ArticleSchema
from model.Memomodel import UserMemo, UserMemoSchema
from sqlalchemy.orm import Session

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


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
    db: Session = Depends(get_db),
):
    if title is not None:
        search_articles=read_research_article(db,title)
        return search_articles
    
    elif id is not None: 
        id_articles=read_select_article(db,id)
        return id_articles

    articles=research_articles(db)
    return articles


@app.get("/articles/{id}")
def get_select_article(
    id:int,
    db: Session = Depends(get_db),
):
    select_article=read_select_article(db,id)
    return select_article

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
    db: Session = Depends(get_db),
)->ArticleSchema:
    f=add_articles(db,title,content,tags,user_name,user_avatar,user_email)
    return ArticleSchema.model_validate(f)

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

@app.delete("/usermemo/{id}")
async def delete_usermemo(
    id:int,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_auth_user_id),
) -> None:
    destroy_memo(db,user_id,id)

#async def create_article(article: Article):
#    response = supabase.table("articles").insert({
 #       "title": article.title,
 #       "content": article.content,
  #      "tags": article.tags,
   # }).execute()
#
 #   if response.get("status_code") == 201:
  #      return {"message": "記事が保存されました。"}
   # raise HTTPException(status_code=500, detail="記事の保存に失敗しました。")