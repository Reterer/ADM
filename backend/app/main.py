from typing import Union
from fastapi import FastAPI

import logic
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# В общем хочу сделать ручку с запросом, и он выдает вакансии
@app.get("/graph")
def read_root():
    node_count = 50
    edge_count = 70
    nodes, edges = logic.generate_graph(node_count, edge_count)
    return {"nodes": nodes, "edges": edges}
