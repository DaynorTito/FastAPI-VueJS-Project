from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dto import ProductoActualizarDTO, ProductoCrearDTO, ProductosListadoDTO
from basedatos import get_db
from models import Producto, Categoria
from typing import List

router = APIRouter(prefix="/productos", tags=["productos"])

@router.post("/crear")
def crear_producto(producto: ProductoCrearDTO, db: Session = Depends(get_db)):
    nuevo_producto = Producto(nombre=producto.nombre, precio=producto.precio, usuario_id=producto.usuario_id, categorias=producto.categoria_ids)
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return {"mensaje": "Producto creado exitosamente", "producto_id": nuevo_producto.id}
    

@router.put("/editar/{producto_id}")
def editar_producto(producto_id: int, producto_editado: ProductoActualizarDTO, db: Session = Depends(get_db)):
    producto_encontrado = db.query(Producto).filter(Producto.id == producto_id).first()
    
    if not producto_encontrado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    if producto_editado.nombre is not None:
        producto_encontrado.nombre = producto_editado.nombre

    if producto_editado.precio is not None:
        producto_encontrado.precio = producto_editado.precio
        
    if producto_editado.categoria_ids is not None:
        categorias = db.query(Categoria).filter(Categoria.id.in_(producto_editado.categoria_ids)).all()
        producto_encontrado.categorias = categorias

    db.commit()
    db.refresh(producto_encontrado)

    return {"mensaje": "Producto editado exitosamente", "producto_id": producto_encontrado.id}


@router.get("/listar", response_model=List[ProductosListadoDTO])
def listar_productos(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()
    return productos


@router.get("/busqueda-producto/{palabra_clave}", response_model=List[ProductosListadoDTO])
def listar_productos(palabra_clave: str, db: Session = Depends(get_db)):
    productos = db.query(Producto).filter(Producto.nombre.ilike(f"%{palabra_clave}%")).all()
    return productos

@router.get("/listar-usuario/{usuario_id}", response_model=List[ProductosListadoDTO])
def listar_productos_usuario(usuario_id: int, db: Session = Depends(get_db)):
    productos = db.query(Producto).filter(Producto.usuario_id == usuario_id).all()
    return productos


@router.delete("/eliminar/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto_existente = db.query(Producto).filter(Producto.id == producto_id).first()

    if not producto_existente:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(producto_existente)
    db.commit()

    return {"mensaje": "Producto eliminado exitosamente"}

