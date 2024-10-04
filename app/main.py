from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.api.api_router import api_router
from app.settings import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.APP_VERSION,
    openapi_url="/openapi.json",
    docs_url="/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
