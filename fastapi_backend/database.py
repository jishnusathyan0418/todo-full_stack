import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# SQL_DATABASE_URL = "postgresql://jishnu04:shyjasathyan17@localhost:5432/my_database"
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessioLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
