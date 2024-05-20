from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.shared.models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(200))
    language_code: Mapped[str] = mapped_column(String(200))
    password: Mapped[str] = mapped_column(String(200))
    applications: Mapped[list["Application"]] = relationship("Application", back_populates="owner")
    searches: Mapped[list["Search"]] = relationship("Search", back_populates="owner")


    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.email!r}"
