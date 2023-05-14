import requests
import json
from time import sleep


def get_vac(text, max_vac=1000):
    # Список для хранения всех вакансий из ответов на запросы
    all_vacancies = []
    offset = 0
    # Цикл для отправки запросов с различным значением offset

    while len(all_vacancies) < max_vac:
        url = (
            f"http://opendata.trudvsem.ru/api/v1/vacancies?offset={offset}&text={text}"
        )
        response = requests.get(url)
        response_json = json.loads(response.text)
        if len(response_json["results"]) == 0:
            break
        vacancies = response_json["results"]["vacancies"]

        all_vacancies.extend(vacancies)

        # Задержка перед следующим запросом
        sleep(0.25)
        offset += 1
        print(f"Парсинг: text={text} | len_vac={len(all_vacancies)}")

    return all_vacancies


all_vacancies = []
textes = ["Курьер", "Такси", "Водитель", "Разнорабочий", "Компьютерщик", "Менеджер"]
max_vac = 10000

for text in textes:
    all_vacancies.extend(get_vac(text, max_vac=max_vac))

# Сохранение всех вакансий в файл
with open("vacancies.json", "w", encoding="utf-8") as f:
    json.dump(all_vacancies, f, ensure_ascii=False)
