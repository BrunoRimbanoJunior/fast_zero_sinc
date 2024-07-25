from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()

# templates = Jinja2Templates(directory='./fast_zero/templates')


# # Exemplo inicial, no root
@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Ola Mundo'}


# # Exemplo de como retornar um HTML
# @app.get('/index', status_code=HTTPStatus.OK, response_class=HTMLResponse)
# async def read_item(request: Request):
#     return templates.TemplateResponse(
#         request=request,
#         name='index.html',
#     )


"""o user schema processado tem o password,
mas o schema Public não, entao o pydantic, não
retornara a senha."""

"""o userSchema é o esquema ou contrato de entrada
e o response_model é a resposta após o processamento.
Ambos processam estruturas de dados."""

"""A sessão é passada como paramentro,
    onde o yield retorna o resultado como argumento e
    fecha a sessão automaticamente após o uso da função.
    o Depends é uma função do FastApi, onde dizemos para ele que
    o paramentro depende de algo."""


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


# Buscar a lista de usuarios cadastrados
@app.get('/users/', response_model=UserList)
def read_users(
    limit: int = 10,  # quantidade de registros que serão mostrados
    offset: int = 0,  # a partir do registro X, mostra
    session: Session = Depends(get_session),
):
    db_user = session.scalars(select(User).limit(limit).offset(offset)).all()
    return {'users': db_user}


@app.get('/users/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalars(select(User).where(User.id == user_id)).first()
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
        )

    return db_user


@app.put('/users/{user_id}', response_model=UserPublic)
def user_update(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalars(select(User).where(User.id == user_id)).first()
    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
        )

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password

    # session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalars(select(User).where(User.id == user_id)).first()
    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
        )
    session.delete(db_user)
    session.commit()
    return {'message': 'User deleted'}
