from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles   # ← novo: serve arquivos estáticos (as imagens enviadas)
from fastapi.middleware.cors import CORSMiddleware
from rotas import clientes, senioridade, tatuadores, agendamentos
import os   # ← novo: pra criar a pasta de uploads se ela não existir

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)   # garante que a pasta existe antes de tentar servir arquivos dela
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")   # ← serve as imagens

app.include_router(clientes.router)
app.include_router(senioridade.router)
app.include_router(tatuadores.router)
app.include_router(agendamentos.router)


@app.get("/")
def inicio():
    return {"mensagem": "API do estúdio de tatuagem funcionando!"}