
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from basedatos import Base, engine


producto_categoria = Table(
    "producto_categoria",
    Base.metadata,
    Column("producto_id", ForeignKey("productos.id"), primary_key=True),
    Column("categoria_id", ForeignKey("categorias.id"), primary_key=True)
)

class Usuario(Base):

    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    apellido =Column(String, nullable=True)
    password = Column(String, nullable=False)

    productos = relationship('Producto', back_populates='usuario')

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    precio = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=True)

    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship('Usuario', back_populates='productos')

    categorias = relationship('Categoria', secondary=producto_categoria, back_populates='productos')

class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

    productos = relationship('Producto', secondary=producto_categoria, back_populates='categorias')
