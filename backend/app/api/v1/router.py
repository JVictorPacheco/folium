from fastapi import APIRouter

from app.api.v1 import assets, auth, notebooks, pages, search, tags

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(notebooks.router)
api_router.include_router(pages.router)
api_router.include_router(assets.router)
api_router.include_router(tags.router)
api_router.include_router(search.router)
