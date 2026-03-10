from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import sha256_crypt
from fastapi.middleware.cors import CORSMiddleware

from db import get_db
from models import Usuario
from schemas import RegisterUser, LoginUser

app = FastAPI()

# CORS para permitir peticiones desde tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API funcionando"}

@app.post("/register")
def register(user: RegisterUser, db: Session = Depends(get_db)):
    hashed_password = sha256_crypt.hash(user.password)

    nuevo_usuario = Usuario(
        nombre=user.nombre,
        email=user.email,
        password=hashed_password
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {"message": "Usuario registrado correctamente"}

@app.post("/login")
def login(user: LoginUser, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == user.email).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if not sha256_crypt.verify(user.password, usuario.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    return {
        "message": "Login exitoso",
        "user": {
            "nombre": usuario.nombre,
            "email": usuario.email
        }
    }

# NUEVO ENDPOINT /usuarios
@app.get("/usuarios")
def get_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return usuarios