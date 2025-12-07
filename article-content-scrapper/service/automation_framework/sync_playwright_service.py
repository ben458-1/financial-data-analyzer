import os.path
from typing import List

from playwright.sync_api import sync_playwright, Page
import json

from model.article_request import ArticleRequest
from service.utils import get_matched_datetime_value, extract_date
from model.action import Action
# from playwright_stealth import stealth_sync
from logger import log
from service.rabbit_mq import rabbit_mq as mq

cur_dir = os.path.dirname(__file__)
session_storage_path = os.path.join(os.path.dirname(os.path.dirname(cur_dir)), 'session_storage')


def extract_info_from_webpage(page, url, config):
    page.goto(url)
    if is_article_protected(config, page):
        handle_site_auth(config, page)
    if page:
        try:
            header_value = header(config.get('header'), page)
            body_value = body(config.get('body'), page)
            author_value = author(config.get('author'), page)
            parsed_date, date = parse_date(config.get('date'), page)
            return {
                'header': header_value,
                'body': body_value,
                'author': author_value,
                'date': date,
                'std_date': parsed_date,
                'language': config.get('language', ''),
                'newspaper_id': config.get('newspaperID', 0)
            }
        except Exception as e:
            log.log_error('Error occurred while crawling into ', e)
            return None
    else:
        return None


def crawl_from_article(selectors, page: Page, name):
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
        except Exception as e:
            log.log_error("Element not found or not visible within the timeout ", exception=e)
            log.log_warning("Moving to next selectors in the list")
            continue
    log.log_critical(
        f"Error: Required '{name}' configuration is missing for article URL: '{page.url}'. Please review the configuration.")
    return ' '


def crawl_date_from_article(selectors, page, name):
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
            continue
    log.log_critical(
        f"Error: Required '{name}' configuration is missing for article URL: '{page.url}'. Please review the configuration.")
    return {'date': ' ', 'regex': []}


def extract_articles_batch():
    print('')


def fetch_articles_from_urls(article_metadata_list: list):
    articles = []
    print()


def process_captcha():
    print('processing captcha')


def header(selectors, page):
    return crawl_from_article(selectors, page, 'Header')


def body(selectors, page):
    return crawl_from_article(selectors, page, 'Body')


def author(selectors, page):
    return crawl_from_article(selectors, page, 'Author')


def parse_date(selectors, page):
    output = crawl_date_from_article(selectors, page, 'Article Date')
    try:
        # print(output)
        value = get_matched_datetime_value(output.get('regex'), output.get('date'))
        date = value if value else output.get('date')
        parsed_date = extract_date(date)
        return parsed_date, output.get('date')

    except Exception as e:
        log.log_error(f"Date-time parsing exception. Please check the format of the input: '{output.get('date')}'.", e)
        return '', output.get('date')


def extract(headless, url: str, config, can_publish: bool):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)  # Launch a single browser instance
        context = browser.new_context(
            # user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            # viewport={"width": 1366, "height": 768},
            # locale="en-US",
            # geolocation={"latitude": 37.7749, "longitude": -122.4194},
            # permissions=["geolocation"]
        )
        page = context.new_page()  # open a new tab
        # apply stealth settings to the page
        # stealth_sync(page)
        try:
            if config.get('login') == 1:
                auth_status = handle_site_auth(config, page).get('authenticate_status')
                if auth_status:
                    article_info = extract_info_from_webpage(page, url, config)

                    if can_publish:
                        mq.publish_message_into_article_analyzer(json.dumps(article_info))

                    return article_info
            else:
                article_info = extract_info_from_webpage(page, url, config)

                if can_publish:
                    mq.publish_message_into_article_analyzer(json.dumps(article_info))

                return article_info
        except Exception as e:
            log.log_error('Error occurred while extracting', exception=e)
        finally:
            log.log_application_end()
            browser.close()


