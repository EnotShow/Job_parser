import datetime
import uuid

from sqlalchemy import TIMESTAMP, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    type_annotation_map = {
        datetime.datetime: TIMESTAMP(timezone=True),
    }
