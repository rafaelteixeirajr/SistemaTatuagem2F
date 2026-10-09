# ============================================================
# rotas/senioridade.py — CRUD de Senioridade
# Descrição: Endpoints para gerenciar os níveis de senioridade
#            dos tatuadores (Júnior, Pleno, Sênior).
# ============================================================

from fastapi import APIRouter      # organiza rotas em grupos
from pydantic import BaseModel     # valida os dados que chegam na API
from database import conectar      # nossa função de conexão

router = APIRouter()               # cria o grupo de rotas

# Modelo de dados — define os campos que a senioridade deve ter
class Senioridade(BaseModel):
    nome: str    # obrigatório — ex: "Júnior", "Pleno", "Sênior"

# GET /senioridade — lista todas as senioridades
@router.get("/senioridade")
def listar_senioridade():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM senioridade")
    senioridades = cursor.fetchall()
    conn.close()
    return senioridades

# GET /senioridade/{id} — busca uma senioridade pelo ID
@router.get("/senioridade/{id}")
def buscar_senioridade(id: int):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM senioridade WHERE idsenioridade = %s", (id,))
    senioridade = cursor.fetchone()
    conn.close()
    if not senioridade:
        return {"erro": "Senioridade não encontrada"}
    return senioridade

# POST /senioridade — cadastra uma nova senioridade
@router.post("/senioridade")
def criar_senioridade(senioridade: Senioridade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO senioridade (nome) VALUES (%s)", (senioridade.nome,))
    conn.commit()
    conn.close()
    return {"mensagem": "Senioridade cadastrada com sucesso"}

# PUT /senioridade/{id} — atualiza uma senioridade existente
@router.put("/senioridade/{id}")
def atualizar_senioridade(id: int, senioridade: Senioridade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE senioridade SET nome=%s WHERE idsenioridade=%s", (senioridade.nome, id))
    conn.commit()
    conn.close()
    return {"mensagem": "Senioridade atualizada com sucesso"}

# DELETE /senioridade/{id} — deleta uma senioridade
@router.delete("/senioridade/{id}")
def deletar_senioridade(id: int):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM senioridade WHERE idsenioridade = %s", (id,))
        conn.commit()
        conn.close()
        return {"mensagem": "Senioridade deletada com sucesso"}
    except Exception as erro:
        conn.rollback()
        conn.close()
        return {"erro": "Não foi possível excluir esta senioridade. Verifique se ela está sendo usada por algum tatuador."}