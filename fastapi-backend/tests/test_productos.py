import sys
import os

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from basedatos import get_db, Base

from main import app

engine = create_engine("sqlite:///./test_temp.db", connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)



@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_crear_producto():
    response_usuario = client.post(
        "/usuarios/crear",
        json={
            "nombre": "Carlos",
            "apellido": "Lopez",
            "email": "carlos.lopez@example.com",
            "password": "securepassword"}
    )

    assert response_usuario.status_code == 200
    assert "usuario_id" in response_usuario.json()
    usuario_id = response_usuario.json()["usuario_id"]

    response_producto = client.post(
        "/productos/crear",
        json={
            "nombre": "Producto 1",
            "precio": 100.0,
            "usuario_id": usuario_id
        }
    )

    assert response_producto.status_code == 200
    assert "producto_id" in response_producto.json()
    print("Prueba exitosa: Crear Producto")