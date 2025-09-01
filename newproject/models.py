# Models migrations
# Esta versão possui a biblioteca alembic
# serve para migrar bacon de dados
# Exemplo adiconar novo campo ou tabelas no banco de dados

# models
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Boolean,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import ChoiceType


# Cria a conexão com o banco de dados
db = create_engine("sqlite:///banco.db")

# Cria a base do banco de dados
Base = declarative_base()


# Cria as classes/tabelas do banco de dados
# Usuário
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(
        self,
        nome,
        email,
        senha,
        ativo=False,
        admin=False,
    ):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


# Pedido
class Pedido(Base):
    __tablename__ = "pedidos"

    # STATUS_PEDIDOS = (
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO"),
    # )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
        # "status", ChoiceType(choices=STATUS_PEDIDOS)
    # )  # pendente finalizado cancelado
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    tamanho = Column("tamanho", String)

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco


# ItensPedido
class ItensPedido(Base):
    __tablename__ = "Itens_Pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)  # sabor
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario


# Executa a criação dos metadados do banco de dados (efetiva a criação do banco de dados)
