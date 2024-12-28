from sqlalchemy.orm import Session

from  model.Memomodel import UserMemo


def read_memo(db: Session, user_id: str):
    users = db.query(UserMemo).filter(UserMemo.user_id == user_id).order_by(UserMemo.id).all()
    return users

def read_select_memo(db:Session,user_id:str,title):
    select_users = db.query(UserMemo).filter(UserMemo.user_id == user_id,UserMemo.title.like(f"%{title}%")).order_by(UserMemo.id).all()
    return select_users


def create_memo(db: Session, usermemo: UserMemo):
    db.add(usermemo)
    db.commit()


def destroy_memo(db: Session, user_id: str, id: int):
    db.query(UserMemo).filter(UserMemo.user_id == user_id, UserMemo.id == id).delete()
    db.commit()