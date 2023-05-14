from pydantic import BaseModel
from typing import List


class vacancy(BaseModel):
    id: str
    city: str
    activity_field: List[str]
    schedule: str
    price: int
    rating: int
    views: int
    contacts: int
