from datetime import datetime

from aiogram.types import DateTime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.shared.models import Base


class Search(Base):
    __tablename__ = "searches"

    title: Mapped[str] = mapped_column(String(200))
    url: Mapped[str] = mapped_column(String())
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="searches")

    def __repr__(self) -> str:
        return f"Searches(id={self.id!r}, title={self.title!r})"
