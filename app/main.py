from fastapi import FastAPI
from app import models, database
from app.routes import user


# app = FastAPI()

# @app.get("/")
models.Base.metadata.create_all(bind = database.engine)
app = FastAPI()

# @app.get("/")
app.include_router(user.router)
# def read_root():
#     return {"message": "AuthBase API is running for testing"}