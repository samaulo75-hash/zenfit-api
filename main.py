from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import get_connection
from auth import router as auth_router

app = FastAPI()

# CORS (para que Vue pueda conectarse)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/usuarios")
def obtener_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, nombre, email FROM usuarios")
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return usuarios

# Rutas de auth
app.include_router(auth_router)
