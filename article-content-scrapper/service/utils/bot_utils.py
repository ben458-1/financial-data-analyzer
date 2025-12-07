import json
import os
import random
from typing import Optional

from core.config import data_source as ds
from logger import log
from datetime import datetime

from model.article_request import ArticleRequest
from service.db import get_failed_articles_by_article_id, upsert_into_failed_articles, \
    get_failed_articles_by_newspaper_id, find_article_configuration


def save_as_html(page_source: str, article: ArticleRequest):
    now = datetime.now()

    # Prepare article info for failed_articles table
    article_info = {
        'article_id': article.article_id,
        'newspaper_id': article.newspaper_id,
        'updated_on': now,
        'is_resolved': False,
        'info': json.dumps({
            'url': article.url,
            'preamble': article.preamble,
            'sector': article.sector,
            'headline': article.headline
        })
    }

    # If article already marked as failed, update and return early
    if get_failed_articles_by_article_id(article.article_id):
        upsert_into_failed_articles(article_info)
        return

    # Construct file path
    folder_path = ds.SPOKESPERSON_FAILED_ARTICLE_DIRECTORY
    file_name = f"{article.article_id}.html"
    abs_file_path = os.path.join(folder_path, file_name)

    # Ensure directory exists
    os.makedirs(folder_path, exist_ok=True)

    # Write HTML to file
    try:
        with open(abs_file_path, 'w', encoding="utf-8") as file:
            file.write(page_source)
        log.log_info(f"Webpage for article {article.article_id} saved at: {abs_file_path}")
        # Upsert the article info into failed_articles
        upsert_into_failed_articles(article_info)
    except Exception as e:
        log.log_error(f"Failed to save HTML for article {article.article_id}.", e)


def reparse_failed_articles_by_newspaperid(newspaperid) -> list[dict]:
    from service.automation_framework.soup_service import ArticleSoupParser

    try:
        failed_articles = get_failed_articles_by_newspaper_id(newspaperid)
        articles: [ArticleRequest] = []
        articles_response = []

        for fa in failed_articles:
            articles.append(ArticleRequest(
                newspaper_id=newspaperid,
                date=str(fa.get('failure_at', '')),
                url=fa.get('info', {}).get('url'),
                article_id=fa.get('article_id'),
                headline=fa.get('info', {}).get('headline', ''),
                preamble=fa.get('info', {}).get('preamble', ''),
                sector=fa.get('info', {}).get('sector', ''),
                publish=True
            ))

        article_config = find_article_configuration(newspaperid)

        soup_service = ArticleSoupParser(config=article_config.get('doc'), can_publish=False)
        articles_response.extend(soup_service.reparse_failed_articles(articles))

        return articles_response

    except Exception as e:
        log.log_error('Error occurred while parsing batch articles.', e)
        return []
    finally:
        log.log_application_end()


def fetch_failed_article_html(article_id: int) -> str | None:
    folder_path = ds.SPOKESPERSON_FAILED_ARTICLE_DIRECTORY
    file_name = f"{article_id}.html"
    abs_file_path = os.path.join(folder_path, file_name)

    try:

        if not os.path.exists(abs_file_path):
            log.log_error(f"HTML file not found for article_id={article_id}: {abs_file_path}")
            return None

        with open(abs_file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            return content

    except Exception as e:
        log.log_error(
            f"Exception occurred while reading HTML for article_id={article_id}, path={abs_file_path}",
            exception=e
        )
        return None


def get_random_proxy() -> Optional[str]:
    """
    Selects a random proxy from a comma-separated PROXIES config string.

    Returns:
        A cleaned proxy string or None if not found/available.
    """
    try:
        if not hasattr(ds, 'PROXIES') or not ds.PROXIES:
            log.log_warning("[Proxy Rotation] PROXIES config is missing or empty.")
            return None

        # Split, strip, and filter out empty values
        proxies = [p.strip() for p in ds.PROXIES.split(',') if p.strip()]
        if not proxies:
            log.log_warning("[Proxy Rotation] No valid proxies found after parsing.")
            return None

        proxy = random.choice(proxies)
        log.log_info(f"[Proxy Rotation] Selected proxy: {proxy}")
        return proxy

    except Exception as e:
        log.log_error("[Proxy Rotation] Failed to retrieve a random proxy.", exception=e)
        return None
