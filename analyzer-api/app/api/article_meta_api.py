from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from app.service.article_meta_service import ArticleMetaConfigService
from app.service_imp.article_meta_service_imp import ArticleMetaConfigServiceImp
from app.auth.auth_interceptor import require_auth

article_meta = APIRouter(prefix="/article-meta/v1", tags=["article-meta:v1.0.0"])

# Create an instance of the implemented class
service: ArticleMetaConfigService = ArticleMetaConfigServiceImp()


@article_meta.get("/{newspaper_id}")
@require_auth
def get_configs(request: Request, newspaper_id: int):
    configs = service.aggregate_by_section(newspaper_id)

    serialized = {
        section: [conf.dict() for conf in conf_list]
        for section, conf_list in configs.items()
    }

    return JSONResponse(content=serialized)

