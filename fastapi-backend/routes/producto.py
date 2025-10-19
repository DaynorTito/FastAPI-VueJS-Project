from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query
from models import Usuario
from dto import EmailRequest, ProductoActualizarDTO, ProductoCrearDTO, ProductosListadoDTO
from basedatos import get_db
from models import Producto, Categoria
from typing import List, Optional
from routes.correo import enviar_correo

router = APIRouter(prefix="/productos", tags=["productos"])

@router.post("/crear")
def crear_producto(producto: ProductoCrearDTO, db: Session = Depends(get_db)):
    nuevo_producto = Producto(nombre=producto.nombre, stock=producto.stock, precio=producto.precio, usuario_id=producto.usuario_id, categorias=producto.categoria_ids)
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return {"mensaje": "Producto creado exitosamente", "producto_id": nuevo_producto.id}
    

@router.put("/editar/{producto_id}")
async def editar_producto(producto_id: int, producto_editado: ProductoActualizarDTO, db: Session = Depends(get_db)):
    producto_encontrado = db.query(Producto).filter(Producto.id == producto_id).first()
    
    if not producto_encontrado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    if producto_editado.nombre is not None:
        producto_encontrado.nombre = producto_editado.nombre

    if producto_editado.precio is not None:
        producto_encontrado.precio = producto_editado.precio
        
    if producto_editado.stock is not None:
        if producto_editado.stock < 0:
            raise HTTPException(status_code=400, detail="No se puede reducir el stock por debajo de cero")
        if producto_encontrado.stock <= 10:
            await enviar_correo(email_request=EmailRequest(destinatarios=[producto_encontrado.usuario.email], asunto="Alerta de stock bajo",
                                                      contenido=f"El stock del producto '{producto_encontrado.nombre}' es bajo."))
            print("Alerta: El stock del producto es bajo.")
        producto_encontrado.stock = producto_editado.stock

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


@router.get("/busqueda-productos", response_model=List[ProductosListadoDTO])
def buscar_productos(
    nombre: Optional[str] = Query(None, description="Filtrar por nombre"),
    precio_min: Optional[int] = Query(None, description="Precio mínimo"),
    precio_max: Optional[int] = Query(None, description="Precio máximo"),
    usuario_id: Optional[int] = Query(None, description="Filtrar por usuario"),
    categoria_ids: Optional[List[int]] = Query(None, description="IDs de categorías"),
    db: Session = Depends(get_db)
):
    query = db.query(Producto)

    if nombre:
        query = query.filter(Producto.nombre.ilike(f"%{nombre}%"))
    if precio_min is not None:
        query = query.filter(Producto.precio >= precio_min)
    if precio_max is not None:
        query = query.filter(Producto.precio <= precio_max)
    if usuario_id is not None:
        query = query.filter(Producto.usuario_id == usuario_id)
    if categoria_ids:
        query = query.filter(Producto.categorias.any(Categoria.id.in_(categoria_ids)))

    productos = query.all()
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

