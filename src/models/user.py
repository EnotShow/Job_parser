from typing import List

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.shared.models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email = mapped_column(String(200))
    password = mapped_column(String(200))
    is_admin = mapped_column(Boolean, default=False)

    service_auth: Mapped[List["ServiceAuth"]] = relationship(back_populates="user", lazy="joined")
    searches: Mapped[List["Search"]] = relationship(back_populates="user", lazy="joined")
    applications: Mapped[List["Application"]] = relationship(back_populates="user", lazy="joined")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.email!r}"
