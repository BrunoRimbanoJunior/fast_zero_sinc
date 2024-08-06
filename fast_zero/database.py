import os

# from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.settings import Settings

# load_dotenv()

database_url = os.getenv(Settings().DATABASE_URL)
engine = create_engine(database_url)


def get_session():
    with Session(engine) as session:
        yield session
