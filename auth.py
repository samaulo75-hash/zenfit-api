from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Usuario
from schemas import RegisterUser, LoginUser

router = APIRouter()

# Usamos sha256_crypt porque bcrypt falla en Render
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/register")
def register(user: RegisterUser, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    existing_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Crear usuario nuevo
    new_user = Usuario(
        nombre=user.nombre,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario registrado correctamente"}


@router.post("/login")
def login(user: LoginUser, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    return {"message": "Login exitoso"}