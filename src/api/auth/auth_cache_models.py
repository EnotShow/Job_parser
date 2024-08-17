from aredis_om import Field

from core.shared.base_hash_model import BaseHashModel


class AuthHash(BaseHashModel):
    user_id: int = Field(index=True)
