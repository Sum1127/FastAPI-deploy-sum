import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine=create_engine(
    url=os.environ.get("DB_URL"),
    echo=bool(os.environ.get("DB_ECHO")),
)

SessionLocal = sessionmaker(bind=engine)
