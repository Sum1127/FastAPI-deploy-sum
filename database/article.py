from model.Article import Article
from sqlalchemy.orm import Session

# def fetch_articles():
#     try:
#         response = supabase.table("articles").select("*").execute()
#         if response.error:
#             print(f"Error: {response.error}")
#             return []
#         return response.data
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         return []

# if __name__ == "__main__":
#     articles = fetch_articles()
#     if articles:
#         print("Articles fetched successfully:", articles)
#     else:
#         print("Failed to fetch articles")

def research_articles(db:Session):
    return db.query(Article).all()

def add_articles(db: Session,title,content,tags, user_name, user_avatar,user_email):
    db_article=Article(title=title,content=content,tags=tags, user_name=user_name, user_avatar=user_avatar,user_email=user_email)
    db.add(db_article)
    db.commit()
    return db_article

def read_select_article(db:Session, id):
    return db.query(Article).filter(Article.id==id).first()

def read_research_article(db:Session,title):
    return db.query(Article).filter(Article.title.like(f"%{title}%")).all()


# def read_id_article(db:Session,id):
#     return db.query(Article).filter(Article.id==id).first()
