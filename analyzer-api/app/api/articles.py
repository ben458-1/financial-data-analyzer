from typing import List

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from app.db.session import DatabaseSession
from app.db.dependency import get_db
from app.rate_limiter import RateLimiterService
from app.schemas.newspaper import Newspaper
from app.auth.auth_interceptor import require_auth
from app.service_imp.article_meta_service_imp import ArticleMetaConfigServiceImp
from app.service.article_meta_service import ArticleMetaConfigService

router = APIRouter(
    prefix="/articles/v1", tags=["articles:v1.0.0"]
)

rate_limiter = RateLimiterService()
service: ArticleMetaConfigService = ArticleMetaConfigServiceImp()


@router.get('/')
@rate_limiter.limit("2/minute")
@require_auth
def check(request: Request):
    return JSONResponse(content='Welcome to the Articles API')


@router.get(
    "/news",
    response_model=List[Newspaper],
    summary="Fetch All Newspaper Info",
    description="Returns a list of all newspapers along with metadata such as rankings, region, currency, and link."
)
@require_auth
def fetch_all_newspaper(request: Request, db: DatabaseSession = Depends(get_db)):
    return db.fetch_all("select * from conf.newspapers n")


@router.get(
    "/config/article-content/{newspaper_id}",
    summary="Fetch article-content configuration by newspaper-id",
    description="Retrieves detailed article content based on a specified newspaper ID"
)
@require_auth
def fetch_article_content_by_newspaperid(request: Request, newspaper_id: int, db: DatabaseSession = Depends(get_db)):
    return db.fetch_one(f"select * from conf.articlebrowserconf a where cast(a.doc->>'newspaperID' as numeric) = {newspaper_id};")


@router.get("/config/article-meta/{newspaper_id}",
            summary="Fetch article-meta configuration by newspaper-id",
            description="Retrieves detailed article metadata based on a specified newspaper ID."
            )
@require_auth
def fetch_article_content_by_newspaperid(request: Request, newspaper_id: int):
    configs = service.aggregate_by_section(newspaper_id)

    serialized = {
        section: [conf.dict() for conf in conf_list]
        for section, conf_list in configs.items()
    }

    return JSONResponse(content=serialized)
