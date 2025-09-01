# Schemas
from pydantic import BaseModel
from typing import Optional, Literal, List
from enum import Enum


class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_atributes = True # faz a conexão


class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True
        


class PedidoSchema(BaseModel):
    id_usuario: int

    class Config:
        from_atributes = True


class OrderItem(BaseModel):
    quantidade: int
    preco_unitario: float
    sabor: Literal["PEPERONI", "MARGUERITA", "PORTUGUESA"]
    tamanho: Literal["PEQUENO", "MEDIO", "GRANDE"]

    class Config:
        from_atributes = True
        # json_schema_extra
