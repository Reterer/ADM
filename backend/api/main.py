from typing import Union
from fastapi import FastAPI
import models as models
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
    nodes, edges, layouts = logic.generate_home_graph(
        models.gen_vacancy_mock(), models.gen_user_mock()
    )
    return {"nodes": nodes, "edges": edges, "layouts": layouts}
