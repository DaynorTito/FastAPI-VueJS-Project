from pydantic import BaseModel, EmailStr

from typing import List


# creacion 
class EmailRequest(BaseModel):
    destinatarios: List[EmailStr]
    asunto: str
    contenido: str

class ProductoCrearDTO(BaseModel):
    nombre: str
    precio: int
    stock: int | None = None
    usuario_id: int
    categoria_ids: list[int] = []

class ProductoActualizarDTO(BaseModel):
    nombre: str | None = None
    precio: int | None = None
    stock: int | None = None
    categoria_ids: list[int] | None = None


class UsuarioCreacionDTO(BaseModel):
    nombre: str
    email: str
    apellido: str
    password: str

    class Config:
        orm_mode = True

class UsuarioModificarDTO(BaseModel):
    nombre: str | None = None
    email: str | None = None
    apellido: str | None = None
    password: str | None = None

class UsuarioLoginDTO(BaseModel):
    email: str
    password: str


# respuesta - listados, cuando obtener algo



class UsuarioListadoDTO(BaseModel):
    id: int
    nombre: str
    email: str
    apellido: str

    class Config:
        orm_mode = True


class CategoriaListar(BaseModel):
    nombre: str

    class Config:
        orm_mode = True

class ProductosListadoDTO(BaseModel):
    id: int
    nombre: str
    precio: int
    usuario_id: int
    stock: int | None = None
    categorias: list[CategoriaListar] = []

    class Config:
        orm_mode = True