def extract_batch(articles: List[ArticleRequest], config, can_publish: bool):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Launch a single browser instance
        context = browser.new_context()
        page = context.new_page()  # open a new tab

        # apply stealth settings to the page
        # stealth_sync(page)
        articles_response = []

        try:
            if config.get('login') == 1:
                auth_status = handle_site_auth(config, page).get('authenticate_status')
                if auth_status:
                    for article in articles:
                        log.log_info(f"Started crawling URL - '{article.url}'")
                        article_info = extract_info_from_webpage(page, article.url, config)
                        article_info['article_id'] = article.article_id
                        article_info['preamble'] = article.preamble
                        article_info['sector'] = article.sector

                        if can_publish:
                            mq.publish_message_into_article_analyzer(json.dumps(article_info))

                        articles_response.append(article_info)
                        log.log_separator()
            else:
                for article in articles:
                    log.log_info(f"Started crawling URL - '{article.url}'")
                    article_info = extract_info_from_webpage(page, article.url, config)
                    article_info['article_id'] = article.article_id
                    article_info['preamble'] = article.preamble
                    article_info['sector'] = article.sector

                    if can_publish:
                        mq.publish_message_into_article_analyzer(json.dumps(article_info))

                    articles_response.append(article_info)
                    log.log_separator()
            return articles_response
        except Exception as e:
            log.log_error('Error occurred while extracting', exception=e)
        finally:
            log.log_application_end()
            browser.close()


def wait_content_to_load(page: Page):
    page.wait_for_load_state("networkidle")


def handle_site_auth(config, page: Page):
    auth_config = config.get('authConfig', {})
    log.log_separator()
    if auth_config:
        log.log_info('Start site authentication process.')
        try:
            news_id = config.get('newspaperID')
            newspaper_session_storage_id = f"{news_id}_{str(config.get('name', '')).replace(' ', '').lower()}"
            page.goto(auth_config.get('loginUrl'))
            credential = fetch_auth_credentials(newspaper_id=news_id)
            session_storage_file = os.path.join(session_storage_path, newspaper_session_storage_id)

            steps = auth_config.get('steps', {})

            for k in steps:
                step = steps.get(k)
                step_action = step.get('action')

                if step_action == Action.TYPE.value:
                    enter_text(page, step.get('type'), step.get('name'), credential.get(k, ''))
                elif step_action == Action.CLICK.value:
                    click_element(page, step.get('type'), step.get('name'))
                else:
                    log.log_warning(f"configured '{k}' action in authentication config is not supported")
                    return {'authenticate_status': False}
            # Save storage state into the file.
            page.context.storage_state(path=f'{session_storage_file}.json')
            return {'authenticate_status': True}
        except Exception as auth_err:
            log.log_error(f'Error occurred while trying to sign in to the {config.get("name")} site', auth_err)
    else:
        log.log_warning('Missing Authenticate configuration.')
        log.log_separator()
    return {'authenticate_status': False}


def handle_site_cookies(config, page: Page):
    cookies_config = config.get('cookies', None)
    if cookies_config:
        try:
            log.log_info('Cookies not yet implement')
        except Exception as e:
            log.log_error('Error occurred while trying to handle cookies in site ', e)
    else:
        log.log_warning('Missing Cookies configuration')


def fetch_auth_credentials(newspaper_id: int):
    return {'email': 'vigneshwaran.euroland@gmail.com', 'password': 'FinancialTimes@1998'}


def enter_text(page: Page, locator_type, locator, text):
    """Finds an input field and types text into it."""
    page.type(selector=locator, text=text)


def click_element(page: Page, locator_type, locator):
    """Finds an element and clicks it."""
    page.locator(selector=locator).click(timeout=2000)


def is_article_protected(config, page: Page):
    if config.get('login') == 1:
        site_identifier_locator = config.get('authConfig', {}).get('siteIdentifier', {}).get('name', None)
        if site_identifier_locator:
            auth_is_required = page.locator(site_identifier_locator).count() > 0
            if auth_is_required:
                return True
            else:
                log.log_warning('Site is not restricted or does not match the site identifier configuration')
        else:
            log.log_warning('Site Identifier configuration is missing.')
            return False
