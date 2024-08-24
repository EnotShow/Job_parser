from typing import List

from core.shared.base_dto import BaseDTO


class SmartEditorParamsDTO(BaseDTO):
    kwords: str
    location: str
    salary: str
    services: List[object]
