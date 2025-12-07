import json
import traceback
from datetime import datetime, timezone
from typing import List

import certifi
import requests
import pycurl
from bs4 import BeautifulSoup

from exceptions.custom_exception import InvalidArgumentsException
from logger import log
from model.article_request import ArticleRequest
from model.system_error_mail import SysErrorModel
from service.utils import mail_utils, date_utils, bot_utils
from service.rabbit_mq import rabbit_mq as mq
from core.config import data_source as ds
from service.db import upsert_into_failed_articles, insert_article_data_into_db
from service.utils.bot_utils import fetch_failed_article_html


class ArticleSoupParser:
    newspaper_id: int
    article_id: int
    article_url: str
    newspaper_name: str
    config: dict
    can_publish: bool
    missing_configuration: set
    alert: bool = False
    excludes: []
    excludes_element: set
    can_save_article: bool
    affected_articles: []
    article: ArticleRequest
    is_article_resolved: bool

    def __init__(self, config: dict, can_publish: bool = False):
        self.config = config
        self.can_publish = can_publish
        self.newspaper_name = config.get('name', '')
        self.newspaper_id = config.get('newspaperID')
        self.can_save_article = False
        self.missing_configuration = set()
        self.affected_articles = []
        self.alert: bool = False

    @staticmethod
    def create_curl_instance():
        try:
            c = pycurl.Curl()
            return c
        except Exception as err:
            log.log_error('Error occurred while instantiating CURL.', err)
            return None

    @staticmethod
    def close_curl(pycurl_obj):
        if pycurl_obj:
            pycurl_obj.close()

    def make_request(self) -> str | None:
        try:
            log.log_info(f"[Request] Fetching URL: {self.article_url}")

            # === Optional Proxy Setup ===
            proxy = None
            if getattr(self, "config", {}).get("useIpProxy") == 1 and getattr(ds, "PROXY_ENABLED", False):
                proxy = bot_utils.get_random_proxy()
                if proxy:
                    log.log_info(f"[Request] Using proxy: {proxy}")
                    proxies = {
                        "http": proxy,
                        "https": proxy
                    }
                else:
                    log.log_warning("[Request] Proxy enabled but no proxy available.")
                    proxies = None
            else:
                proxies = None

            response = requests.get(self.article_url, verify=certifi.where(), proxies=proxies)
            if response.status_code == 200:
                encoding = response.encoding or 'utf-8'
                return response.content.decode(encoding)
            else:
                log.log_warning(
                    f"Non-success HTTP response for URL {self.article_url}: "
                    f"{response.status_code} {response.reason}"
                )
                return None
        except requests.RequestException as e:
            log.log_error(f"HTTP request error for URL {self.article_url}", e)
            return None
        except Exception as e:
            log.log_error(f"Unexpected error during request to {self.article_url}", e)
            return None

    def initiate_html_parser(self, doc: str) -> dict | None:
        try:
            soup = BeautifulSoup(doc, 'html.parser')

            self.can_save_article = False

            header = self._parse_element('header', soup)
            body = self._parse_element('body', soup)
            author = self._parse_element('author', soup)
            std_date, raw_date = self._parse_date('date', soup)
            keywords = self._parse_keyword_elements('keywords', soup)

            if self.can_save_article:
                # Save the page source for debugging
                bot_utils.save_as_html(page_source=doc, article=self.article)
                self.can_save_article = False
                self.affected_articles.append({"article_id": self.article_id, "article_url": self.article_url})
                self.alert = True
                self.is_article_resolved = False

            return {
                'header': header,
                'body': body,
                'author': author,
                'date': raw_date,
                'std_date': std_date,
                'language': self.config.get('language', ''),
                'newspaper_id': self.config.get('newspaperID', 0),
                'keywords': keywords
            }
        except Exception as e:
            log.log_error('Error occurred while crawling into ', e)
            return None

    def reparse_html(self, doc: str) -> dict | None:
        try:
            soup = BeautifulSoup(doc, 'html.parser')

            self.can_save_article = False

            header = self._parse_element('header', soup)
            body = self._parse_element('body', soup)
            author = self._parse_element('author', soup)
            std_date, raw_date = self._parse_date('date', soup)
            keywords = self._parse_keyword_elements('keywords', soup)

            if self.can_save_article:
                self.can_save_article = False
                self.affected_articles.append({"article_id": self.article_id, "article_url": self.article_url})
                self.alert = True

            return {
                'header': header,
                'body': body,
                'author': author,
                'date': raw_date,
                'std_date': std_date,
                'language': self.config.get('language', ''),
                'newspaper_id': self.config.get('newspaperID', 0),
                'keywords': keywords
            }
        except Exception as e:
            log.log_error('Error occurred while crawling into ', e)
            return None

    def _parse_element(self, section_name: str, soup: BeautifulSoup) -> str:
        selectors = self.config.get(section_name, [])

        for sc in selectors:
            elements = soup.select(sc.get('name', ''))

            if not elements:
                log.log_warning(
                    f"[{section_name}] No elements found for selector '{sc.get('name', 'invalid')}' "
                    f"on page: {self.article_url}"
                )
                continue

            values = [ele.get_text(strip=True) for ele in elements]
            return ' '.join(values).replace('\n', ' ').replace('\t', ' ').strip()

        if section_name == 'author':
            return ''

        # Missing or Mismatching Configuration
        self.missing_configuration.add(section_name)
        self.can_save_article = True

        return ''

    def _parse_keyword_elements(self, section_name: str, soup: BeautifulSoup) -> List[str]:
        selectors = self.config.get(section_name, [])

        for sc in selectors:
            elements = soup.select(sc.get('name', ''))

            if not elements:
                log.log_warning(
                    f"[{section_name}] No elements found for selector '{sc.get('name', 'invalid')}' "
                    f"on page: {self.article_url}"
                )
                continue

            values = [ele.get_text(strip=True) for ele in elements]
            return values

        return []

    def _parse_date(self, section_name: str, soup: BeautifulSoup) -> tuple[str, str]:

        selectors = self.config.get(section_name, [])
        date_regex = self.config.get('dateRegex', [])

        for sc in selectors:
            elements = soup.select(sc.get('name', ''))
            attr = sc.get("attribute", "")

            if not elements:
                log.log_warning(
                    f"[{section_name}] No elements found for selector '{sc.get('name', 'invalid')}' "
                    f"on page: {self.article_url}"
                )
                continue

            values = (
                [ele.get(attr, '').strip() for ele in elements]
                if attr else
                [ele.get_text(strip=True).replace('\n', '') for ele in elements]
            )
            raw_date = ''.join(values)

            try:
                matched = date_utils.get_matched_datetime_value(date_regex, raw_date)
                parsed_date = date_utils.extract_date(matched or raw_date)
                return parsed_date, raw_date
            except Exception as e:
                log.log_error(f'date_time parsing error for {self.article_url}:', e)
                return '', raw_date

        # Missing or Mismatching Configuration
        self.missing_configuration.add(section_name)
        self.can_save_article = True

        return '', ''

    def extract(self, article: ArticleRequest) -> dict | None:
        try:
            log.log_info(f"Started crawling URL - '{article.url}'")
            self.alert = False
            self.article_id = article.article_id
            self.article_url = article.url
            self.article = article

            if self.config.get('login') == 1:
                try:
                    msg = "Login is required for this newspaper site. Please switch to 'login' execution mode or " \
                          "update the login field configuration."
                    log.log_error(msg)
                    raise InvalidArgumentsException(message=msg)
                except InvalidArgumentsException as err:
                    stacktrace = traceback.format_exc()
                    err = SysErrorModel(type="Selenium Execution Mode",
                                        message=str(err),
                                        time=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
                                        environment=ds.STAGE,
                                        stack_trace=stacktrace,
                                        component='ArticleSoupParser'
                                        )
                    mail_utils.system_error_alert(err.dict())

                    raise err

            html = self.make_request()

            if not html:
                return None
            article_info = self.initiate_html_parser(html)

            article_info['article_id'] = article.article_id
            article_info['preamble'] = article.preamble
            article_info['sector'] = article.sector
            article_info['link'] = article.url

            # Inserting into database.
            insert_article_data_into_db(article_info)

            if self.can_publish:
                mq.publish_message_into_article_analyzer(json.dumps(article_info))

            if self.alert:
                context = {
                    "newspaper_id": self.newspaper_id,
                    "newspaper_name": self.newspaper_name,
                    "missing_config": self.missing_configuration,
                    "articles": self.affected_articles,
                    "year": date_utils.current_year()
                }
                mail_utils.config_missing_alert(context)

            return article_info
        except Exception as e:
            log.log_error('Error occurred while parsing article.', e)
        finally:
            log.log_application_end()

    def extract_batch(self, articles: list[ArticleRequest]) -> list[dict]:
        results = []
        try:

            self.alert = False

            if self.config.get('login') == 1:
                try:
                    msg = "Login is required for this newspaper site. Please switch to 'login' execution mode or " \
                          "update the login field configuration."
                    log.log_error(msg)
                    raise InvalidArgumentsException(message=msg)
                except InvalidArgumentsException as err:
                    stacktrace = traceback.format_exc()
                    err = SysErrorModel(type="Selenium Execution Mode",
                                        message=str(err),
                                        time=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
                                        environment=ds.STAGE,
                                        stack_trace=stacktrace,
                                        component='ArticleSoupParser'
                                        )
                    mail_utils.system_error_alert(err.dict())

                    raise err

            for article in articles:
                self.article_id = article.article_id
                self.article_url = article.url
                self.article = article
                log.log_info(f"Started crawling URL - '{article.url}'")
                html = self.make_request()

                if not html:
                    continue

                data = self.initiate_html_parser(html)
                data.update({
                    'article_id': article.article_id,
                    'preamble': article.preamble,
                    'sector': article.sector,
                    'link': article.url
                })

                # Inserting into database.
                insert_article_data_into_db(data)

                if self.can_publish:
                    mq.publish_message_into_article_analyzer(json.dumps(data))

                results.append(data)
                log.log_separator()

            if self.alert:
                context = {
                    "newspaper_id": self.newspaper_id,
                    "newspaper_name": self.newspaper_name,
                    "missing_config": self.missing_configuration,
                    "articles": self.affected_articles,
                    "year": date_utils.current_year()
                }
                mail_utils.config_missing_alert(context)

            return results

        except Exception as e:
            log.log_error('Error occurred while parsing batch articles.', e)
            return []
        finally:
            log.log_application_end()

    def reparse_failed_articles(self, articles: List[ArticleRequest]) -> list[dict]:
        results = []
        try:

            self.alert = False

            for article in articles:
                self.is_article_resolved = True
                self.article_id = article.article_id
                self.article_url = article.url
                self.article = article
                log.log_info(f"Started crawling URL - '{article.url}'")
                html = fetch_failed_article_html(article.article_id)

                if not html:
                    continue

                data = self.initiate_html_parser(html)
                data.update({
                    'article_id': article.article_id,
                    'preamble': article.preamble,
                    'sector': article.sector,
                    'link': article.url
                })

                if self.can_publish:
                    mq.publish_message_into_article_analyzer(json.dumps(data))

                results.append(data)
                log.log_separator()

                if self.is_article_resolved:
                    upsert_into_failed_articles({'article_id': article.article_id,
                                                 'newspaper_id': self.newspaper_id,
                                                 'is_resolved': True
                                                 })
                else:
                    upsert_into_failed_articles({'article_id': article.article_id,
                                                 'newspaper_id': self.newspaper_id,
                                                 'is_resolved': False
                                                 })

            if self.alert:
                context = {
                    "newspaper_id": self.newspaper_id,
                    "newspaper_name": self.newspaper_name,
                    "missing_config": self.missing_configuration,
                    "articles": self.affected_articles,
                    "year": date_utils.current_year()
                }
                mail_utils.config_missing_alert(context)

            return results
        except Exception as e:
            log.log_error('Error occurred while parsing batch articles.', e)
            return []
        finally:
            log.log_application_end()
