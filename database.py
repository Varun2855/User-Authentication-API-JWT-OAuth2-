from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url="postgresql://postgres:12345@localhost:5432/authdb"; #dummy password
engine=create_engine(db_url)
session=sessionmaker(autocommit=False, autoflush=False, bind=engine)
