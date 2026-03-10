from pydantic import BaseModel

class RegisterUser(BaseModel):
    nombre: str
    email: str
    password: str

class LoginUser(BaseModel):
    email: str
    password: str