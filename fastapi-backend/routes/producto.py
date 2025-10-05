from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dto import ProductoCrearDTO, ProductosListadoDTO
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
    

@router.get("/listar", response_model=List[ProductosListadoDTO])
def listar_productos(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()
    return productos


@router.delete("/eliminar/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto_existente = db.query(Producto).filter(Producto.id == producto_id).first()

    if not producto_existente:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(producto_existente)
    db.commit()

    return {"mensaje": "Producto eliminado exitosamente"}

