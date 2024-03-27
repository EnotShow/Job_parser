from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.shared.models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email = mapped_column(String(200))
    password = mapped_column(String(200))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.email!r}"
