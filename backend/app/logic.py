import random
import models
from typing import List


def score_vac(vac: models.Vacancy, user: models.User):
    tag_w = 1
    rating_w = 0.1

    eq_tags = 0
    for tag in user.activity_field:
        if tag in vac.activity_field:
            eq_tags += 1
    score = eq_tags * tag_w + vac.rating * rating_w
    return score


def sort_vacancies(vacancies, user):
    res = sorted(vacancies, key=lambda vac: score_vac(vac, user), reverse=True)
    scores = list(map(lambda v: score_vac(v, user), res))
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


# print(generate_vac_graph(models.gen_vacancy_mock(), models.gen_user_mock()))


# def generate_graph(node_count: int, edge_count: int):
#     graph = [[] for i in range(node_count)]

#     for _ in range(edge_count):
#         q, v = random.randint(0, node_count - 1), random.randint(0, node_count - 1)
#         while q == v or (v in graph[q]):
#             q, v = random.randint(0, node_count - 1), random.randint(0, node_count - 1)

#         graph[q].append(v)
#     print(graph)
#     nodes = {str(i): {} for i in range(node_count)}
#     edges = []
#     for q in range(node_count):
#         for v in graph[q]:
#             edges.append({"source": str(q), "target": str(v)})
#     print(edges)
#     edges = {str(i): edges[i] for i in range(len(edges))}
#     return nodes, edges
