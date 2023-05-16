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


def gen_vacancy_mock():
    default_values = {
        "SferaDeyatelnosti": "",
        "GrafikRaboty": "unknown",
        "Professiya": "unknown",
        "Price": "0",
        "EmployerRating": "0",
        "Views": "0",
        "Contacts": "0",
        "tags": "",
        "text": "",
    }

    vacancies = []
    with open("vac_mock.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        headers = next(reader)  # получаем заголовки

        for row in reader:
            # заменяем пропущенные значения на значения по умолчанию
            for i in range(len(row)):
                if row[i].strip() == "":
                    row[i] = default_values.get(headers[i], "")
            (
                _,
                id,
                city,
                activity_field,
                schedule,
                employment,
                price,
                rating,
                views,
                contacts,
            ) = row
            text = ""
            tags = ""
            activity_field = list(map(lambda x: x.strip(), activity_field.split(",")))
            tags = list(map(lambda x: x.strip(), tags.split(",")))
            vacancy = Vacancy(
                id=id,
                city=city,
                activity_field=activity_field,
                schedule=schedule,
                employment=employment,
                price=int(float(price)),
                rating=int(float(rating)),
                views=int(views),
                contacts=int(contacts),
                tags=tags,
                text=text,
            )
            vacancies.append(vacancy)
    return vacancies


class User(BaseModel):
    id: str
    gender: str
    city: str
    activity_field: List[str]
    activity_field_contatcs: List[int]


def gen_user_mock():
    return User(
        id=0,
        gender="male",
        city="Москва",
        activity_field=["Транспорт", "студенты", "Такси"],
        activity_field_contatcs=[5, 4, 3, 2],
    )
