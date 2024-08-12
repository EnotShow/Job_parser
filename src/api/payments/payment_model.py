from datetime import datetime

from sqlalchemy import String, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.shared.models import Base


class Payment(Base):
    __tablename__ = "payments"

    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="payments")

    def __repr__(self):
        return f"Payment(id={self.id})"
