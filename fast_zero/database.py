from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.settings import Settings

# o create engine recebe o caminho da base
engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
