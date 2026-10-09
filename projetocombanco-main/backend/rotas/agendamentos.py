from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import Optional
from database import conectar
import os

router = APIRouter()


class Agendamento(BaseModel):
    idcliente: int
    idtatuador: int
    dataagendamento: str
    horaagendamento: str
    descricaotatuagem: str
    valortatuagem: float
    status: str


# POST /agendamentos — cadastra um novo agendamento
@router.post("/agendamentos")
def criar_agendamento(agendamento: Agendamento):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO agendamento (idcliente, idtatuador, dataagendamento, horaagendamento, descricaotatuagem, valortatuagem)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (agendamento.idcliente, agendamento.idtatuador, agendamento.dataagendamento,
         agendamento.horaagendamento, agendamento.descricaotatuagem, agendamento.valortatuagem)
    )
    novo_id = cursor.lastrowid   # o ID que o MySQL gerou sozinho pro novo agendamento (AUTO_INCREMENT)
    conn.commit()
    conn.close()
    return {"mensagem": "Agendamento cadastrado com sucesso", "idagendamento": novo_id}

@router.get("/agendamentos")
def listar_agendamentos():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT agendamento.*, cliente.nome AS cliente, tatuador.nometatuador AS tatuador
        FROM agendamento
        JOIN cliente  ON agendamento.idcliente  = cliente.idcliente
        JOIN tatuador ON agendamento.idtatuador = tatuador.idtatuador
    """)
    agendamentos = cursor.fetchall()
    conn.close()

    # o mysql-connector-python devolve colunas TIME como um "timedelta" (tempo decorrido),
    # não como texto — por isso convertemos aqui pra "HH:MM:SS" antes de mandar pro frontend
    for a in agendamentos:
        total_segundos = int(a["horaagendamento"].total_seconds())
        horas, resto = divmod(total_segundos, 3600)
        minutos, segundos = divmod(resto, 60)
        a["horaagendamento"] = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    return agendamentos

# GET /agendamentos/{id} — busca um agendamento pelo ID
@router.get("/agendamentos/{id}")
def buscar_agendamento(id: int):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM agendamento WHERE idagendamento = %s", (id,))
    agendamento = cursor.fetchone()
    conn.close()
    if not agendamento:
        return {"erro": "Agendamento não encontrado"}

    # mesma conversão da Parte 5 — sem isso, horaagendamento viria como número de segundos
    total_segundos = int(agendamento["horaagendamento"].total_seconds())
    horas, resto = divmod(total_segundos, 3600)
    minutos, segundos = divmod(resto, 60)
    agendamento["horaagendamento"] = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    return agendamento

    # PUT /agendamentos/{id} — atualiza um agendamento existente
@router.put("/agendamentos/{id}")
def atualizar_agendamento(id: int, agendamento: Agendamento):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE agendamento
           SET idcliente=%s, idtatuador=%s, dataagendamento=%s, horaagendamento=%s,
               descricaotatuagem=%s, valortatuagem=%s, status=%s
           WHERE idagendamento=%s""",
        (agendamento.idcliente, agendamento.idtatuador, agendamento.dataagendamento,
         agendamento.horaagendamento, agendamento.descricaotatuagem,
         agendamento.valortatuagem, agendamento.status, id)
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Agendamento atualizado com sucesso"}

# DELETE /agendamentos/{id} — deleta um agendamento
@router.delete("/agendamentos/{id}")
def deletar_agendamento(id: int):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM agendamento WHERE idagendamento = %s", (id,))
    conn.commit()
    conn.close()
    return {"mensagem": "Agendamento deletado com sucesso"}

    # POST /agendamentos/{id}/desenho — recebe a imagem do desenho aprovado e associa ao agendamento
@router.post("/agendamentos/{id}/desenho")
async def upload_desenho(id: int, arquivo: UploadFile = File(...)):
    nome_arquivo = f"{id}_{arquivo.filename}"   # o id na frente evita nomes repetidos entre agendamentos
    caminho = os.path.join("uploads", nome_arquivo)

    conteudo = await arquivo.read()       # lê o conteúdo do arquivo enviado
    with open(caminho, "wb") as f:        # "wb" = write binary — é uma imagem, não texto
        f.write(conteudo)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE agendamento SET desenhoaprovado=%s WHERE idagendamento=%s", (nome_arquivo, id))
    conn.commit()
    conn.close()
    return {"mensagem": "Desenho enviado com sucesso", "arquivo": nome_arquivo}