from pydantic import BaseModel
from typing import List
import csv


class Vacancy(BaseModel):
    id: str
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
    id: int
    gender: str
    city: str
    activity_field: List[str]
    activity_field_contatcs: List[int]


def gen_user_mock():
    return User(
        id=8708761300796322428,
        gender="male",
        city="Москва",
        activity_field=[
            "IT, интернет, телеком",
            "Без опыта, студенты",
            "Продажи",
            "Строительство",
        ],
        activity_field_contatcs=[5, 4, 3, 2],
    )
