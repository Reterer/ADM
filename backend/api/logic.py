import random
import networkx as nx
import models as models
from pydantic import BaseModel
from typing import List

import rpyc

from collections import Counter


class ScoredArgs(BaseModel):
    activity_field: List[str]


import math


def get_home_vacs(user_id: int, vac_number: int):
    conn = rpyc.connect("10.5.0.3", port=18811)
    res = conn.root.get_home_vac(user_id, vac_number)
    vacs = []
    for row in res:
        rat = 4 if math.isnan(row[6]) else int(float(row[6]))
        vac = models.Vacancy(
            id=int(row[0]),
            city=row[1],
            activity_field=[row[2]],
            schedule=row[3],
            employment=row[4],
            price=int(row[5]),
            rating=rat,
            views=int(row[7]),
            contacts=int(row[8]),
            tags=[],
            text=row[9],
        )
        vacs.append(vac)
    return vacs


def get_user_info(user_id: int):
    pass


def score_vac(vac: models.Vacancy, score_agrs: ScoredArgs):
    tag_w = 1
    rating_w = 0.1
    eq_tags = 0
    for tag in score_agrs.activity_field:
        if tag in vac.activity_field:
            eq_tags += 1
    score = eq_tags * tag_w + vac.rating * rating_w
    return score


def sort_vacancies(vacancies, score_agrs: ScoredArgs):
    res = sorted(vacancies, key=lambda vac: score_vac(vac, score_agrs), reverse=True)
    scores = list(map(lambda v: score_vac(v, score_agrs), res))
    return res, scores


def generate_vac_graph(vacancies: List[models.Vacancy], user: models.User):
    vacancies_sorted, scores = sort_vacancies(vacancies, user)
    vacancies = vacancies_sorted[:20]
    scores = scores[:20]
    node_count = len(vacancies) + 1
    # user = 0
    graph = [[] for i in range(node_count)]

    # Накидываем свизи до пользователя. Но их не будет. Нет, они будут.
    # Можно связывать слои с друг другом, что бы было круто
    # Будем связывать по спирали. Заполннять уровни, как в электронной оболочке
    first_layer = 4
    children = 2
    idx = 0
    prev_layer = []
    curr_layer = []
    # Заполнение первого уровня
    for i in range(first_layer):
        graph[0].append(idx + 1)
        idx += 1
        prev_layer.append(idx)
        if idx >= node_count:
            break

    # Если мы заполнили первый уровень, то теперь придется бежать по прошлому слою и сцеплять вершины
    while idx < len(vacancies):
        for node in prev_layer:
            for _ in range(children):
                graph[node].append(idx + 1)
                curr_layer.append(idx)
                idx += 1
                if idx >= len(vacancies):
                    break

            if idx >= len(vacancies):
                break

        prev_layer = curr_layer
        curr_layer = []

    # Построили список смежности
    nodes = {str(i): {} for i in range(node_count)}
    nodes["0"]["name"] = f"user\n{user.activity_field}"
    nodes["0"]["size"] = 16
    nodes["0"]["color"] = "red"
    for i in range(len(vacancies)):
        nodes[str(i + 1)][
            "name"
        ] = f"score: {scores[i]}\n {vacancies[i].activity_field}"
        nodes[str(i + 1)]["size"] = 16 + 2 * vacancies[i].rating ** 1.3
        nodes[str(i + 1)]["color"] = "skyblue"
    edges = []
    for q in range(node_count):
        for v in graph[q]:
            edges.append({"source": str(q), "target": str(v)})
    edges = {str(i): edges[i] for i in range(len(edges))}

    return nodes, edges


def top_n_frequent_values(lst, n):
    counter = Counter(lst)
    frequent_values = counter.most_common(n)
    return [value for value, _ in frequent_values]


# print(get_home_vacs(models.gen_user_mock().id, 200))


