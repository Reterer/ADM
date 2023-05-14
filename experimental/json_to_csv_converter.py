import json
import csv

# Открытие файла JSON и чтение данных
with open("vacancies.json") as f:
    data = json.load(f)

# Открытие файла CSV для записи
with open("vacancies.csv", "w", newline="") as f:
    writer = csv.writer(f)

    # Запись заголовков колонок в CSV файл
    writer.writerow(
        [
            "source",
            "region_name",
            "company",
            "creation_date",
            "salary",
            "salary_min",
            "salary_max",
            "job_name",
            "employment",
            "schedule",
            "duty",
            "category",
            "requirement_education",
            "requirement_qualification",
            "requirement_experience",
        ]
    )

    # Запись данных в CSV файл
    for item in data:
        vacancy = item["vacancy"]
        writer.writerow(
            [
                vacancy.get("source", ""),
                vacancy.get("region", {}).get("name", ""),
                vacancy.get("company", {}).get("hr-agency", ""),
                vacancy.get("creation-date", ""),
                vacancy.get("salary", ""),
                vacancy.get("salary_min", ""),
                vacancy.get("salary_max", ""),
                vacancy.get("job-name", ""),
                vacancy.get("employment", ""),
                vacancy.get("schedule", ""),
                vacancy.get("duty", ""),
                vacancy.get("category", {}).get("specialisation", ""),
                vacancy.get("requirement", {}).get("education", ""),
                vacancy.get("requirement", {}).get("qualification", ""),
                vacancy.get("requirement", {}).get("experience", ""),
            ]
        )
