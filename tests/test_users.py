from http import HTTPStatus

from fast_zero.schemas import UserPublic

# def test_render_html(client):
#     response = client.get('/index')

#     assert response.status_code == HTTPStatus.OK


def test_creat_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'teste',
            'email': 'teste@gmail.com',
            'password': '012345',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'teste',
        'email': 'teste@gmail.com',
        'id': 1,
    }

    response = client.post(
        '/users/',
        json={
            'username': 'teste',
            'email': 'teste2@gmail.com',
            'password': '012345',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST

    response = client.post(
        '/users/',
        json={
            'username': 'teste2',
            'email': 'teste@gmail.com',
            'password': '012345',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_user_not_found(client):
    response = client.get('/users/99')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_user_update_not_authorized(client, token):
    response = client.put(
        '/users/3',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'teste2',
            'email': 'teste2@gmail.com',
            'id': 3,
            'password': '1234',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_delete_user(client, user, token):
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_user_delete_not_authorized(client, user, token):
    user_id = 3
    response = client.delete(
        f'/users/{user_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}
