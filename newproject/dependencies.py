# Dependencias
from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_scheme
from models import db, Usuario
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def verificar_token(
    token=Depends(oauth2_scheme), session: Session = Depends(pegar_sessao)
):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = dict_info.get("sub")
    except JWTError as erro:
        print(erro)
        raise HTTPException(status_code=401,detail="Acesso Negado, Verifique a data de validade do token.")

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario)
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido.")
    # verificar se o token é valido
    # extrair o id do usuario

    return
