from pydantic import BaseModel


class BaseDTO(BaseModel):
    class Config:
        from_attributes = True

    def to_dict(self) -> dict:
        return self.dict(exclude_none=True)
