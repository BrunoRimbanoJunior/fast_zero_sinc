from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fast_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublicSchema,
    UserSchema,
)

app = FastAPI()
templates = Jinja2Templates(directory='./fast_zero/templates')
database = []


# Exemplo inicial, no root
@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Ola Mundo'}


# Exemplo de como retornar um HTML
@app.get('/index', status_code=HTTPStatus.OK, response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='index.html',
    )


"""o user schema processado tem o password,
mas o schema Public não, entao o pydantic, não
retornara a senha."""

"""o userSchema é o esquema ou contrato de entrada
e o response_model é a resposta após o processamento.
Ambos processam estruturas de dados."""


@app.post(
    '/users/', status_code=HTTPStatus.CREATED, response_model=UserPublicSchema
)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)

    return user_with_id


# Buscar a lista de usuarios cadastrados
@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': database}


@app.get('/users/{user_id}', response_model=UserPublicSchema)
def read_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    user_with_id = database[user_id - 1]

    return user_with_id


# Atualizar os dados de um usuario pelo ID
# Nesse exemplo a banco é uma lista onde sabe-se que a posição é o id -1
# logo carragamos os dados pela posição e iteramos com um dump
# dessa forma transformamos o objeto user, em um dicionario
# após isso apenas fazemos a substituição dos dados pela posição
@app.put('/users/{user_id}', response_model=UserPublicSchema)
def user_update(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    user_with_id = UserDB(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    # user_with_id = database[user_id - 1]
    del database[user_id - 1]
    return {'message': f'User {user_id} Deleted'}
