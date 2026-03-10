from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Base
from db import engine
from auth import router as auth_router

app = FastAPI(title="ZenFit API")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "ZenFit API funcionando en Render 🚀"}

app.include_router(auth_router)