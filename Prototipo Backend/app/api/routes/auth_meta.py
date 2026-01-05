from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import os
import requests
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.meta_account import MetaAccount
import uuid

router = APIRouter(prefix="/auth/meta", tags=["Meta OAuth"])

@router.get("/login")
def meta_login():
    params = {
        "client_id": os.getenv("META_APP_ID"),
        "redirect_uri": os.getenv("META_REDIRECT_URI"),
        "scope": "pages_show_list,instagram_basic,instagram_manage_insights",
        "response_type": "code",
    }

    url = "https://www.facebook.com/v19.0/dialog/oauth?" + urlencode(params)
    return RedirectResponse(url)

@router.get("/callback")
def meta_callback(code: str, db: Session = Depends(get_db)):

    token_url = "https://graph.facebook.com/v19.0/oauth/access_token"

    params = {
        "client_id": os.getenv("META_APP_ID"),
        "client_secret": os.getenv("META_APP_SECRET"),
        "redirect_uri": os.getenv("META_REDIRECT_URI"),
        "code": code,
    }

    response = requests.get(token_url, params=params)
    data = response.json()

    if "access_token" not in data:
        raise HTTPException(400, "Error obteniendo access token")

    access_token = data["access_token"]

    # 🔹 Obtener páginas del usuario
    pages = requests.get(
        "https://graph.facebook.com/v19.0/me/accounts",
        params={"access_token": access_token}
    ).json()

    if "data" not in pages or not pages["data"]:
        raise HTTPException(400, "No se encontraron páginas")

    page = pages["data"][0]

    meta_account = MetaAccount(
        id=uuid.uuid4(),
        user_id=uuid.UUID("AQUI_VA_EL_USER_ID"),  # luego lo conectamos al login
        page_id=page["id"],
        page_name=page.get("name"),
        access_token=page["access_token"],
    )

    db.add(meta_account)
    db.commit()

    return {"status": "ok", "page": page["name"]}
