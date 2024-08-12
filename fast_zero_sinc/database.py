from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero_sinc.settings import Settings

settings = Settings()

engine = create_engine(settings.DATABASE_URL)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
