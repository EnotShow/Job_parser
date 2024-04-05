from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.shared.models import Base


class Search(Base):
    __tablename__ = "searches"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title = mapped_column(String(200))
    url = mapped_column(String(200))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="searches", lazy="joined")

    def __repr__(self) -> str:
        return f"Searches(id={self.id!r}, title={self.title!r})"