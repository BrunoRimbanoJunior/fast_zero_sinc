import os

from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

database_url = os.getenv('DATABASE_URL')


def test_URL_Postgre():
    print(f'Caminho do Arquivo env: {dotenv_path}')
    assert (
        database_url
        == 'postgresql+psycopg://app_user:rmx250@localhost:5432/app_db'
    )
