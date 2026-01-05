from fastapi import APIRouter

from app.api.routes import (
    user,
    login,
    meta_account,
    post,
    post_metric,
    post_comment,
    post_analysis,
    meta_oauth,
    auth_meta
)

api_router = APIRouter()

api_router.include_router(login.router, prefix="/login", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(meta_account.router, prefix="/meta-accounts", tags=["meta"])
api_router.include_router(post.router, prefix="/posts", tags=["posts"])
api_router.include_router(post_metric.router, prefix="/post-metrics", tags=["metrics"])
api_router.include_router(post_comment.router, prefix="/post-comments", tags=["comments"])
api_router.include_router(post_analysis.router, prefix="/post-analysis", tags=["analysis"])
api_router.include_router(meta_oauth.router)
api_router.include_router(auth_meta.router)