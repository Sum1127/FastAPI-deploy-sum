from typing import Union
from fastapi import FastAPI,HTTPException,Body,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from uuid import UUID
from sqlalchemy.orm import Session
from model.Article import Article,ArticleSchema
from model.Memomodel import UserMemo,UserMemoSchema
import os
from dotenv import load_dotenv
import database.supabase_client 
from database.article import research_articles,add_articles,read_select_article,read_research_article
from database.usermemo import read_memo,create_memo,destroy_memo,read_select_memo

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
    title: Union[str,None] = None,
    db: Session = Depends(get_db),
):
    if title is not None:
        search_articles=read_research_article(db,title)
        return search_articles
    
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
    db:Session=Depends(get_db),
    user_id: UUID = Depends(get_auth_user_id),
)->list[UserMemoSchema]:
    if title is not None:
        search_memo_list=read_select_memo(db,user_id,title)
        return search_memo_list
    
    memo_list=read_memo(db, user_id)
    return [UserMemoSchema.model_validate(i) for i in memo_list]

@app.post("/createarticles")
async def post_articles(
    title:str=Body(...),
    content:str=Body(...),
    tags:list[str]=Body([...]),
    db: Session = Depends(get_db),
)->ArticleSchema:
    f=add_articles(db,title,content,tags)
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