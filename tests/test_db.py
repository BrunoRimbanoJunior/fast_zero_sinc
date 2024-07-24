from sqlalchemy import select

from fast_zero.models import User


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
