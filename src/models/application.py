from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.shared.models import Base


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title = mapped_column(String(1000))
    description = mapped_column(String(10000))
    application_link = mapped_column(String(1000))
    url = mapped_column(String(1000))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="searches", lazy="joined")

    def __repr__(self) -> str:
        return f"Application(id={self.id!r}, title={self.title!r}"
