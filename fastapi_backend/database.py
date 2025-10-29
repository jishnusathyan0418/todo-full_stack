import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQL_DATABASE_URL = "postgresql://jishnu04:shyjasathyan17@localhost:5432/my_database"

engine = create_engine(
    SQL_DATABASE_URL
)

SessioLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
