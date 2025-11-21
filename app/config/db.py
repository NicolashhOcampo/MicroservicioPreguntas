from sqlmodel import create_engine, SQLModel, Session
from app.models import Question, Answer
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL= os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
        
def get_session_sync():
    return Session(engine)