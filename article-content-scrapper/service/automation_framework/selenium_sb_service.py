import json
import time
import os
from typing import List

from seleniumbase import SB
from selenium.webdriver.common.by import By

from model.article_request import ArticleRequest
from service.utils import extract_date, get_matched_datetime_value, save_as_html
from model.action import Action
from logger import log
from service.rabbit_mq import rabbit_mq as mq

cur_dir = os.path.dirname(__file__)
session_storage_path = os.path.join(os.path.dirname(os.path.dirname(cur_dir)), 'session_storage')


def driver_config(driver):
    print('yet to config')


# def initialize_webdriver(uc_mode=True):
#     driver = None
#     try:
#         driver = Driver(uc=uc_mode, browser='chrome')
#         return driver
#     except Exception as wd_err:
#         print(f'Error occured while initializing the  {wd_err}')
#         if driver:
#             driver.quit()
#         return None


def extract_info_from_webpage(config, driver=None):
    if driver:
        try:
            header_value = header(config.get('header'), driver)
            body_value = body(config.get('body'), driver)
            author_value = author(config.get('author'), driver)
            parsed_date, date = parse_date(config.get('date'), driver)

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


def process_captcha():
    print('processing captcha')


def authenticate_user():
    print('Authenticating user')


def crawl_from_article(selectors, driver, name):
    """
       Crawls through the provided selectors to extract text from elements
       identified by CSS selectors or XPath.

       Args:
           selectors (list): A list of dictionaries containing selector information.
           driver (WebDriver): The Selenium WebDriver instance.

       Returns:
           str: A concatenated string of text from the found elements.
           :param selectors:
           :param driver:
           :param name:
           :return:
    """
    values = []

    for s in selectors:
        selector_type = s.get('type', '')
        selector_query = s.get('name', '')
        if selector_type == 'css':
            elements = driver.find_elements(selector_query, By.CSS_SELECTOR)
            if elements:
                for ele in elements:
                    values.append(ele.text)
                return ' '.join(values)
            else:
                log.log_warning(f"Element '{selector_query}' is not present on the page: {driver.get_current_url()}")
                continue
        elif selector_type == 'xpath':
            elements = driver.find_elements(selector_query, By.XPATH)
            if elements:
                for ele in elements:
                    values.append(ele.text)
                return ' '.join(values)
            else:
                log.log_warning(f"Element '{selector_query}' is not present on the page: {driver.get_current_url()}")
                continue
        else:
            log.log_warning(f"Unsupported selector type: '{selector_type}'")
    log.log_critical(f"Error: Required '{name}' configuration is missing for article URL: '{driver.get_current_url()}'."
                     f" Please review the configuration.")

    page_source = driver.get_page_source()
    save_as_html(page_source=page_source, article_id='15')

    return ''


def crawl_date_from_article(selectors, driver, name):
    values = []
    for s in selectors:
        selector_type = s.get('type', '')
        selector_query = s.get('name', '')
        if selector_type == 'css':
            elements = driver.find_elements(selector_query, By.CSS_SELECTOR)
            if elements:
                for ele in elements:
                    values.append(ele.text)
                return {'date': ' '.join(values), 'regex': s.get('regex', [])}
            else:
                log.log_warning(f"Element '{selector_query}' is not present on the page: {driver.get_current_url()}")
                continue
        elif selector_type == 'xpath':
            elements = driver.find_elements(selector_query, By.CSS_SELECTOR)
            if elements:
                for ele in elements:
                    values.append(ele.text)
                return {'date': ' '.join(values), 'regex': s.get('regex', [])}
            else:
                log.log_warning(f"Element '{selector_query}' is not present on the page: {driver.get_current_url()}")
                continue
        else:
            log.log_warning(f"Unsupported selector type: '{selector_type}'")
    log.log_critical(
        f"Error: Required '{name}' configuration is missing for article URL: '{driver.get_current_url()}'. Please review the configuration.")

    page_source = driver.get_page_source()
    save_as_html(page_source=page_source, article_id='15')

    return {'date': ' ', 'regex': []}


def header(selectors, driver):
    return crawl_from_article(selectors, driver, 'Article Header')


def body(selectors, driver):
    return crawl_from_article(selectors, driver, 'Article Body')


def author(selectors, driver):
    return crawl_from_article(selectors, driver, 'Author')


def parse_date(selectors, driver):
    output = crawl_date_from_article(selectors, driver, 'Date')
    try:
        # print(output)
        value = get_matched_datetime_value(output.get('regex'), output.get('date'))
        date = value if value else output.get('date')
        parsed_date = extract_date(date)
        return parsed_date, output.get('date')

    except Exception as e:
        log.log_error(f"Date-time parsing exception. Please check the format of the input: '{output.get('date')}'.", e)
        return '', output.get('date')


