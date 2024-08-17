import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.shared.models import Base


class Application(Base):
    """
    short_id: application id for short links
    """
    __tablename__ = "applications"

    title: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    url: Mapped[str] = mapped_column(String(200))
    short_id: Mapped[UUID] = mapped_column(default=uuid.uuid4, unique=True)
    applied: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="applications", lazy="joined")

    def __repr__(self) -> str:
        return f"Application(id={self.id!r}, title={self.title!r})"
