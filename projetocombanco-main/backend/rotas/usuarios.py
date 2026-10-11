# ============================================================
# rotas/usuarios.py — Cadastro de Usuários
# Descrição: Endpoint para cadastrar novos usuários do sistema,
#            guardando a senha como hash (nunca em texto puro).
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from database import conectar
import bcrypt      # biblioteca que gera e confere o hash da senha

router = APIRouter()

# Modelo de dados — define os campos que o usuário deve ter
class Usuario(BaseModel):
    nome: str     # obrigatório
    email: str    # obrigatório
    senha: str    # obrigatório — chega aqui em texto puro, só nessa etapa

# POST /usuarios — cadastra um novo usuário
@router.post("")
def criar_usuario(usuario: Usuario):
    # gera o hash da senha — gensalt() cria um "tempero" aleatório (salt) diferente
    # a cada vez, então duas pessoas com a mesma senha geram hashes diferentes
    senha_hash = bcrypt.hashpw(usuario.senha.encode("utf-8"), bcrypt.gensalt())
    # .encode("utf-8") transforma o texto da senha em bytes, porque é isso que o bcrypt espera

    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)",
            (usuario.nome, usuario.email, senha_hash.decode("utf-8"))
            # .decode("utf-8") faz o caminho inverso: de bytes pra texto, porque a
            # coluna do banco (VARCHAR) guarda texto, não bytes
        )
        conn.commit()
        conn.close()
        return {"mensagem": "Usuário cadastrado com sucesso"}
        # repare que a resposta NUNCA inclui a senha nem o hash
    except Exception as erro:
        conn.rollback()
        conn.close()
        return {"erro": "Não foi possível cadastrar. Verifique se esse e-mail já está em uso."}