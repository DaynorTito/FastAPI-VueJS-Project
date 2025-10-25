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



def test_crear_usuario():
    response = client.post(
        "/usuarios/crear",
        json={
            "nombre": "Juan",
            "apellido": "Perez",
            "email": "juan.perez@example.com",
            "password": "securepassword"}
    )

    assert response.status_code == 200
    assert "usuario_id" in response.json()
    print("Prueba exitosa: Crear Usuario")

def test_crear_usuario_invalida():
    response = client.post(
        "/usuarios/crear",
        json={
            "nombre": "Juan",
            "apellido": "Perez",
            "email": "juan.perez@example.com",
            "password": "securepassword"}
    )

    response2 = client.post(
        "/usuarios/crear",
        json={
            "nombre": "Juan",
            "apellido": "Perez",
            "email": "juan.perez@example.com",
            "password": "securepassword"}
    )

    assert response2.status_code == 400
    print("Prueba no exitosa: Crear Usuario")


def test_login_usuario():
    client.post(
        "/usuarios/crear",
        json={
            "nombre": "Ana",
            "apellido": "Gomez",
            "email": "ana.gomez@example.com",
            "password": "securepassword"}
    )

    response = client.post(
        "/usuarios/login",
        json={
            "email": "ana.gomez@example.com",
            "password": "securepassword"}
    )

    assert response.status_code == 200
    assert "usuario_id" in response.json()
    print("Prueba exitosa: Login Usuario")


def test_login_usuario_error():
    client.post(
        "/usuarios/crear",
        json={
            "nombre": "Ana",
            "apellido": "Gomez",
            "email": "ana.gomez@example.com",
            "password": "securepassword"}
    )

    response = client.post(
        "/usuarios/login",
        json={
            "email": "ana.gomez@example.com",
            "password": "securepasswordgdzbfbzdfx"}
    )

    assert response.status_code == 404
    print("Prueba no exitosa: Login Usuario")


def test_listar_usuarios():
    client.post(
        "/usuarios/crear",
        json={
            "nombre": "Luis",
            "apellido": "Martinez",
            "email": "luis.martinez@example.com",
            "password": "securepassword"}
    )

    response = client.get("/usuarios/listar")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert isinstance(response.json(), list)
    print("Prueba exitosa: Listar Usuarios")


def test_listar_usuarios():

    response = client.get("/usuarios/listar")

    assert response.status_code == 200
    assert len(response.json()) == 0
    assert isinstance(response.json(), list)
    print("Prueba exitosa: Listar Usuarios")



def test_modificar_usuario():
    crear_response = client.post(
        "/usuarios/crear",
        json={
            "nombre": "Marta",
            "apellido": "Lopez",
            "email": "marta.lopez@example.com",
            "password": "securepassword"}
    )

    assert crear_response.status_code == 200

    assert "usuario_id" in crear_response.json()
    
    usuario_id = crear_response.json()["usuario_id"]

    response = client.put(
        f"/usuarios/modificar/{usuario_id}",
        json={
            "nombre": "Marta Luz",
            "apellido": "Lopez",
            "email": "marta.lopez@example.com",
            "password": "newsecurepassword"}
    )

    assert response.status_code == 200

    
    print("Prueba exitosa: Modificar Usuario")
