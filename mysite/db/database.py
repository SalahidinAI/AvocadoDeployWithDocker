from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

DB_URL = 'postgresql://postgres:adminadmin@localhost/Avocado'

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
