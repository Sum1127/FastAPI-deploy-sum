import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

engine=create_engine(
    url=os.environ.get("DB_URL"),
    echo=bool(os.environ.get("DB_ECHO")),
)

# Supabase クライアントを初期化
# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

SessionLocal = sessionmaker(bind=engine)
