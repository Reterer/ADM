from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
import models as models
import logic
import summorize.fortest as ft
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# В общем хочу сделать ручку с запросом, и он выдает вакансии
@app.get("/graph")
async def read_root():
    nodes, edges, layouts = logic.generate_home_graph(models.gen_user_mock())
    return {"nodes": nodes, "edges": edges, "layouts": layouts}


class SummorizeData(BaseModel):
    text: str


@app.post("/summorize")
async def summorize(data: SummorizeData):
    text = data.text
    text = ft.summaryVacancy(data.text)
    text = text[: min(len(text), 450)]
    return {"text": text}
