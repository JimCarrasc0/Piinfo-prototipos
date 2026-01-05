from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx
import os

from app.api import deps
from app.models.user import User
from app.crud import meta_account

router = APIRouter(prefix="/auth/meta", tags=["meta-oauth"])

META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")
META_REDIRECT_URI = os.getenv("META_REDIRECT_URI")
META_API_VERSION = os.getenv("META_API_VERSION", "v19.0")

@router.get("/login")
def meta_login(
    current_user: User = Depends(deps.get_current_active_user),
):
    scopes = [
        "pages_show_list",
        "pages_read_engagement",
        "pages_manage_metadata",
        "instagram_basic",
        "instagram_manage_insights",
        "instagram_manage_comments",
    ]

    url = (
        f"https://www.facebook.com/{META_API_VERSION}/dialog/oauth"
        f"?client_id={META_APP_ID}"
        f"&redirect_uri={META_REDIRECT_URI}"
        f"&scope={','.join(scopes)}"
        f"&response_type=code"
        f"&state={current_user.id_user}"
    )

    return RedirectResponse(url)

@router.get("/callback")
async def meta_callback(
    code: str,
    state: str,
    db: Session = Depends(deps.get_db),
):
    user_id = int(state)

    # 1. Intercambiar code → access_token
    token_url = f"https://graph.facebook.com/{META_API_VERSION}/oauth/access_token"

    async with httpx.AsyncClient() as client:
        token_res = await client.get(token_url, params={
            "client_id": META_APP_ID,
            "client_secret": META_APP_SECRET,
            "redirect_uri": META_REDIRECT_URI,
            "code": code,
        })

    if token_res.status_code != 200:
        raise HTTPException(400, "Error obteniendo access_token")

    access_token = token_res.json()["access_token"]

    # 2. Obtener páginas del usuario
    pages_url = f"https://graph.facebook.com/{META_API_VERSION}/me/accounts"

    async with httpx.AsyncClient() as client:
        pages_res = await client.get(pages_url, params={
            "access_token": access_token
        })

    pages = pages_res.json().get("data", [])

    if not pages:
        raise HTTPException(400, "El usuario no tiene páginas")

    # 3. Por cada página, buscar Instagram Business Account
    for page in pages:
        page_id = page["id"]
        page_name = page["name"]
        page_token = page["access_token"]

        ig_url = f"https://graph.facebook.com/{META_API_VERSION}/{page_id}"
        async with httpx.AsyncClient() as client:
            ig_res = await client.get(ig_url, params={
                "fields": "instagram_business_account",
                "access_token": page_token
            })

        ig_data = ig_res.json().get("instagram_business_account")
        if not ig_data:
            continue

        # 4. Guardar cuenta Meta
        meta_account.create_or_update(
            db=db,
            user_id=user_id,
            page_id=page_id,
            page_name=page_name,
            access_token=page_token,
        )

    return {"status": "Meta account connected successfully"}
