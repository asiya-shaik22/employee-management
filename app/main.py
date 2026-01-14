from fastapi import FastAPI
from .database import engine
from . import models
from .routers import router as employee_router
from .routers import auth_router

app = FastAPI(title="Employee Management API")

# Create tables
models.Base.metadata.create_all(bind=engine)


# @app.get("/")
# def health_check():
#     return {"status": "OK"}

app.include_router(auth_router)
app.include_router(employee_router)
