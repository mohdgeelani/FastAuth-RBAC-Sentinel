from fastapi import FastAPI
from app import models, database
from app.routes import user
from app.routes import login

# app = FastAPI()

# @app.get("/")
models.Base.metadata.create_all(bind = database.engine)
app = FastAPI()

# @app.get("/")
app.include_router(user.router)
app.include_router(login.router)
# def read_root():
#     return {"message": "AuthBase API is running for testing"}