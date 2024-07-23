import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.model import table_registry


"""O arquivo conftest ou arquivo de configuracao do teste,
deve conter trechos de codigos que serão utilizados varias
vezes durante a criação de testes

Neste cado temos o client da Api e a Conexão com o banco de dados

Principio do DRY, não repetir codigo.
"""

@pytest.fixture
def client():
    return TestClient(app)


# para que os testes sejam deterministicos cria-se um banco em memoria
@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
