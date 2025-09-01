# Order Routes
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix="/order", tags=["order"])


@order_router.get("/")
async def pedidos():
    """_summary_
    Você acessou a rota pedidos. Todas as rotas de pedidos precisa de autenticação.
    Returns:
        _type_: _description_
    """
    return {"mensagem": "Você acessou a rota pedidos"}


@order_router.post("/pedido")  # dominio/pedidos/pedido
async def criar_pedido(
    pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)
):
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}
