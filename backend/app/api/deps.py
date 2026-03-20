from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db


DbSession = Session


def db_dependency(db: Session = Depends(get_db)) -> Session:
    return db
