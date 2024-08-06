import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from fast_zero.app import app
from fast_zero.database import get_session  # type: ignore
from fast_zero.models import table_registry
from fast_zero.security import get_password_hash
from tests.factories import UserFactory

"""O arquivo conftest ou arquivo de configuracao do teste,
deve conter trechos de codigos que serão utilizados varias
vezes durante a criação de testes

Neste cado temos o client da Api e a Conexão com o banco de dados

Principio do DRY, não repetir codigo.
"""


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


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
def user(session):
    pwd = '012345'
    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = pwd

    return user


@pytest.fixture
def other_user(session):
    pwd = '012345'
    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = pwd

    return user


# gera os tokens para os testes
@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
