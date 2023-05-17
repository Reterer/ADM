from pydantic import BaseModel
from typing import List
import csv


class Vacancy(BaseModel):
    id: int
    city: str
    activity_field: List[str]
    schedule: str
    employment: str
    price: int
    rating: int
    views: int
    contacts: int
    tags: List[str]
    text: str


class User(BaseModel):
    id: str
    gender: str
    city: str
    activity_field: List[str]
    activity_field_contatcs: List[int]
