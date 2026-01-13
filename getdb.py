from database import session
from sqlalchemy.orm import Session

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()