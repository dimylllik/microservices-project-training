from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

Base = declarative_base()

engine = create_engine(DATABASE_URL, echo=False, future=True)

Session = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=True
)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
