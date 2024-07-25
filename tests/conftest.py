import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session  # type: ignore
from fast_zero.models import User, table_registry

"""O arquivo conftest ou arquivo de configuracao do teste,
deve conter trechos de codigos que serão utilizados varias
vezes durante a criação de testes

Neste cado temos o client da Api e a Conexão com o banco de dados

Principio do DRY, não repetir codigo.
"""


@pytest.fixture
def client(session):
    """
    Para a execução de testes, não queremos executar no banco principal,
    então temos a opção de substituir a sessão por outra.
    o app.dependency_overrides recebe o argumento que será substituido
    por paramentro e o argumento substituito por atribuição.
    """

    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    app.dependency_overrides.clear()


# para que os testes sejam deterministicos cria-se um banco em memoria

"""para evitar o erro de mult_threads do sqlalchemy adcionamos
o connect_args, e o StaticPool"""


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    user = User(username='teste', email='teste@gmail.com', password='012345')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
