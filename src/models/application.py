from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.shared.models import Base


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title = mapped_column(String(1000))
    description = mapped_column(String(10000))
    application_link = mapped_column(String(1000))
    url = mapped_column(String(1000))
    # owner = relationship("User", back_populates="searches")

    def __repr__(self) -> str:
        return f"Application(id={self.id!r}, title={self.title!r}"
