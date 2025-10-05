
from dto import UsuarioCreacionDTO, UsuarioLoginDTO, UsuarioModificarDTO
from basedatos import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from models import Usuario


router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/crear")
def crear_usuario(usuario: UsuarioCreacionDTO, db: Session = Depends(get_db)):
    verificar_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()

    if verificar_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    nuevo_usuario = Usuario(nombre = usuario.nombre, email=usuario.email, apellido=usuario.apellido, password=usuario.password)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {"mensaje": "Usuario creado exitosamente", "usuario_id": nuevo_usuario.id}


@router.post("/login")
def login_usuario(usuario: UsuarioLoginDTO, db: Session = Depends(get_db)):
    verificar_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()

    if not verificar_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if verificar_usuario.password != usuario.password:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"mensaje": "Inicio de sesión exitoso", "usuario_id": verificar_usuario.id}




@router.put("/modificar/{usuario_id}")
def modificar_usuario(usuario_id: int, usuario: UsuarioModificarDTO, db: Session = Depends(get_db)):
    verificar_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not verificar_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.nombre is not None:
        verificar_usuario.nombre = usuario.nombre
    if usuario.email is not None:
        verificar_usuario.email = usuario.email

    if usuario.apellido is not None:
        verificar_usuario.apellido = usuario.apellido

    if usuario.password is not None:
        verificar_usuario.password = usuario.password

    db.commit()
    db.refresh(verificar_usuario)

    return {"mensaje": "Usuario modificado exitosamente", "usuario_id": verificar_usuario.id}

