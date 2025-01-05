import datetime

from model.Memomodel import UserMemo
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


def read_memo(db: Session, user_id: str):
    users = db.query(UserMemo).filter(UserMemo.user_id == user_id).order_by(UserMemo.id).all()
    return users

def read_id_usermemo(db:Session,user_id:str,id):
    return db.query(UserMemo).filter(UserMemo.user_id==user_id,UserMemo.id==id).order_by(UserMemo.id).first()

def read_select_memo(db:Session,user_id:str,title):
    select_users = db.query(UserMemo).filter(UserMemo.user_id == user_id,UserMemo.title.like(f"%{title}%")).order_by(UserMemo.id).all()
    return select_users

def read_timeselect_memo(db:Session,user_id:str,created_at:datetime.datetime):
    search_date=created_at.strftime('%Y-%m-%d')

    select_times=db.query(UserMemo).filter(
        UserMemo.user_id == user_id,
        func.date_trunc('day',UserMemo.created_at)==search_date,
        ).order_by(UserMemo.id).all()
    return select_times

def read_memo_dates(db:Session,user_id:str):
    result=db.query(func.date_trunc('day',UserMemo.created_at).label("created_date")).filter(
        UserMemo.user_id==user_id,
    ).distinct().order_by(desc("created_date")).all()

    dates = []
    for row in result:
        dates.append(row.created_date)
    return dates

def edit_usermemo(id:int,title:str,content:str,db:Session,user_id:str):
    db_memo=db.query(UserMemo).filter(UserMemo.user_id==user_id,UserMemo.id==id).order_by(UserMemo.id).first()
    db_memo.title=title
    db_memo.content=content
    db.commit()
    return db_memo

def create_memo(db: Session, usermemo: UserMemo):
    db.add(usermemo)
    db.commit()


def destroy_memo(db: Session, user_id: str, id: int):
    db.query(UserMemo).filter(UserMemo.user_id == user_id, UserMemo.id == id).delete()
    db.commit()