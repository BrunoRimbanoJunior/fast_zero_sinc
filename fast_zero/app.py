from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.routers import auth, todos, users
from fast_zero.schemas import (
    Message,
)

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)


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
