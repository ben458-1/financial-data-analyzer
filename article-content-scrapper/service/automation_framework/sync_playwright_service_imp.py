import os
import json
from typing import List

from interface.crawling import Crawling
from model.action import Action
from model.article_request import ArticleRequest
from service.utils import mail_utils, date_utils, bot_utils
from logger import log
from core import config as conf
from core.config import Settings
from service.rabbit_mq import rabbit_mq as mq

from playwright.sync_api import sync_playwright, Page


class PlaywrightServiceImp(Crawling):
    cur_dir: str
    session_storage_path: str
    newspaper_id: int
    article_id: int
    newspaper_name: str
    page_wait: int
    config: dict
    can_publish: bool
    lang: str
    ds: Settings

    def __init__(self, config: dict, can_publish: bool):
        self.config = config
        self.can_publish = can_publish
        self.newspaper_name = config.get('name', '')
        self.newspaper_id = config.get('newspaperID')
        self.page_wait = config.get('betweenWait')
        self.lang = config.get('language')
        self.cur_dir = os.path.dirname(__file__)
        self.session_storage_path = os.path.join(os.path.dirname(os.path.dirname(self.cur_dir)), 'session_storage')
        self.ds = conf.data_source

    def automation_tool_config(self, driver) -> None:
        log.log_info("Not yet implement tool configuration")

    def extract_info_from_webpage(self, driver) -> dict | None:

        page = driver

        if page:
            try:
                header_value = self.header(self.config.get('header'), page)
                body_value = self.body(self.config.get('body'), page)
                author_value = self.author(self.config.get('author'), page)
                parsed_date, date = self.parse_date(self.config.get('date'), page)
                return {
                    'header': header_value,
                    'body': body_value,
                    'author': author_value,
                    'date': date,
                    'std_date': parsed_date,
                    'language': self.lang,
                    'newspaper_id': self.newspaper_id
                }
            except Exception as e:
                log.log_error('Error occurred while crawling into ', e)
                return None

        log.log_warning("Web driver is not initialized")
        return None

    def process_captcha(self):
        log.log_info("Not yet implement captcha handler")

    def authenticate_user(self):
        log.log_info("Not yet implement user authentication")

    def crawl_from_article(self, selectors: dict, section_name: str, driver) -> str:

        page: Page = driver
        texts = []

        for s in selectors:
            selector_query = s.get('name', '')
            try:
                is_element_present = page.wait_for_selector(selector=selector_query, timeout=10000)

                if is_element_present:
                    elements = page.query_selector_all(selector_query)
                    if elements:
                        for ele in elements:
                            text = ele.inner_text()
                            texts.append(text)
                        return ' '.join(texts)
                else:
                    log.log_warning(f"Element '{selector_query}' is not present on the page: {page.url}")
                    continue

            except Exception:
                log.log_warning("Element not found or not visible within the timeout. "
                                "Moving to next selectors in the list")
                continue

        log.log_critical(
            f"Error: Required '{section_name}' configuration is missing for article URL: '{page.url}'. "
            f"Please review the configuration.")

        return ' '

    def crawl_date_from_article(self, selectors: dict, section_name: str, driver) -> dict:

        page: Page = driver
        texts = []

        for s in selectors:
            selector_query = s.get('name', '')
            elements = page.query_selector_all(selector_query)

            if elements:
                for ele in elements:
                    text = ele.inner_text()
                    texts.append(text)
                return {'date': ' '.join(texts), 'regex': s.get('regex', [])}
            else:
                log.log_warning(f"Element '{selector_query}' is not present on the page: {page.url}")

        log.log_critical(
            f"Error: Required '{section_name}' configuration is missing for article URL: '{page.url}'. "
            f"Please review the configuration.")

        return {'date': ' ', 'regex': []}

    def header(self, selectors: dict, driver) -> str:
        return self.crawl_from_article(selectors, 'Article Header', driver)

    def body(self, selectors: dict, driver) -> str:
        return self.crawl_from_article(selectors, 'Article Body', driver)

    def author(self, selectors: dict, driver) -> str:
        return self.crawl_from_article(selectors, 'Author', driver)

    def parse_date(self, selectors: dict, driver) -> tuple[str, str]:

        output = self.crawl_date_from_article(selectors, 'Article Date', driver)

        try:

            value = date_utils.get_matched_datetime_value(output.get('regex'), output.get('date'))
            date = value if value else output.get('date')
            parsed_date = date_utils.extract_date(date)

            return parsed_date, output.get('date')

        except Exception as e:
            log.log_error(f"Date-time parsing exception. Please check the format of the input: '{output.get('date')}'.",
                          e)
            return '', output.get('date')

    def extract(self, url: str) -> dict | None:

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.ds.HEADLESS)  # Launch a single browser instance
            context = browser.new_context()
            page = context.new_page()  # open a new tab

            try:
                if self.config.get('login') == 1:
                    auth_status = self.handle_site_auth(page).get('authenticate_status')
                    if not auth_status:
                        return None

                page.goto(url)

                if self.is_article_protected(page):
                    self.handle_site_auth(page)

                article_info = self.extract_info_from_webpage(page)

                if self.can_publish:
                    mq.publish_message_into_article_analyzer(json.dumps(article_info))

                return article_info
            except Exception as e:
                log.log_error('Error occurred while extracting', exception=e)
            finally:
                log.log_application_end()
                browser.close()

    def extract_all(self, articles: List[ArticleRequest]) -> List[dict]:

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=self.ds.HEADLESS)  # Launch a single browser instance
            context = browser.new_context()
            page = context.new_page()  # open a new tab

            articles_response = []

            try:
                if self.config.get('login') == 1:
                    auth_status = self.handle_site_auth(page).get('authenticate_status')

                    if not auth_status:
                        return []

                    for article in articles:
                        log.log_info(f"Started crawling URL - '{article.url}'")

                        page.goto(article.url)

                        if self.is_article_protected(page):
                            self.handle_site_auth(page)

                        article_info = self.extract_info_from_webpage(page)
                        article_info['article_id'] = article.article_id
                        article_info['preamble'] = article.preamble
                        article_info['sector'] = article.sector

                        if self.can_publish:
                            mq.publish_message_into_article_analyzer(json.dumps(article_info))

                        articles_response.append(article_info)
                        log.log_separator()

                return articles_response
            except Exception as e:
                log.log_error('Error occurred while extracting', exception=e)
            finally:
                log.log_application_end()
                browser.close()

    def handle_site_auth(self, driver) -> dict:

        page: Page = driver
        auth_config = self.config.get('authConfig', {})
        log.log_separator()

        if auth_config:
            log.log_info('Start site authentication process.')

            try:
                news_id = self.newspaper_id
                newspaper_session_storage_id = f"{news_id}_{self.newspaper_name}"

                page.goto(auth_config.get('loginUrl'))

                credential = self.fetch_auth_credentials(newspaper_id=news_id)
                session_storage_file = os.path.join(self.session_storage_path, newspaper_session_storage_id)

                steps = auth_config.get('steps', {})

                for k in steps:
                    step = steps.get(k)
                    step_action = step.get('action')

                    if step_action == Action.TYPE.value:
                        self.enter_text(step.get('type'), step.get('name'), credential.get(k, ''), page)
                    elif step_action == Action.CLICK.value:
                        self.click_element(step.get('type'), step.get('name'), page)
                    else:
                        log.log_warning(f"configured '{k}' action in authentication config is not supported")
                        return {'authenticate_status': False}

                # Save storage state into the file.
                page.context.storage_state(path=f'{session_storage_file}.json')
                return {'authenticate_status': True}

            except Exception as auth_err:
                log.log_error(f'Error occurred while trying to sign in to the {self.newspaper_name} site', auth_err)
        else:
            log.log_warning('Missing Authenticate configuration.')
            log.log_separator()

        return {'authenticate_status': False}

    def fetch_auth_credentials(self, newspaper_id: int) -> dict:
        return {'email': 'vigneshwaran.euroland@gmail.com', 'password': 'FinancialTimes@1998'}

    def enter_text(self, locator_type: str, locator: str, text: str, driver) -> None:
        driver.type(selector=locator, text=text)

    def click_element(self, locator_type: str, locator: str, driver) -> None:
        driver.locator(selector=locator).click(timeout=2000)

    def wait(self, locator_type: str, locator: str, driver) -> None:
        pass

    def page_action(self, duration: int, driver) -> None:
        pass

    def is_article_protected(self, driver):

        if self.config.get('login') == 1:
            site_identifier_locator = self.config.get('authConfig', {}).get('siteIdentifier', {}).get('name', None)

            if site_identifier_locator:
                auth_is_required = driver.locator(site_identifier_locator).count() > 0

                if auth_is_required:
                    return True
                else:
                    log.log_warning('Site is not restricted or does not match the site identifier configuration')
            else:
                log.log_warning('Site Identifier configuration is missing.')
                return False

        return False

    def stealth_mode(self, driver) -> None:
        pass
