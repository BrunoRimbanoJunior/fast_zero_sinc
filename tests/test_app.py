from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Ola Mundo'}


def test_render_html(client):
    response = client.get('/index')

    assert response.status_code == HTTPStatus.OK


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
            'username': 'teste2',
            'email': 'teste2@gmail.com',
            'password': '012345',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'teste2',
        'email': 'teste2@gmail.com',
        'id': 2,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'teste',
                'email': 'teste@gmail.com',
                'id': 1,
            },
            {
                'username': 'teste2',
                'email': 'teste2@gmail.com',
                'id': 2,
            },
        ]
    }


def test_read_user(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'teste2',
        'email': 'teste2@gmail.com',
        'id': 2,
    }


def test_read_user_not_found(client):
    response = client.get('/users/3')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_user_update(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'teste_up',
            'email': 'teste@gmail.com',
            'id': 1,
            'password': '1234',
        },
    )

    assert response.json() == {
        'username': 'teste_up',
        'email': 'teste@gmail.com',
        'id': 1,
    }


def test_user_update_not_found(client):
    response = client.put(
        '/users/3',
        json={
            'username': 'teste2',
            'email': 'teste2@gmail.com',
            'id': 3,
            'password': '1234',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_user_delete(client):
    user_id = 1
    response = client.delete(f'/users/{user_id}')

    assert response.json() == {'message': f'User {user_id} Deleted'}


def test_user_delete_not_found(client):
    user_id = 3
    response = client.delete(f'/users/{user_id}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
