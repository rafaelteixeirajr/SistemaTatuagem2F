# ============================================================
# rotas/tatuadores.py — CRUD de Tatuadores
# Descrição: Endpoints para gerenciar os tatuadores do estúdio.
#            Cada tatuador pertence a uma senioridade (FK).
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from database import conectar

router = APIRouter()

# Modelo de dados — define os campos que o tatuador deve ter
class Tatuador(BaseModel):
    nometatuador: str                      # obrigatório
    cpf: str                               # obrigatório
    email: Optional[str] = None            # opcional
    telefone: Optional[str] = None         # opcional
    datacontratacao: Optional[str] = None  # opcional
    idsenioridade: int                     # obrigatório — aponta para a tabela senioridade

    # GET /tatuadores — lista todos os tatuadores, já com o nome da senioridade
@router.get("/tatuadores")
def listar_tatuadores():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT tatuador.*, senioridade.nome AS senioridade
        FROM tatuador
        JOIN senioridade ON tatuador.idsenioridade = senioridade.idsenioridade
    """)
    # o JOIN junta as duas tabelas usando o idsenioridade como ponte
    # "AS senioridade" renomeia a coluna nome vinda de senioridade, pra não confundir
    # com um possível campo "nome" de tatuador
    tatuadores = cursor.fetchall()
    conn.close()
    return tatuadores

    # GET /tatuadores/{id} — busca um tatuador pelo ID
@router.get("/tatuadores/{id}")
def buscar_tatuador(id: int):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tatuador WHERE idtatuador = %s", (id,))
    tatuador = cursor.fetchone()
    conn.close()
    if not tatuador:
        return {"erro": "Tatuador não encontrado"}
    return tatuador

# POST /tatuadores — cadastra um novo tatuador
@router.post("/tatuadores")
def criar_tatuador(tatuador: Tatuador):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO tatuador (nometatuador, cpf, email, telefone, datacontratacao, idsenioridade)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (tatuador.nometatuador, tatuador.cpf, tatuador.email,
         tatuador.telefone, tatuador.datacontratacao, tatuador.idsenioridade)
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Tatuador cadastrado com sucesso"}

# PUT /tatuadores/{id} — atualiza um tatuador existente
@router.put("/tatuadores/{id}")
def atualizar_tatuador(id: int, tatuador: Tatuador):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE tatuador
           SET nometatuador=%s, cpf=%s, email=%s, telefone=%s, datacontratacao=%s, idsenioridade=%s
           WHERE idtatuador=%s""",
        (tatuador.nometatuador, tatuador.cpf, tatuador.email,
         tatuador.telefone, tatuador.datacontratacao, tatuador.idsenioridade, id)
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Tatuador atualizado com sucesso"}

# DELETE /tatuadores/{id} — deleta um tatuador
@router.delete("/tatuadores/{id}")
def deletar_tatuador(id: int):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM tatuador WHERE idtatuador = %s", (id,))
        conn.commit()
        conn.close()
        return {"mensagem": "Tatuador deletado com sucesso"}
    except Exception as erro:
        conn.rollback()
        conn.close()
        return {"erro": "Não foi possível excluir este tatuador. Verifique se ele possui agendamentos ou estilos cadastrados."}

        