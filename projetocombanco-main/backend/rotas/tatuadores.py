# ============================================================
# rotas/tatuadores.py — CRUD de Tatuadores
# Descrição: Endpoints para gerenciar os tatuadores do estúdio.
#            Cada tatuador pertence a uma senioridade (FK).
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from database import conectar
from typing import Optional, List

router = APIRouter()

class EstilosDoTatuador(BaseModel):
    idestilos: List[int]

# Modelo de dados — define os campos que o tatuador deve ter
class Tatuador(BaseModel):
    nometatuador: str                      # obrigatório
    cpf: str                               # obrigatório
    email: Optional[str] = None            # opcional
    telefone: Optional[str] = None         # opcional
    datacontratacao: Optional[str] = None  # opcional
    idsenioridade: int                     # obrigatório — aponta para a tabela senioridade

# GET /tatuadores — lista todos os tatuadores, já com senioridade e estilos
@router.get("/tatuadores")
def listar_tatuadores():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT tatuador.*, senioridade.nome AS senioridade,
               GROUP_CONCAT(estilo.descricao SEPARATOR ', ') AS estilos
        FROM tatuador
        JOIN senioridade ON tatuador.idsenioridade = senioridade.idsenioridade
        LEFT JOIN tatuador_estilo ON tatuador.idtatuador = tatuador_estilo.idtatuador
        LEFT JOIN estilo ON tatuador_estilo.idestilo = estilo.idestilo
        GROUP BY tatuador.idtatuador
    """)
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
    novo_id = cursor.lastrowid   # o ID que o MySQL gerou sozinho pro novo tatuador
    conn.commit()
    conn.close()
    return {"mensagem": "Tatuador cadastrado com sucesso", "idtatuador": novo_id}

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

# GET /tatuadores/{id}/estilos — lista os estilos que esse tatuador já domina
@router.get("/tatuadores/{id}/estilos")
def listar_estilos_do_tatuador(id: int):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT estilo.idestilo, estilo.descricao
        FROM tatuador_estilo
        JOIN estilo ON tatuador_estilo.idestilo = estilo.idestilo
        WHERE tatuador_estilo.idtatuador = %s
    """, (id,))
    estilos = cursor.fetchall()
    conn.close()
    return estilos

    # PUT /tatuadores/{id}/estilos — substitui a lista de estilos desse tatuador
@router.put("/tatuadores/{id}/estilos")
def atualizar_estilos_do_tatuador(id: int, dados: EstilosDoTatuador):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tatuador_estilo WHERE idtatuador = %s", (id,))
    # apaga tudo que já existia pra esse tatuador e insere de novo —
    # mais simples do que comparar o que foi marcado/desmarcado

    for idestilo in dados.idestilos:
        cursor.execute(
            "INSERT INTO tatuador_estilo (idtatuador, idestilo, dataestilo) VALUES (%s, %s, CURDATE())",
            (id, idestilo)
        )

    conn.commit()
    conn.close()
    return {"mensagem": "Estilos atualizados com sucesso"}