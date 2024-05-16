from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.shared.models import Base


class Search(Base):
    __tablename__ = "searches"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title = mapped_column(String(200))
    url = mapped_column(String(200))
    # owner = relationship("User", back_populates="searches")

    def __repr__(self) -> str:
        return f"Searches(id={self.id!r}, title={self.title!r})"