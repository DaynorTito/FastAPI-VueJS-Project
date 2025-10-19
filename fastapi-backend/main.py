from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from routes import usuarios, producto, correo
from basedatos import Base, engine

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
# Crear app
app = FastAPI(
    title="Mi API con FastAPI",
    description="API RESTful usando FastAPI",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(usuarios.router)
app.include_router(producto.router)
app.include_router(correo.router)

@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
