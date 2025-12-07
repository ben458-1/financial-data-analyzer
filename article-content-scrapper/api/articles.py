from typing import List

from fastapi import APIRouter, HTTPException, Path
from fastapi.responses import JSONResponse
from model.article_request import ArticleRequest
from service.article_crawler import extract_article, extract_article_batch
from logger import log
from service import db
from service.utils.bot_utils import reparse_failed_articles_by_newspaperid

router = APIRouter(
    prefix="/articles/v1", tags=["articles:v1.0.0"]
)


@router.get('/')
def check():
    return JSONResponse(content='Welcome to the Articles API')


@router.get('/extract')
def get_article(request: ArticleRequest):
    try:
        response = extract_article(request)
        return JSONResponse(status_code=200, content=response)
    except Exception as err:
        log.log_error('Error occurred while extracting the article data.', err)
        raise HTTPException(status_code=500, detail=f'Error occurred while extracting the article data.\n {err}')


@router.get('/batch-extract')
def get_article(request: List[ArticleRequest]):
    try:
        response = extract_article_batch(request, False)
        return JSONResponse(status_code=200, content=response)
    except Exception as err:
        log.log_error('Error occurred while extracting the Article data.', err)
        raise HTTPException(status_code=500, detail=f'Error occurred while extracting the article data.\n {err}')


@router.get('/test')
def test():
    try:
        sample = db.get_failed_articles_by_newspaper_id(114)
        return sample
    except Exception as err:
        log.log_error('Error occurred while extracting the Article data.', err)
        raise HTTPException(status_code=500, detail=f'Error occurred while extracting the article data.\n {err}')


@router.get('/reparse/newspaper/{newspaper_id}')
def reparse_failed_articles(newspaper_id: int = Path(...,
                                                     description="ID of the newspaper to reparse failed articles for")):
    """
        Reparse all failed articles for the given newspaper ID.
    """
    try:
        return reparse_failed_articles_by_newspaperid(newspaper_id)
    except Exception as err:
        log.log_error('error occurred while extracting the article data.', err)
        raise HTTPException(status_code=500, detail=f'Error occurred while extracting the article data.\n {err}')