def extract(url, config, can_publish: bool):
    log.log_separator()
    try:
        log.log_info('Initializing seleniumbase for web crawling.')
        with SB(uc=True) as sb:
            sb.uc_open_with_reconnect(url, 2)
            time.sleep(10)
            if config.get('login') == 1:
                auth_status = handle_site_auth(config, sb).get('authenticate_status')
                if auth_status:
                    article_info = extract_info_from_webpage(config, sb)

                    if can_publish:
                        mq.publish_message_into_article_analyzer(json.dumps(article_info))

                    return article_info
            else:
                article_info = extract_info_from_webpage(config, sb)

                if can_publish:
                    mq.publish_message_into_article_analyzer(json.dumps(article_info))

                return article_info
    except Exception as err:
        log.log_error('Error occurred while extracting', exception=err)
    finally:
        log.log_application_end()


def extract_batch(articles: List[ArticleRequest], config, can_publish: bool):
    log.log_separator()
    try:
        log.log_info('Initializing seleniumbase for web crawling.')
        article_extracted_output = []
        with SB(uc=True) as sb:
            if config.get('login') == 1:
                auth_status = handle_site_auth(config, sb).get('authenticate_status')
                if auth_status:
                    for article in articles:
                        log.log_info(f"Started crawling URL - '{article.url}'")
                        sb.uc_open_with_reconnect(article.url, 2)
                        time.sleep(10)
                        article_info = extract_info_from_webpage(config, sb)
                        article_info['article_id'] = article.article_id
                        article_info['preamble'] = article.preamble
                        article_info['sector'] = article.sector

                        if can_publish:
                            mq.publish_message_into_article_analyzer(json.dumps(article_info))

                        article_extracted_output.append(article_info)
                        log.log_separator()
                    return article_extracted_output
            else:
                for article in articles:
                    log.log_info(f"Started crawling URL - '{article.url}'")
                    sb.uc_open_with_reconnect(article.url, 2)
                    time.sleep(10)
                    article_info = extract_info_from_webpage(config, sb)
                    article_info['article_id'] = article.article_id
                    article_info['preamble'] = article.preamble
                    article_info['sector'] = article.sector

                    if can_publish:
                        mq.publish_message_into_article_analyzer(json.dumps(article_info))

                    article_extracted_output.append(article_info)
                    log.log_separator()
                return article_extracted_output
    except Exception as err:
        log.log_error('Error occurred while extracting', exception=err)
    finally:
        log.log_application_end()


def handle_site_auth(config, driver: SB):
    auth_config = config.get('authConfig', {})
    log.log_separator()
    if auth_config:
        log.log_info('Start site authentication process.')
        try:
            news_id = config.get('newspaperID')
            # newspaper_session_storage_id = f"{news_id}_{str(config.get('name', '')).replace(' ', '').lower()}"
            driver.uc_open_with_reconnect(auth_config.get('loginUrl'), 2)
            credential = fetch_auth_credentials(newspaper_id=news_id)
            # session_storage_file = os.path.join(session_storage_path, newspaper_session_storage_id)

            steps = auth_config.get('steps', {})

            for k in steps:
                step = steps.get(k)
                step_action = step.get('action')

                if step_action == Action.TYPE.value:
                    enter_text(driver, step.get('type'), step.get('name'), credential.get(k, ''))
                elif step_action == Action.CLICK.value:
                    click_element(driver, step.get('type'), step.get('name'))
                else:
                    log.log_warning(f"configured '{k}' action in authentication config is not supported")
                    return {'authenticate_status': False}
            # Save storage state into the file.
            # driver.context.storage_state(path=f'{session_storage_file}.json')
            return {'authenticate_status': True}
        except Exception as auth_err:
            log.log_error(f'Error occurred while trying to sign in to the {config.get("name")} site', auth_err)
    else:
        log.log_warning('Missing Authenticate configuration.')
    log.log_separator()
    return {'authenticate_status': False}


def fetch_auth_credentials(newspaper_id: int):
    return {'email': 'vigneshwaran.euroland@gmail.com', 'password': 'FinancialTimes@1998'}


def enter_text(driver, locator_type, locator, text):
    """Finds an input field and types text into it."""
    driver.type(locator, text=text)


def click_element(driver, locator_type, locator):
    """Finds an element and clicks it."""
    driver.click(locator, timeout=2000)


def is_article_protected(config, driver):
    if config.get('login') == 1:
        site_identifier_locator = config.get('authConfig', {}).get('siteIdentifier', {}).get('name', None)
        if site_identifier_locator:
            auth_is_required = driver.find_elements(site_identifier_locator).count() > 0
            if auth_is_required:
                log.log_info('Site required Authentication.')
                return True
            else:
                log.log_warning('Site is not restricted or does not match the site identifier configuration')
        else:
            log.log_warning('Site Identifier configuration is missing.')
            return False
