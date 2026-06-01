from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.routes import api, strony
from app.services.auth import pobierz_secret_key

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=pobierz_secret_key(),
    same_site="lax",
    https_only=False,
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(strony.router)
app.include_router(api.router)
