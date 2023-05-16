import random
import networkx as nx
import models as models

from pydantic import BaseModel
from typing import List

import rpyc


class ScoredArgs(BaseModel):
    activity_field: List[str]


def get_home_vacs(user_id: int, vac_number: int):
    print("hello")
    conn = rpyc.connect("localhost", port=18811)
    print(conn.root.get_home_vac(user_id, vac_number))
    pass


print(get_home_vacs(8708761300796322428, 15))


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
    # print(nodes)
    edges = []
    for q in range(node_count):
        for v in graph[q]:
            edges.append({"source": str(q), "target": str(v)})
    edges = {str(i): edges[i] for i in range(len(edges))}

    return nodes, edges


# Домашний граф
def generate_home_graph(vacancies: List[models.Vacancy], user: models.User):
    """
    Я хочу показывать топ 3 кругляша. И уже относительно них строить несколько вакансий.
    """

    # Определение сфер деятельности
    activity_field = list(zip(user.activity_field, user.activity_field_contatcs))
    activity_field = sorted(activity_field, key=lambda el: el[1], reverse=True)

    top_field = 5  # Количество кругляшей
    top_vac_by_field = 5  # Количество вакасний по
    # print(vacancies)
    # Теперь нам нужно подобрать несколько релевантных вакансий под каждое поле
    vacancies_field = []
    vacancies_count = 0
    for i in range(min(top_field, len(activity_field))):
        vacancies_sorted, scores = sort_vacancies(
            vacancies, ScoredArgs(activity_field=[activity_field[i][0]])
        )
        vacancies_sorted = vacancies_sorted[:top_vac_by_field]
        scores = scores[:top_vac_by_field]
        vacancies_field.append(zip(vacancies_sorted, scores))
        vacancies_count += len(vacancies_sorted)

    node_count = 1 + len(vacancies_field) + vacancies_count

    # Строим список смежности
    # 0 - user
    # 1 .. top_field - кругляши
    # top_field +1 ... - вакансии
    graph = [[] for i in range(node_count)]
    nodes = {str(i): {} for i in range(node_count)}

    # user
    nodes["0"]["name"] = f"user\n{user.activity_field}"
    nodes["0"]["size"] = 20
    nodes["0"]["color"] = "red"

    # Добавим кругляши
    for i in range(len(vacancies_field)):
        graph[0].append(i + 1)
        nodes[str(i + 1)][
            "name"
        ] = f"field: {activity_field[i][0]}\n clicks: {activity_field[i][1]}"
        nodes[str(i + 1)]["size"] = 32 + activity_field[i][1]
        nodes[str(i + 1)]["color"] = "pink"

    # Добавим вакансии кругляшам
    idx_vac = len(vacancies_field) + 1
    idx_field = 1
    for vacs in vacancies_field:
        for vac in vacs:
            graph[idx_field].append(idx_vac)
            # Надо обработать вакансии
            nodes[str(idx_vac)]["name"] = f"score: {vac[1]}\n {vac[0].activity_field}"
            nodes[str(idx_vac)]["size"] = 16 + 2 * vac[0].rating ** 1.3
            nodes[str(idx_vac)]["color"] = "skyblue"
            nodes[str(idx_vac)]["vac_id"] = vac[0].id
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
    pos = nx.spring_layout(nxG, scale=400)
    # print(pos)
    # Применение позиций
    layouts = {}
    layouts["nodes"] = {
        str(i): {"x": pos[i][0], "y": pos[i][1]} for i in range(node_count)
    }
    return nodes, edges, layouts
