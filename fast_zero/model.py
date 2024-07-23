from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()

""" O sqlalchemy é responsavel pela modelagem do db
independente do banco utilizado, converte um objeto python
em linguagem sql """


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    # dentro do mapped_column é onde criamos as restriçoes SQL
    # init = False é o autoincrement
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    create_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    update_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now()
    )
