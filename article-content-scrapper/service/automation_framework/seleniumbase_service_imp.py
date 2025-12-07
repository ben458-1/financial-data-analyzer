import os
import json
import time
import random
from typing import List
from datetime import datetime

from seleniumbase import SB
from selenium.webdriver.common.by import By

from exceptions.custom_exception import AuthenticationFailedException
from logger import log
from model.action import Action
from interface.crawling import Crawling
from service.db import insert_article_data_into_db
from service.rabbit_mq import rabbit_mq as mq
from model.article_request import ArticleRequest
from service.utils import mail_utils, date_utils, bot_utils
from selenium.webdriver.common.action_chains import ActionChains
from service import db
from core.config import data_source as ds


class SeleniumBaseImp(Crawling):
    cur_dir: str
    session_storage_path: str
    newspaper_id: int
    article_id: int
    article_url: str
    newspaper_name: str
    page_wait: int
    config: dict
    can_publish: bool
    lang: str
    cookies: str
    login: int
    missing_configuration: set
    alert: bool = False
    excludes: []
    excludes_element: set
    can_save_article: bool
    affected_articles: []
    article: ArticleRequest

    def __init__(self, config: dict, can_publish: bool):
        self.config = config
        self.can_publish = can_publish
        self.newspaper_name = config.get('name', '')
        self.newspaper_id = config.get('newspaperID')
        self.page_wait = config.get('betweenWait')
        self.lang = config.get('language')
        self.cur_dir = os.path.dirname(__file__)
        self.session_storage_path = os.path.join(os.path.dirname(os.path.dirname(self.cur_dir)), 'session_storage')
        self.login = config.get('login', 0)
        self.excludes = config.get('excludes', [])
        self.exclude_elements_set = set()
        self.can_save_article = False
        self.missing_configuration = set()
        self.affected_articles = []

    def automation_tool_config(self, driver) -> None:
        raise NotImplementedError('yet to config')

    def extract_info_from_webpage(self, driver) -> dict | None:
        if driver:
            try:
                self.can_save_article = False
                self.exclude_elements(driver)
                header_value = self.header(self.config.get('header'), driver)
                body_value = self.body(self.config.get('body'), driver)
                author_value = self.author(self.config.get('author'), driver)
                parsed_date, date = self.parse_date(self.config.get('date'), driver)
                keywords = self.keywords(self.config.get('keywords'), driver)

                if self.can_save_article:
                    # Save the page source for debugging
                    bot_utils.save_as_html(page_source=driver.get_page_source(), article=self.article)
                    self.can_save_article = False
                    self.affected_articles.append({"article_id": self.article_id, "article_url": self.article_url})
                    self.alert = True

                return {
                    'header': header_value,
                    'body': body_value,
                    'author': author_value,
                    'date': date,
                    'std_date': parsed_date,
                    'language': self.lang,
                    'newspaper_id': self.newspaper_id,
                    'keywords': keywords
                }
            except Exception as e:
                log.log_error('Error occurred while crawling into ', e)
                return None
        else:
            return None

    def process_captcha(self):
        raise NotImplementedError('Captcha is not yet Implemented')

    def authenticate_user(self):
        raise NotImplementedError('Authentication is not yet Implemented')

    def crawl_keywords_from_article(self, selectors: list[dict], section_name: str, driver) -> List[str]:
        for s in selectors:
            selector_type = s.get('type')
            selector_query = s.get('name')

            if not selector_type or not selector_query:
                continue  # Skip invalid selector entries

            by_type = {
                'css': By.CSS_SELECTOR,
                'xpath': By.XPATH
            }.get(selector_type)

            if not by_type:
                log.log_warning(f"[{section_name}] Unsupported selector type: '{selector_type}'")
                continue

            elements = driver.find_elements(selector_query, by_type)

            if not elements:
                log.log_warning(
                    f"[{section_name}] No elements found for selector '{selector_query}' "
                    f"on page: {driver.get_current_url()}"
                )
                continue

            keywords = [ele.text.strip() for ele in elements if ele.text.strip()]
            if keywords:
                return keywords

        return []

    def crawl_from_article(self, selectors: list[dict], section_name: str, driver) -> str:
        for s in selectors:
            selector_type = s.get('type')
            selector_query = s.get('name')

            if not selector_type or not selector_query:
                continue  # Skip invalid selector entries

            by_type = {
                'css': By.CSS_SELECTOR,
                'xpath': By.XPATH
            }.get(selector_type)

            if not by_type:
                log.log_warning(f"[{section_name}] Unsupported selector type: '{selector_type}'")
                continue

            elements = driver.find_elements(selector_query, by_type)

            if not elements:
                log.log_warning(
                    f"[{section_name}] No elements found for selector '{selector_query}' "
                    f"on page: {driver.get_current_url()}"
                )
                continue

            filtered_elements = [el for el in elements if el not in self.exclude_elements_set and el.text.strip()]
            text_content = ' '.join(ele.text.strip() for ele in filtered_elements if ele.text.strip())
            if text_content:
                return text_content

        # Missing or Mismatching Configuration
        self.missing_configuration.add(section_name)
        self.can_save_article = True

        return ''

    def exclude_elements(self, driver):
        self.exclude_elements_set = set()
        for ex in self.excludes:
            ex_type = ex.get("type")
            ex_query = ex.get("name")
            if not ex_type or not ex_query:
                continue

            try:
                by = By.CSS_SELECTOR if ex_type == "css" else By.XPATH
                exclude_elements = driver.find_elements(ex_query, by)
                self.exclude_elements_set.update(exclude_elements)
            except Exception as e:
                log.log_warning(f"Exclude selector error: {ex_query} | {e}")

    def crawl_date_from_article(self, selectors: List[dict], section_name: str, driver) -> dict:

        date_regex = self.config.get('dateRegex', [])

        for selector in selectors:
            selector_type = selector.get('type', '')
            selector_query = selector.get('name', '')
            attribute = selector.get('attribute', '')

            if not selector_type or not selector_query:
                continue  # Skip invalid selector entries

            by_type = {
                'css': By.CSS_SELECTOR,
                'xpath': By.XPATH
            }.get(selector_type)

            if not by_type:
                log.log_warning(f"[{section_name}] Unsupported selector type: '{selector_type}'")
                continue

            elements = driver.find_elements(selector_query, by_type)

            if elements:

                values = (
                    [el.get_attribute(attribute).strip() for el in elements if el.get_attribute(attribute)]
                    if attribute else
                    [el.text for el in elements if el.text.strip()]
                )

                if values:
                    return {'date': ' '.join(values), 'regex': date_regex}
                else:
                    log.log_warning(
                        f"Elements found but contain no text: '{selector_query}' at {driver.get_current_url()}")
            else:
                log.log_warning(f"Element '{selector_query}' not found on page: {driver.get_current_url()}")

        # Missing or Mismatching Configuration
        self.missing_configuration.add(section_name)
        self.can_save_article = True

        return {'date': ' ', 'regex': date_regex}

    def header(self, selectors: List[dict], driver) -> str:
        return self.crawl_from_article(selectors=selectors, section_name='Article Header', driver=driver)

    def body(self, selectors: List[dict], driver) -> str:
        return self.crawl_from_article(selectors=selectors, section_name='Article Body', driver=driver)

    def author(self, selectors: List[dict], driver) -> str:
        return self.crawl_from_article(selectors=selectors, section_name='Author', driver=driver)

    def keywords(self, selectors: List[dict], driver) -> List[str]:
        return self.crawl_keywords_from_article(selectors=selectors, section_name='Keywords', driver=driver)

    def parse_date(self, selectors: List[dict], driver) -> tuple[str, str]:
        output = self.crawl_date_from_article(selectors=selectors, section_name='Article Date', driver=driver)
        try:
            value = date_utils.get_matched_datetime_value(output.get('regex'), output.get('date'))
            date = value if value else output.get('date')
            parsed_date = date_utils.extract_date(date)
            return parsed_date, output.get('date')

        except Exception as e:
            log.log_error(f"Date-time parsing exception. Please check the format of the input: '{output.get('date')}'.",
                          e)
            return '', output.get('date')

    def extract(self, article: ArticleRequest) -> dict | None:
        log.log_separator()
        try:
            log.log_info('Initializing seleniumbase for web crawling.')

            # === Proxy Injection (Only if enabled) ===
            if self.config.get('useIpProxy', 0) == 1:

                log.log_info("[Proxy Config] useIpProxy enabled via configuration.")

                if ds.PROXY_ENABLED:
                    proxy = bot_utils.get_random_proxy()
                    os.environ["SB_PROXY"] = proxy
                    log.log_info(f"[Proxy Config] ✅ Proxy activated: {proxy}")
                else:
                    log.log_warning("[APP Config] 🔒 PROXY_ENABLED flag is disabled — skipping proxy injection.")
            else:
                os.environ.pop("SB_PROXY", None)  # Clear if disabled

            with SB(uc=True, browser='chrome', headless=False, ad_block_on=True, maximize=True) as sb:

                self.stealth_mode(sb)
                # cookies = []

                if self.config.get('login') == 1:
                    auth_status = self.handle_site_auth(sb).get('authenticate_status')
                    # cookies = sb.get_cookies()
                    if not auth_status:
                        return None

                sb.uc_open_with_reconnect(article.url, 2)

                time.sleep(25)

                # Set cookies before visiting the page again
                # for cookie in cookies:
                #     sb.driver.add_cookie(cookie)

                self.alert = False
                self.article_id = article.article_id
                self.article_url = article.url
                self.article = article

                article_info = self.extract_info_from_webpage(sb)

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
        except Exception as err:
            log.log_error('Error occurred while extracting', exception=err)
        finally:
            log.log_application_end()

    def extract_all(self, articles: List[ArticleRequest]) -> List[dict]:
        log.log_separator()
        try:
            log.log_info('Initializing seleniumbase for web crawling.')
            article_extracted_output = []

            USER_AGENT = self.generate_chrome_user_agent()

            # === Proxy Injection (Only if enabled) ===
            if self.config.get('useIpProxy', 0) == 1:

                log.log_info("[Proxy Config] useIpProxy enabled via configuration.")

                if ds.PROXY_ENABLED:
                    proxy = bot_utils.get_random_proxy()
                    os.environ["SB_PROXY"] = proxy
                    log.log_info(f"[Proxy Config] Proxy activated: {proxy}")
                else:
                    log.log_warning("[APP Config] PROXY_ENABLED flag is disabled — skipping proxy injection.")
            else:
                os.environ.pop("SB_PROXY", None)  # Clear if disabled

            with SB(uc=True, browser='chrome', headless=False,
                    ad_block_on=True, maximize=True, ) as sb:

                sb.driver.execute_cdp_cmd("Network.enable", {})
                sb.driver.execute_cdp_cmd("Network.setUserAgentOverride", {
                    "userAgent": USER_AGENT,
                    "platform": "Windows"
                })

                self.stealth_mode(sb)

                if self.config.get('login') == 1:
                    auth_status = self.handle_site_auth(sb).get('authenticate_status')
                    if not auth_status:
                        raise AuthenticationFailedException('Authentication failed')

                self.alert = False

                first = True

                for article in articles:
                    log.log_info(f"Started crawling URL - '{article.url}'")
                    sb.uc_open_with_reconnect(article.url, 2)

                    if first:
                        time.sleep(20)
                        first = False
                    time.sleep(10)

                    self.article_id = article.article_id
                    self.article_url = article.url
                    self.article = article

                    article_info = self.extract_info_from_webpage(sb)

                    article_info['article_id'] = article.article_id
                    article_info['preamble'] = article.preamble
                    article_info['sector'] = article.sector
                    article_info['link'] = article.url

                    # Inserting into database.
                    insert_article_data_into_db(article_info)

                    if self.can_publish:
                        mq.publish_message_into_article_analyzer(json.dumps(article_info))

                    article_extracted_output.append(article_info)
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

                return article_extracted_output
        except Exception as err:
            log.log_error('Error occurred while extracting', exception=err)
        finally:
            log.log_application_end()

    def handle_site_auth(self, driver) -> dict:
        log.log_info('Starting authentication process.')
        auth_info = SeleniumBaseImp.fetch_auth_config(self.newspaper_id)
        auth_config = auth_info.get('config', {})
        if not auth_config:
            log.log_warning('Missing authentication configuration.')
            return {'authenticate_status': False}

        if not auth_info.get('use_auto_signin', True):
            session_id_expires_at = auth_info.get('session_id_expires_at', None)
            if session_id_expires_at and session_id_expires_at > datetime.now():
                SeleniumBaseImp.inject_cookies_and_visit(driver=driver,
                                                         raw_cookie_string=auth_info.get("cookies", ""),
                                                         domain=auth_config.get('domain', ''),
                                                         target_url=auth_config.get('afterLoginUrl', ''))
                return {'authenticate_status': True}
            return {'authenticate_status': False}

        try:
            driver = driver.driver  # Assuming you have a driver instance
            driver.uc_open_with_reconnect(auth_config.get('loginUrl'), 2)

            credential = self.fetch_auth_credentials(self.newspaper_id)
            steps = auth_config.get('steps', {})

            # Simulate random scrolling
            self.random_scroll(driver)

            sorted_steps = sorted(steps, key=lambda x: x["step"])

            for step in sorted_steps:
                step_action = step.get('action')

                log.log_info(f"[STEP 1] Executing action: '{step.get('action')}' on element: '"
                             f"{step.get('name')}' (key: {step.get('key')})")

                if step_action == Action.TYPE.value:
                    self.human_like_typing(step.get('type'), step.get('name'), credential.get(step.get('key'), ''),
                                           driver)
                elif step_action == Action.CLICK.value:
                    self.click_element(step.get('type'), step.get('name'), driver)
                else:
                    log.log_warning(f"Unsupported action: {step_action}")
                    return {'authenticate_status': False}

                # Introduce random delay after each action
                time.sleep(random.uniform(1, 3))

            time.sleep(random.uniform(1, 3))

            if driver.get_current_url() == auth_config.get('afterLoginUrl'):
                return {'authenticate_status': True}

            log.log_info(f"Authentication failed for {self.newspaper_name}")
            return {'authenticate_status': False}

        except Exception as e:
            log.log_error('Error during authentication', e)
            return {'authenticate_status': False}

    @staticmethod
    def inject_cookies_and_visit(driver, target_url: str, domain: str, raw_cookie_string: str):
        # Visit domain root (required to set cookies)
        driver.get(target_url)

        # Parse raw cookie string like: "name1=value1; name2=value2"
        cookies = []
        for pair in raw_cookie_string.split(";"):
            if "=" in pair:
                name, value = pair.strip().split("=", 1)
                cookies.append({"name": name, "value": value, "domain": domain, "path": "/"})

        # Add cookies
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                log.log_error(f"Failed to add cookie {cookie}", exception=e)

    def fetch_auth_credentials(self, newspaper_id: int) -> dict:
        return db.fetch_newspaper_credential(newspaper_id)

    @staticmethod
    def fetch_auth_config(newspaper_id: int) -> dict:
        return db.fetch_auth_configuration(newspaper_id)

    def enter_text(self, locator_type: str, locator: str, text: str, driver) -> None:
        input_field = driver.find_element(Crawling.get_locator_type(locator_type), locator)
        input_field.send_keys(text)
        # Wait for a while to see the result
        time.sleep(random.uniform(0.5, 1.5))

    @staticmethod
    def random_scroll(driver):
        """Random scroll down to simulate human reading."""
        driver.execute_script("window.scrollBy(0, {})".format(random.randint(100, 500)))
        time.sleep(random.uniform(0.5, 1.5))

    @staticmethod
    def human_like_typing(locator_type: str, locator: str, text: str, driver, typo_chance=0.1) -> None:
        element = driver.find_element(Crawling.get_locator_type(locator_type), locator)
        for char in text:
            if random.random() < typo_chance:
                # Introduce a typo: type wrong character
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                element.send_keys(wrong_char)
                time.sleep(random.uniform(0.05, 0.2))
                # Correct it
                element.send_keys("\b")  # Backspace
                time.sleep(random.uniform(0.05, 0.2))

            element.send_keys(char)
            time.sleep(random.uniform(0.08, 0.25))  # Random delay per char

    def click_element(self, locator_type: str, locator: str, driver) -> None:
        self.random_scroll(driver)
        driver.click(locator, timeout=2000)

    def is_article_protected(self, driver):
        if self.config.get('login') == 1:
            site_identifier_locator = self.config.get('authConfig', {}).get('siteIdentifier', {}).get('name', None)
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

    def wait(self, locator_type: str, locator: str, driver) -> None:
        raise NotImplementedError("wait() cannot be performed")

    def page_action(self, locator_type: str, locator: str, duration: int, driver) -> None:

        width = 1280
        height = 720

        driver.set_window_size(width, height)
        # Create an instance of ActionChains
        actions = ActionChains(driver)

        # Set initial position (Move to an arbitrary start point)
        actions.move_by_offset(100, 100).perform()

        # Random movements within viewport
        num_movements = 3  # Number of movements
        for _ in range(num_movements):
            random_x = random.randint(-100, 100)  # Safe X range
            random_y = random.randint(-100, 100)  # Safe Y range

            try:
                actions.move_by_offset(random_x, random_y).perform()
                time.sleep(5)  # Pause between movements
            except Exception as e:
                print(f"❌ Movement error: {e}")

    @staticmethod
    def human_like_mouse_movement(driver):
        actions = ActionChains(driver)
        # Randomly move the mouse around
        for _ in range(random.randint(3, 6)):
            x_offset = random.randint(-50, 50)
            y_offset = random.randint(-50, 50)
            actions.move_by_offset(x_offset, y_offset).perform()
            time.sleep(random.uniform(0.5, 1.5))  # Random pause

    def stealth_mode(self, driver):
        # Remove WebDriver flag
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Add some dummy plugins
        driver.execute_script("""
        Object.defineProperty(navigator, 'plugins', { 
            get: () => [
                {
                    name: 'Chrome PDF Plugin',
                    filename: 'internal-pdf-viewer',
                    description: 'Portable Document Format'
                },
                {
                    name: 'Chrome PDF Viewer',
                    filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai',
                    description: ''
                },
                {
                    name: 'Native Client',
                    filename: 'internal-nacl-plugin',
                    description: ''
                }
            ] 
        });
        """)

        # Add languages
        driver.execute_script("""
        Object.defineProperty(navigator, 'languages', { 
            get: () => ['en-US', 'en'] 
        });
        """)

        # Fix WebGL fingerprinting
        driver.execute_script("""
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) { return 'NVIDIA Corporation'; }
            if (parameter === 37446) { return 'NVIDIA GeForce RTX 3090/PCIe/SSE2'; }
            return getParameter.call(this, parameter);
        };
        """)

        # Fake Permissions API (for push notifications detection)
        driver.execute_script("""
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = function (parameters) {
                if (parameters.name === 'notifications') {
                  return Promise.resolve({ state: Notification.permission });
                }
                return originalQuery(parameters);
            };
        """)
