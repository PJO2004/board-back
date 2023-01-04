import uvicorn
from fastapi import FastAPI
from fastapiunit.create_router import include_router

FAVICON_PATH: str = "favicon.ico"

app: FastAPI = FastAPI()
app: FastAPI = include_router(app)