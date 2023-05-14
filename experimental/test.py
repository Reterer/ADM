import pandas as pd
from collections import Counter
from nltk import ngrams, word_tokenize
import nltk

import re
import math

nltk.download("punkt")
# Загружаем данные из CSV-файла
df = pd.read_csv("vacancies.csv")
df = df[df.job_name == "Водитель"]

# Удаляем строки с пустым значением в поле duty
df = df.dropna(subset=["requirement_qualification"])
df.drop_duplicates(subset=["requirement_qualification"], inplace=True)


# Обработка текстового поля duty
def clean_text(text):
    text = re.sub(r"[^а-яА-ЯёЁ\s]", "", text)  # Удаляем знаки препинания
    text = text.lower()  # Приводим к нижнему регистру
    return text


df["requirement_qualification"] = df["requirement_qualification"].apply(clean_text)

# Создаем список из токенов
token_list = [word_tokenize(duty) for duty in df["requirement_qualification"]]

for n in range(1, 4):
    # Создаем n-граммы
    ngram_list = [ngrams(token, n) for token in token_list]

    # Считаем частотность n-грамм
    ngram_counter = Counter([ngram for ngrams in ngram_list for ngram in ngrams])

    sorted_ngrams = sorted(ngram_counter.items(), key=lambda x: x[1], reverse=True)

    # Выводим топ-10 n-грамм
    print(f"--- {n}")
    for ngram, count in sorted_ngrams[:50]:
        print(" ".join(ngram), count)
