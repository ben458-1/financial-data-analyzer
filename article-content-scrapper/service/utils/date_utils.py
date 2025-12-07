import regex
from dateutil.parser import ParserError
import dateparser

from dateutil import parser
from logger import log
from datetime import datetime


def get_matched_datetime_value(_regex_, value: str):
    if _regex_ and value:
        try:
            for re in _regex_:
                match = regex.search(re, value)
                if match:
                    t = match.group('time') if 'time' in match.groupdict() else ''
                    d = match.group('date')
                    return f'{d} {t}'
        except Exception as e:
            log.log_error("Error occurred during regex matching.", e)
    return ''


def extract_date(value):
    try:
        parsed_output = parser.parse(value)
        return parsed_output.isoformat()
    except ParserError as e:
        try:
            parsed_output = dateparser.parse(value)
            return parsed_output.isoformat() if parsed_output else parsed_output
        except Exception as e:
            log.log_error(f"Date-time parsing exception. Please check the format of the input: '{value}'.", e)
            return ''
    except Exception as e:
        log.log_error(f"Date-time parsing exception. Please check the format of the input: '{value}'.", e)
        return ''


def current_year() -> int:
    now = datetime.now()
    # Extract the current year
    return now.year

