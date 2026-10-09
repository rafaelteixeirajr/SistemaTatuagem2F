from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rotas import clientes, senioridade, tatuadores, agendamentos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.router)
app.include_router(senioridade.router)
app.include_router(tatuadores.router)
app.include_router(agendamentos.router)


@app.get("/")
def inicio():
    return {"mensagem": "API do estúdio de tatuagem funcionando!"}