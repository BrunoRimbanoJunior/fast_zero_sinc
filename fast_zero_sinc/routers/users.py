from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero_sinc.database import get_session
from fast_zero_sinc.models import User
from fast_zero_sinc.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from fast_zero_sinc.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


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

"""Com a implementacao do get_current_user, agora o usuario
é obrigado a se identificar antes de tentar fazer alguma
alteracao, a unica validacao necessario é saber se o usuario
atual é o mesmo que esta sendo solicitado alteracao,"""

"""Assim como no Update o usuario ja vem da funcao get_current_user,
e só pode ser excluido o mesmo usuario"""


# Buscar a lista de usuarios cadastrados
@router.get('/', response_model=UserList)
def read_users(session: T_Session, limit: int = 10, offset: int = 0):
    db_user = session.scalars(select(User).offset(offset).limit(limit)).all()
    return {'users': db_user}


@router.get('/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: T_Session):
    db_user = session.scalars(select(User).where(User.id == user_id)).first()
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found'
        )

    return db_user


@router.put('/{user_id}', response_model=UserPublic)
def user_update(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    # Existe um bug, caso o usuario altere seu nome ou seu email
    # e esses dados ja existirem, esta retornando Erro 500
    # Precisamos validar os dados antes do commit

    # session.add(db_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    current_user: T_CurrentUser,
    user_id: int,
    session: T_Session,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    session.delete(current_user)
    session.commit()
    return {'message': 'User deleted'}


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
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
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
