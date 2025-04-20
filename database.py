from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

load_dotenv()
print("Loaded DATABASE_URL:", os.getenv("DATABASE_URL"))


DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)
# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL is not set in the environment variables.")

# if DATABASE_URL.startswith("postgresql://"):
#     raise ValueError("DATABASE_URL must use 'postgresql+asyncpg://' for async SQLAlchemy.")

engine = create_engine(DATABASE_URL)

# engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
