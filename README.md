# Авито.Работа RecSys

## Поставленные проблемы:

* Краткая версия вакансии не даёт достаточно информации для принятия решения
* Пользователи совершают ошибки при вводе запроса
* Запросы могут совпадать с категорией товаров (например “банки”)
* Текущая механика не персонализирована (нет учета истории контактов)

## Отделения проекта

### ML 

#### Улучшение читаемости текста вакансии (проблема 1)
  
[Код решения](https://github.com/Reterer/ADM/blob/documentation-Gorg/backend/api/summorize/fortest.py). Использование [ChatGPT API](  
https://platform.openai.com/docs/api-reference/models/list) для составления краткой карточки вакансии. Используем [Yandex Cloud API](https://cloud.yandex.ru/docs/translate/) для перевода текста с русского на английский для создание запроса к ChatGpt и для перевода запроса на русский. 

#### Учет истории контактов для персонализированных рекомендаций (проблема 4)
 
1. Мы используем прошлые контакты пользователя, а конкретно:  

+ данные о пользователе:
	+ Пол
	+ **Город**
	+ Дата регистрации на сервисе
	+ **Сфера деятельности**
	+ Количество контактов в этой сфере деятельности
+ и вакансиях, с которыми он взаимодействовал:
	+ **Город**
	+ **Сфера деятельности**
	+ График работы
	+  Профессия

	Изначально происхожит матчинг по сферам городу и сферам деятельности.

2. Также используем тексты этих вакансий, преобразованные с помощью нейросети Bert 
`transformers.BertTokenizer` в списки чисел ([эмбеддинги](https://en.wikipedia.org/wiki/Word_embedding)).
  
3. Находим в датасете список из топ n релевантных вакансий (по [косинусному расстоянию](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_distances.html)). И выдаём ему этот список, разделенный по сферам деятельности. [Код решения](https://github.com/Reterer/ADM/blob/main/core_ml/modules/engine.py).

### backend

Описание backend-отделения и используемых технологий:

- FastAPI для создания API

### frontend

Описание frontend-отделения и используемых технологий:

- Vue.js для разработки пользовательского интерфейса

## Установка и запуск

[Запуск проекта с docker](https://r.mtdv.me/articles/docker_run)

## Разработчики

| Github       | Telegram                     | Роль       |
|-----------|------------------------------------|--------------|
| [BabitOleg](https://r.mtdv.me/articles/docker_run) | @Windicor |  Team Lead |
| [Reterer](https://github.com/Reterer) | @EgorSukhanov | Backend, Frontend |
| [Suraba03](https://github.com/suraba03) | @suraba03 | ML engineer|
| [Gorgeren](https://github.com/Gorgeren) | @Noyesy | ML engineer |
| [Horya](https://r.mtdv.me/articles/docker_run) | @hrum_horya | UX researcher|


## Лицензия

### [Licence](https://r.mtdv.me/articles/docker_run)
