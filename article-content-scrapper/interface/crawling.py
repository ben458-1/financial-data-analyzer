from abc import ABC, abstractmethod
from typing import List, Optional
import random

from logger import log
from core.config import data_source as ds

from model.article_request import ArticleRequest


class Crawling(ABC):
    """
    Abstract base class for web crawling operations.
    This class defines the essential methods required for extracting information from web pages,
    handling authentication, processing captcha's, and interacting with webpage elements.
    """

    @abstractmethod
    def automation_tool_config(self, driver) -> None:
        """
        Configure the automation tool (e.g., Selenium WebDriver) before crawling.

        :param driver: The web driver instance to be configured.
        """
        pass

    @abstractmethod
    def extract_info_from_webpage(self, driver) -> dict | None:
        """
        Extract relevant information from a webpage based on the given configuration.

        :param driver: The web driver instance.
        :return: Extracted data as a dictionary or None if extraction fails.
        """
        pass

    @abstractmethod
    def process_captcha(self):
        """
        Handle CAPTCHA challenges encountered during crawling.
        """
        pass

    @abstractmethod
    def authenticate_user(self):
        """
        Perform user authentication if required by the website.
        """
        pass

    @abstractmethod
    def crawl_from_article(self, selectors: dict, section_name: str, driver) -> str:
        """
        Extract specific section content from an article.

        :param selectors: Dictionary containing selectors for different sections.
        :param section_name: The name of the section to extract.
        :param driver: The web driver instance.
        :return: Extracted text content of the specified section.
        """
        pass

    @abstractmethod
    def crawl_keywords_from_article(self, selectors: dict, section_name: str, driver) -> List[str]:
        """
                Extract specific section content from an article.

                :param selectors: Dictionary containing selectors for different sections.
                :param section_name: The name of the section to extract.
                :param driver: The web driver instance.
                :return: Extracted List of text content of the specified section.
                """
        pass

    @abstractmethod
    def crawl_date_from_article(self, selectors: dict, section_name: str, driver) -> dict:
        """
        Extract the publication date from an article.

        :param selectors: Dictionary containing selectors for different date fields.
        :param section_name: The name of the section where the date is located.
        :param driver: The web driver instance.
        :return: Dictionary containing extracted date information.
        """
        pass

    @abstractmethod
    def header(self, selectors: dict, driver) -> str:
        """
        Extract the article header/title.

        :param selectors: Dictionary containing selectors for the header.
        :param driver: The web driver instance.
        :return: Extracted header text.
        """
        pass

    @abstractmethod
    def body(self, selectors: dict, driver) -> str:
        """
        Extract the main body content of an article.

        :param selectors: Dictionary containing selectors for the body.
        :param driver: The web driver instance.
        :return: Extracted body text.
        """
        pass

    @abstractmethod
    def author(self, selectors: dict, driver) -> str:
        """
        Extract the author name from an article.

        :param selectors: Dictionary containing selectors for the author field.
        :param driver: The web driver instance.
        :return: Extracted author name.
        """
        pass

    @abstractmethod
    def parse_date(self, selectors: dict, driver) -> tuple[str, str]:
        """
        Extract and parse the article's published and modified dates.

        :param selectors: Dictionary containing selectors for date extraction.
        :param driver: The web driver instance.
        :return: Tuple containing the published and modified dates as strings.
        """
        pass

    @abstractmethod
    def extract(self, url: str) -> dict | None:
        """
        Extract data from a given URL based on the provided configuration.

        :param url: The URL of the article.
        :return: Extracted data as a dictionary.
        """
        pass

    @abstractmethod
    def extract_all(self, articles: List[ArticleRequest]) -> List[dict]:
        """
        Extract data from multiple articles in batch processing.

        :param articles: List of ArticleRequest objects containing article details.
        :return: List of extracted data dictionaries.
        """
        pass

    @abstractmethod
    def handle_site_auth(self, driver) -> dict:
        """
        Handle site authentication (e.g., login, session management).

        :param driver: The web driver instance.
        :return: Dictionary containing authentication-related information.
        """
        pass

    @abstractmethod
    def fetch_auth_credentials(self, newspaper_id: int) -> dict:
        """
        Fetch authentication credentials for a specific newspaper.

        :param newspaper_id: Identifier of the newspaper.
        :return: Dictionary containing authentication credentials.
        """
        pass

    @abstractmethod
    def enter_text(self, locator_type: str, locator: str, text: str, driver) -> None:
        """
        Enter text into an input field on a webpage.

        :param locator_type: Type of locator (e.g., ID, XPath, CSS selector).
        :param locator: The locator string to find the input field.
        :param text: The text to enter.
        :param driver: The web driver instance.
        """
        pass

    @abstractmethod
    def click_element(self, locator_type: str, locator: str, driver) -> None:
        """
        Click an element on a webpage.

        :param locator_type: Type of locator (e.g., ID, XPath, CSS selector).
        :param locator: The locator string to find the element.
        :param driver: The web driver instance.
        """
        pass

    @abstractmethod
    def wait(self, locator_type: str, locator: str, driver) -> None:
        """
        Click an element to wait some time on a webpage.

        :param locator_type: Type of locator (e.g., ID, XPath, CSS selector).
        :param locator: The locator string to find the element.
        :param driver: The web driver instance.
        """
        pass

    @abstractmethod
    def page_action(self, locator_type: str, locator: str, duration: int, driver) -> None:
        """
        Make some Action on a webpage.

        :param locator_type: Type of locator (e.g., ID, XPath, CSS selector).
        :param locator: The locator string to find the element.
        :param duration: Make movement of page given duration.
        :param driver: The web driver instance.
        """
        pass

    @abstractmethod
    def is_article_protected(self, driver):
        """
        Check if an article is behind a paywall or protected.

        :param driver: The web driver instance.
        :return: Boolean indicating whether the article is protected.
        """
        pass

    @abstractmethod
    def stealth_mode(self, driver) -> None:
        pass

    @staticmethod
    def generate_chrome_user_agent():
        chrome_versions = [
            "136.0.0.0",
            "135.0.0.0",
            "134.0.0.0",
            "133.0.0.0"
        ]
        os_versions = [
            "Windows NT 10.0; Win64; x64"
        ]

        chrome_version = random.choice(chrome_versions)
        os_version = random.choice(os_versions)

        user_agent = (
            f"Mozilla/5.0 ({os_version}) AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/{chrome_version} Safari/537.36"
        )

        return user_agent

    @staticmethod
    def generate_edge_user_agent():
        edge_versions = [
            "136.0.0.0",
            "135.0.0.0",
            "133.0.0.0"
        ]
        os_versions = [
            "Windows NT 10.0; Win64; x64",
            "Windows NT 10.0; WOW64",
            "Macintosh; Intel Mac OS X 10_15_7",
            "X11; Ubuntu; Linux x86_64"
        ]

        edge_version = random.choice(edge_versions)
        os_version = random.choice(os_versions)

        user_agent = (
            f"Mozilla/5.0 ({os_version}) AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Edg/{edge_version} Safari/537.36"
        )

        return user_agent

    @staticmethod
    def generate_firefox_user_agent():
        firefox_versions = [
            "122.0",
            "121.0",
            "120.0",
            "118.0"
        ]
        os_versions = [
            "Windows NT 10.0; Win64; x64",
            "Windows NT 10.0; WOW64",
            "Macintosh; Intel Mac OS X 10_15_7",
            "X11; Ubuntu; Linux x86_64",
            "iPhone; CPU iPhone OS 14_0 like Mac OS X",
            "Android 10; Mobile; Nexus 5X"
        ]

        firefox_version = random.choice(firefox_versions)
        os_version = random.choice(os_versions)

        user_agent = (
            f"Mozilla/5.0 ({os_version}; rv:{firefox_version}) Gecko/20100101 Firefox/{firefox_version}"
        )

        return user_agent

    @staticmethod
    def generate_android_user_agent():
        android_versions = ["12", "13", "14"]
        device_models = [
            "Nexus 5X",
            "Pixel 6a",
            "Samsung Galaxy S10",
            "OnePlus 9",
            "Xiaomi Mi 10"
        ]

        android_version = random.choice(android_versions)
        device_model = random.choice(device_models)

        user_agent = (
            f"Mozilla/5.0 (Linux; Android {android_version}; {device_model}) "
            f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Mobile Safari/537.36"
        )

        return user_agent

    @staticmethod
    def get_locator_type(locator):
        ID = "id"
        XPATH = "xpath"
        LINK_TEXT = "link text"
        PARTIAL_LINK_TEXT = "partial link text"
        NAME = "name"
        TAG_NAME = "tag name"
        CLASS_NAME = "class name"
        CSS_SELECTOR = "css selector"

        std_loc = {
            "css": CSS_SELECTOR,
            "id": ID,
            "xpath": XPATH,
            "link_text": LINK_TEXT,
            "partial_link_text": PARTIAL_LINK_TEXT,
            "name": NAME,
            "tag_name": TAG_NAME,
            "class_name": CLASS_NAME
        }
        return std_loc.get(locator)
