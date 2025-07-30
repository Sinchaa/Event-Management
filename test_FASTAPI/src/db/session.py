from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker

from ..core.config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.replace('%%','%')
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


# Dependency to get the database session
def get_db():
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()