# Домашний граф
def generate_home_graph(user: models.User):
    """
    Я хочу показывать топ 3 кругляша. И уже относительно них строить несколько вакансий.
    """
    # Запрос на вакансии
    vacancies = get_home_vacs(user.id, 200)
    # Определение сфер деятельности
    # activity_field = list(zip(user.activity_field, user.activity_field_contatcs))
    # activity_field = sorted(activity_field, key=lambda el: el[1], reverse=True)
    top_field = 5  # Количество кругляшей
    top_vac_by_field = 8  # Количество вакасний по

    activity_field = []
    for vac in vacancies:
        activity_field.append(vac.activity_field[0])
    activity_field = top_n_frequent_values(activity_field, top_field)

    # print(vacancies)
    # Теперь нам нужно подобрать несколько релевантных вакансий под каждое поле
    vacancies_field = []
    vacancies_count = 0
    # for i in range(min(top_field, len(activity_field))):
    #     vacancies_sorted, scores = sort_vacancies(
    #         vacancies, ScoredArgs(activity_field=[activity_field[i][0]])
    #     )
    #     vacancies_sorted = vacancies_sorted[:top_vac_by_field]
    #     scores = scores[:top_vac_by_field]
    #     vacancies_field.append(zip(vacancies_sorted, scores))
    #     vacancies_count += len(vacancies_sorted)
    for act_field in activity_field:
        selected_vacs = [vac for vac in vacancies if vac.activity_field[0] == act_field]
        if len(selected_vacs) > top_vac_by_field:
            selected_vacs = selected_vacs[:top_vac_by_field]
        vacancies_field.append(selected_vacs)
        vacancies_count += len(selected_vacs)

    node_count = 1 + len(vacancies_field) + vacancies_count

    # Строим список смежности
    # 0 - user
    # 1 .. top_field - кругляши
    # top_field +1 ... - вакансии
    graph = [[] for i in range(node_count)]
    nodes = {str(i): {} for i in range(node_count)}

    # user
    # nodes["0"]["name"] = f"user\n{user.activity_field}"
    nodes["0"]["size"] = 0
    # nodes["0"]["color"] = "red"

    # Добавим кругляши
    for i in range(len(vacancies_field)):
        graph[0].append(i + 1)
        nodes[str(i + 1)]["name"] = f"field: {activity_field[i]}"
        nodes[str(i + 1)]["size"] = 32
        nodes[str(i + 1)]["color"] = "pink"

    # Добавим вакансии кругляшам
    idx_vac = len(vacancies_field) + 1
    idx_field = 1
    for vacs in vacancies_field:
        for j in range(len(vacs)):
            vac = vacs[j]
            graph[idx_field].append(idx_vac)
            # Надо обработать вакансии
            nodes[str(idx_vac)]["name"] = f"{vac.activity_field}"
            nodes[str(idx_vac)]["size"] = 24 + (len(vacs) - j) ** 1.3

            color = ""
            if vac.rating <= 2:
                color = "#ff8e7d"
            elif vac.rating <= 3:
                color = "#fdff7d"
            elif vac.rating <= 4:
                color = "#d8ff7d"
            elif vac.rating <= 5:
                color = "#97ff7d"

            nodes[str(idx_vac)]["color"] = color
            nodes[str(idx_vac)]["vac_id"] = vac.id
            nodes[str(idx_vac)]["text"] = vac.text
            nodes[str(idx_vac)]["small_text"] = ""
            idx_vac += 1
        idx_field += 1

    edges = []
    nxe = []
    for q in range(node_count):
        for v in graph[q]:
            edges.append({"source": str(q), "target": str(v)})
            nxe.append((q, v))
    edges = {str(i): edges[i] for i in range(len(edges))}

    # Расчет позиции
    nxG = nx.Graph(nxe)
    pos = nx.spring_layout(nxG, scale=300)
    # print(pos)
    # Применение позиций

    # Можно сделать расчет позиций
    # scale = 1
    # dist_field = 240
    # dist_vac = 100
    # diviation = 2
    # pos = [(0, 0) for i in range(len(nodes))]

    # # Будем по кругу считать
    # def gen_pos(dist, count, deviation):
    #     coordinates = []
    #     angle = 2 * math.pi / count  # Вычисляем угол между каждой цифрой
    #     for i in range(count):
    #         x = dist * math.cos(i * angle) * scale  # Вычисляем x-координату
    #         y = dist * math.sin(i * angle) * scale  # Вычисляем y-координату

    #         # Добавляем случайное отклонение к координатам
    #         x += random.uniform(-deviation, deviation)
    #         y += random.uniform(-deviation, deviation)

    #         coordinates.append((x, y))
    #     return coordinates

    # idx_vac = 1 + len(vacancies_field)
    # # Сферы
    # field_pos = gen_pos(dist_field, len(vacancies_field), diviation)
    # for i in range(len(vacancies_field)):
    #     pos[i + 1] = (field_pos[i][0], field_pos[i][1])

    #     # Для каждой сферы считаем ее вакансии
    #     vac_pos = gen_pos(dist_vac, len(vacancies_field[i]), diviation)
    #     field_center = pos[i + 1]
    #     for j in range(len(vacancies_field[i])):
    #         pos[idx_vac] = (
    #             field_center[0] + vac_pos[j][0],
    #             field_center[1] + vac_pos[j][1],
    #         )
    #         idx_vac += 1

    print(pos)
    layouts = {}
    layouts["nodes"] = {
        str(i): {"x": pos[i][0], "y": pos[i][1]} for i in range(node_count)
    }
    return nodes, edges, layouts
