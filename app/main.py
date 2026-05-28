from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import api, strony

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(strony.router)
app.include_router(api.router)
