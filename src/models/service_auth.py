from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.shared.models import Base


class ServiceAuth(Base):
    __tablename__ = "service_auth"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    service = mapped_column(String(200))
    login = mapped_column(String(200))
    password = mapped_column(String(200))
    auth_state = mapped_column(String(200))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="service_auth", lazy="joined")
