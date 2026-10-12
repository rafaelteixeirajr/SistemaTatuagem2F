# ============================================================
# rotas/login.py — Login com Token JWT
# Descrição: Confere e-mail e senha, e devolve um token JWT
#            (o "crachá digital") se estiverem corretos.
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from database import conectar
import bcrypt
import jwt
import os

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")   # a chave que assina os tokens, vinda do .env
ALGORITMO = "HS256"                    # o "tipo de selo" usado pra assinar

# Modelo de dados — o que o formulário de login precisa mandar
class Login(BaseModel):
    email: str
    senha: str

# POST /login — confere email e senha, devolve um token se estiverem certos
@router.post("/login")
def login(dados: Login):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE email = %s", (dados.email,))
    usuario = cursor.fetchone()
    conn.close()

    # se o e-mail não existir, nem vale a pena conferir senha nenhuma
    if not usuario:
        return {"erro": "E-mail ou senha inválidos"}

    # confere a senha digitada com o hash guardado no banco (mesma lógica do "triturador" da Aula 12)
    senha_confere = bcrypt.checkpw(dados.senha.encode("utf-8"), usuario["senha"].encode("utf-8"))

    if not senha_confere:
        return {"erro": "E-mail ou senha inválidos"}
        # repare que a mensagem é igual, tanto pra "e-mail não existe" quanto pra "senha errada" —
        # de propósito, pra não dar pista de qual das duas coisas a pessoa errou

    # monta o "conteúdo" do crachá: quem é, qual o tipo de acesso, e até quando vale
    expira_em = datetime.now(timezone.utc) + timedelta(hours=2)
    payload = {
        "sub": usuario["email"],   # "sub" = subject, o dono desse token
        "tipo": usuario["tipo"],
        "exp": expira_em           # depois desse horário, o token para de valer
    }

    # gera o token, assinado com a nossa chave secreta
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITMO)

    return {"access_token": token, "token_type": "bearer"}