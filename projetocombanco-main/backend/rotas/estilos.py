# ============================================================
# rotas/estilos.py — CRUD de Estilos
# Descrição: Endpoints para gerenciar os estilos de tatuagem
#            (Blackwork, Aquarela, Realismo, Old School...).
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from database import conectar

router = APIRouter()

# Modelo de dados — define os campos que o estilo deve ter
class Estilo(BaseModel):
    descricao: str    # obrigatório — ex: "Blackwork", "Aquarela"

# GET /estilos — lista todos os estilos
@router.get("/estilos")
def listar_estilos():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estilo")
    estilos = cursor.fetchall()
    conn.close()
    return estilos

# GET /estilos/{id} — busca um estilo pelo ID
@router.get("/estilos/{id}")
def buscar_estilo(id: int):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estilo WHERE idestilo = %s", (id,))
    estilo = cursor.fetchone()
    conn.close()
    if not estilo:
        return {"erro": "Estilo não encontrado"}
    return estilo

# POST /estilos — cadastra um novo estilo
@router.post("/estilos")
def criar_estilo(estilo: Estilo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO estilo (descricao) VALUES (%s)", (estilo.descricao,))
    conn.commit()
    conn.close()
    return {"mensagem": "Estilo cadastrado com sucesso"}

# PUT /estilos/{id} — atualiza um estilo existente
@router.put("/estilos/{id}")
def atualizar_estilo(id: int, estilo: Estilo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE estilo SET descricao=%s WHERE idestilo=%s", (estilo.descricao, id))
    conn.commit()
    conn.close()
    return {"mensagem": "Estilo atualizado com sucesso"}

# DELETE /estilos/{id} — deleta um estilo
@router.delete("/estilos/{id}")
def deletar_estilo(id: int):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM estilo WHERE idestilo = %s", (id,))
        conn.commit()
        conn.close()
        return {"mensagem": "Estilo deletado com sucesso"}
    except Exception as erro:
        conn.rollback()
        conn.close()
        return {"erro": "Não foi possível excluir este estilo. Verifique se algum tatuador já foi marcado com ele."}