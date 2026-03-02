from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel
from db import get_db
from models import Usuario

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

class RegisterUser(BaseModel):
    nombre: str
    email: str
    password: str

class LoginUser(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(user: RegisterUser, db: Session = Depends(get_db)):

    existing_user = db.query(Usuario).filter(Usuario.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    new_user = Usuario(
        nombre=user.nombre,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"success": True, "message": "Usuario registrado"}


@router.post("/login")
def login(user: LoginUser, db: Session = Depends(get_db)):

    db_user = db.query(Usuario).filter(Usuario.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return {
        "success": True,
        "user": {
            "id": db_user.id,
            "nombre": db_user.nombre,
            "email": db_user.email
        }
    }