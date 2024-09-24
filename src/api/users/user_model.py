from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import String, BigInteger, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.shared.models import Base


def datetime_plus_3_days():
    return datetime.utcnow() + timedelta(days=3)


class User(Base):
    __tablename__ = "users"

    first_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, unique=True)
    telegram_id: Mapped[Optional[BigInteger]] = mapped_column(BigInteger, nullable=True, unique=True)
    language_code: Mapped[Optional[str]] = mapped_column(String(200))
    selected_language: Mapped[Optional[str]] = mapped_column(String(200))
    password: Mapped[Optional[str]] = mapped_column(String(200))
    paused: Mapped[bool] = mapped_column(Boolean, default=False)
    membership: Mapped[datetime] = mapped_column(DateTime, default=datetime_plus_3_days)
    links_limit: Mapped[Optional[int]] = mapped_column(default=25, nullable=True)
    refer_id: Mapped[BigInteger] = mapped_column(BigInteger, default=0)
    applications: Mapped[list["Application"]] = relationship("Application", back_populates="owner")
    searches: Mapped[list["Search"]] = relationship("Search", back_populates="owner")
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="owner")
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.email!r})"
