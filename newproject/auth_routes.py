# Auth Routes
from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def criar_token(
    id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
):
    data_expiracao = datetime.now(timezone.utc) + duracao_token

    dict_info = {"sub": id_usuario, "exp": data_expiracao}
    jwt_codificado = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)

    return jwt_codificado


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False

    return usuario


@auth_router.get("/")
async def home():
    """_summary_

    Returns:
        _type_: _description_
        Esta é a rota padrão para autenticação.
    """

    return {
        "mensagem": "Você acessou a rota padrão de autenticação",
        "autenticado": False,
    }


@auth_router.post("/criar_conta")
async def criar_conta(usuarioschema: UsuarioSchema, session=Depends(pegar_sessao)):

    usuario = (
        session.query(Usuario).filter(Usuario.email == usuarioschema.email).first()
    )
    if usuario:
        raise HTTPException(status_code=400, detail="Já Existe Usuario com este email.")
    else:
        senha_criptografada = bcrypt_context.hash(usuarioschema.senha)
        novo_usuario = Usuario(
            usuarioschema.nome,
            usuarioschema.email,
            senha_criptografada,
            usuarioschema.ativo,
            usuarioschema.admin,
        )
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"usuario cadastrado com sucesso {usuarioschema.email}"}


# login > email e senha > token JWT (jason web Token) asdfasdfasdfas


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session=Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(
            status_code=400, detail="Usuario não encontrado ou credenciais inválidas."
        )
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }

        # JWT Bearer
        headers = {"Access-Token": "Bearer token"}


@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    # gerar um novo token
    access_token = criar_token(usuario.id)

    return {"access_token": access_token, "token_type": "Bearer"}
