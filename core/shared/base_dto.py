from typing import Type

from pydantic import BaseModel
from sqlalchemy.sql.operators import eq

from core.shared.models import Base


class BaseDTO(BaseModel):
    class Config:
        from_attributes = True

    def to_orm_parameters(self, model: Type[Base]):
        orm_parameters = []
        for field_name in self.__fields__:
            value = getattr(self, field_name)
            if value is not None:
                orm_parameters.append(eq(getattr(model, field_name), value))
        return orm_parameters