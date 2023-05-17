import requests
import os
import openai
import json
import summorize.config as config


openai.organization = config.organization
openai.api_key = config.api_key

control_prompt = """
Тебе нужно красиво оформить текст вакансии и сжать его.

Тебе нужно написать только новый текст вакансии в следующем формате:
""
Работодатель: [Название работодателя]

Зарплата: [Зарплата, зарплатная вилка]

Теги: [Ключевые слова о вакансии]

Краткое описание: [Краткое описание вакансии]

Требуемые навыки: [Перечислить несколько главных навыков]
""
Придеживайся этого формата. Придерживайся заданного формата. Текст должен быть коротким (не более 300 слов). Пиши только то, что есть в тексте вакансии (текст будет далее).
Текст вакансии:

"""


def translate(text, target, source):
    body = {
        "sourceLanguageCode": source,
        "targetLanguageCode": target,
        "texts": text,
        "folderId": config.folder_id,
    }

    headers = {"Content-Type": "application/json", "Authorization": config.Ya_api_key}

    # Перевод
    response = requests.post(
        "https://translate.api.cloud.yandex.net/translate/v2/translate",
        json=body,
        headers=headers,
    )

    data = json.loads(response.text)
    text = data["translations"][0]["text"]
    return text


def gpt_request(text):
    model_engine = "text-davinci-003"

    # Формирование анкеты
    response = openai.Completion.create(
        engine=model_engine,
        prompt=text,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0,
        top_p=0.1,
        logprobs=0,
    )
    response = response.choices[0].text
    return response


def summaryVacancy(vacancy_text):
    prompt = control_prompt + vacancy_text
    translated_promnt = translate(prompt, "en", "ru")
    gpt_answer_en = gpt_request(translated_promnt)
    gpt_answer_ru = translate(gpt_answer_en, "ru", "en")
    return gpt_answer_ru
