import os
from collections import defaultdict
from typing import List

from core import config
from model.article_request import ArticleRequest
from service.automation_framework.soup_service import ArticleSoupParser
from service.db import find_article_configuration
from service.automation_framework import selenium_service
from service.automation_framework.seleniumbase_service_imp import SeleniumBaseImp
from service.automation_framework.sync_playwright_service_imp import PlaywrightServiceImp
from model.automation_framework import AutomationFramework
from logger import log


def extract_article(article: ArticleRequest):

    article_config = find_article_configuration(article.newspaper_id)
    execution_mode = article_config.get('doc').get('executionMode', 'selenium')

    if execution_mode == 'selenium':

        ds = config.data_source
        framework = ds.SELENIUM_FRAMEWORK

        if framework == AutomationFramework.SELENIUMBASE.value:

            log.log_info('Use Seleniumbase to parse the articles')
            sb = SeleniumBaseImp(article_config.get('doc'), can_publish=article.publish)
            article_dict = sb.extract(article)

            return article_dict

        elif framework == AutomationFramework.SELENIUM.value:

            log.log_info('Use Selenium to parse the articles')
            return selenium_service.extract(article.url, article_config.get('doc'), can_publish=article.publish)

        elif framework == AutomationFramework.PLAYWRIGHT.value:

            log.log_info('Use playwright to parse the articles')
            pw = PlaywrightServiceImp(article_config.get('doc'), can_publish=article.publish)
            article_dict = pw.extract(article.url)
            return article_dict

        else:

            log.log_error("Unsupported automation framework configuration")
            return None

    elif execution_mode == 'no-selenium':
        soup_service = ArticleSoupParser(config=article_config.get('doc'), can_publish=article.publish)
        return soup_service.extract(article)

    else:

        return None


def extract_article_batch(articles: List[ArticleRequest], publish: bool):

    grouped_articles_by_newspaper_id: dict[int, list[ArticleRequest]] = defaultdict(list)

    for article in articles:
        grouped_articles_by_newspaper_id[article.newspaper_id].append(article)

    articles_response = []

    for newspaper_id in grouped_articles_by_newspaper_id:

        article_config = find_article_configuration(newspaper_id)
        execution_mode = article_config.get('doc').get('executionMode', 'selenium')
        article_metadata_list = grouped_articles_by_newspaper_id.get(newspaper_id)

        if execution_mode == 'selenium':
            ds = config.data_source
            framework = ds.SELENIUM_FRAMEWORK

            if framework == AutomationFramework.SELENIUMBASE.value:

                log.log_info('Use Seleniumbase to parse the articles')
                sb = SeleniumBaseImp(article_config.get('doc'), can_publish=publish)
                articles_response.extend(sb.extract_all(article_metadata_list))

            elif framework == AutomationFramework.SELENIUM.value:

                log.log_info('Use Selenium to parse the articles')
                articles_response.extend(selenium_service.extract_batch(article_metadata_list, article_config.get('doc'),
                                                               can_publish=publish))

            elif framework == AutomationFramework.PLAYWRIGHT.value:

                log.log_info('Use playwright to parse the articles')
                pw = PlaywrightServiceImp(article_config.get('doc'), can_publish=publish)
                articles_response.extend(pw.extract_all(article_metadata_list))

            else:

                log.log_error("Unsupported automation framework configuration")

        elif execution_mode == 'no-selenium':

            log.log_info('Use beautiful soup to parse the articles')
            soup_service = ArticleSoupParser(config=article_config.get('doc'), can_publish=publish)
            articles_response.extend(soup_service.extract_batch(article_metadata_list))

        else:

            log.log_error('Unsupported execution mode')

    return articles_response
