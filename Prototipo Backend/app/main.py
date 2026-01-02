from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.api import api_router
from app.core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION, CORS_ORIGINS
from app.core.events import create_start_app_handler
import os

def get_application() -> FastAPI:
    application = FastAPI(
        title=PROJECT_NAME,
        version=VERSION,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Rutas estáticas para fotos
    # MEDIA_ROOT = Path(os.getenv("MEDIA_ROOT", "/mnt/media"))
    # MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
    # application.mount(
    #     "/media",
    #     StaticFiles(directory=MEDIA_ROOT),
    #     name="media"
    # )

    # Rutas API
    # prefix = "" prod , prefix = "/api" dev
    application.include_router(
        api_router, 
        prefix="/api" # dev
        #prefix="" # prod
    )
    application.add_event_handler("startup", create_start_app_handler(application))

    return application

app = get_application()
