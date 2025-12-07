import json

import pycurl
import certifi
from bs4 import BeautifulSoup
from logger import log
import requests

from model.article_request import ArticleRequest
from service.utils import mail_utils, date_utils, bot_utils
from service.rabbit_mq import rabbit_mq as mq


def bs4_config():
    print('yet to config')


def create_curl_instance():
    c = None
    try:
        c = pycurl.Curl()
        return c
    except Exception as err:
        log.log_error('Error occurred while instantiating CURL.', err)
        close_curl(c)


def close_curl(pycurl_obj):
    if pycurl_obj:
        pycurl_obj.close()


def make_request(url):
    try:
        # Make the request
        html_doc_response = requests.get(url, verify=certifi.where())
        # Check if the request was successful
        if html_doc_response.status_code == 200:
            # Decode the response content
            # Check the encoding from the response headers
            encoding = html_doc_response.encoding if html_doc_response.encoding else 'utf-8'  # Default to utf-8
            return html_doc_response.content.decode(encoding)
        else:
            raise html_doc_response.status_code
    except Exception as e:
        log.log_error(f'Error occurred while do http request: {url}.', e)


def initiate_html_parser(doc, config, parser_type='html.parser', url=''):
    soup = BeautifulSoup(doc, parser_type)
    header_value = element_parser(config.get('header', []), soup, 'header', url)
    body_value = element_parser(config.get('body', []), soup, 'body', url)
    author_value = element_parser(config.get('author', []), soup, 'author', url)
    parsed_date, date = parse_article_date(config.get('date', []), soup, url)

    return {
        'header': header_value,
        'body': body_value,
        'author': author_value,
        'date': date,
        'std_date': parsed_date,
        'language': config.get('language', ''),
        'newspaper_id': config.get('newspaperID', 0)
    }


def parse_article_date(selectors, soup, url):
    output = date_element_parser(selectors, soup, url)
    try:
        value = date_utils.get_matched_datetime_value(output.get('regex'), output.get('date'))
        date = value if value else output.get('date')
        parsed_date = date_utils.extract_date(date)
        return parsed_date, output.get('date')

    except Exception as e:
        log.log_error('date_time parsing exception: ', e)
        return '', output.get('date')


def element_parser(selector_config, soup, section_name, url):
    for sc in selector_config:
        if sc.get('type', '') == 'css':
            elements = soup.css.select(sc.get('name', ''))
            values = []
            if section_name == 'author':
                if elements:
                    for ele in elements:
                        values.append(str(ele.get_text()).replace('\n', ' ').replace('\t', ' '))
                    return str(' '.join(values)).strip()
            else:
                if elements:
                    for ele in elements:
                        values.append(ele.get_text(strip=True))
                    return str(' '.join(values)).strip()
        continue
    log.log_critical(
        f"Error: Required '{section_name}' configuration is missing for article URL: '{url}'. Please review the configuration.")
    return ''


def date_element_parser(selector_config, soup, url):
    for sc in selector_config:
        if sc.get('type', '') == 'css':
            elements = soup.css.select(sc.get('name', ''))
            values = []
            if elements:
                for ele in elements:
                    values.append(ele.get_text(strip=True).replace('\n', ''))
                return {'date': ''.join(values), 'regex': sc.get('regex', '')}
        continue
    log.log_critical(
        f"Error: Required 'Article Date' configuration is missing for article URL: '{url}'. Please review the configuration.")
    return {'date': ' ', 'regex': ''}


def extract(url, article_config, can_publish: bool):

    try:
        log.log_info(f"Started crawling URL - '{url}'")
        html_doc_response = make_request(url)
        log.log_separator()
        article_info = initiate_html_parser(html_doc_response, article_config, url)

        if can_publish:
            mq.publish_message_into_article_analyzer(json.dumps(article_info))

        return article_info
    except Exception as parser_err:
        log.log_error('Error occurred while parsing article using beautiful parser.', parser_err)
    finally:
        log.log_application_end()


def extract_batch(articles: list[ArticleRequest], article_config, can_publish: bool):

    try:
        article_extracted_list = []
        for article in articles:
            log.log_info(f"Started crawling URL - '{article.url}'")
            html_doc_response = make_request(article.url)
            article_info = initiate_html_parser(html_doc_response, article_config, article.url)
            article_info['article_id'] = article.article_id
            article_info['preamble'] = article.preamble
            article_info['sector'] = article.sector

            if can_publish:
                mq.publish_message_into_article_analyzer(json.dumps(article_info))

            article_extracted_list.append(article_info)
            log.log_separator()
        return article_extracted_list
    except Exception as parser_err:
        log.log_error('Error occurred while parsing article using beautiful parser.', parser_err)
    finally:
        log.log_application_end()
