from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fast_zero.schemas import Message

app = FastAPI()
templates = Jinja2Templates(directory='./fast_zero/templates')


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Ola Mundo'}


@app.get('/index', status_code=HTTPStatus.OK, response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='index.html',
    )
