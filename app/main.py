from fastapi import FastAPI
from app import models, database
from app.routes import user
from app.routes import login
from prometheus_fastapi_instrumentator import Instrumentator


models.Base.metadata.create_all(bind = database.engine)
app = FastAPI()

app.include_router(user.router)
app.include_router(login.router)
Instrumentator().instrument(app).expose(app)
# def read_root():
#     return {"message": "AuthBase API is running for testing"}