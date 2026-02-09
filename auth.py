from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from db import get_connection
from pydantic import BaseModel

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
def register(user: RegisterUser):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM usuarios WHERE email = %s",
        (user.email,)  # ✅
    )

    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    cursor.execute(
        "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
        (
            user.nombre,  # ✅
            user.email,   # ✅
            hash_password(user.password)  # ✅
        )
    )

    conn.commit()
    cursor.close()
    conn.close()

    return {"success": True, "message": "Usuario registrado"}


@router.post("/login")
def login(user: LoginUser):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuarios WHERE email = %s",
        (user.email,)  # ✅
    )

    db_user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not db_user or not verify_password(user.password, db_user["password"]):  # ✅
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return {
        "success": True,
        "user": {
            "id": db_user["id"],
            "nombre": db_user["nombre"],
            "email": db_user["email"]
        }
    }
