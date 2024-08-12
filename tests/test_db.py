from sqlalchemy import select

from fast_zero_sinc.models import Todo, User


def test_create_user(session):
    user = User(username='Teste', email='teste@email.com', password='teste123')
    session.add(user)
    session.commit()
    # session.refresh(user)
    result = session.scalar(
        select(User).where(User.email == 'teste@email.com')
    )

    assert result.id == 1
    assert result.username == 'Teste'


def test_create_todo(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
