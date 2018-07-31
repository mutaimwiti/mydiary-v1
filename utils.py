import os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv())

NOT_FOUND_MSG = 'Not found.'
SERVER_ERROR_MSG = 'Internal server error.'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def env(key, default=None):
    return os.environ.get(key, default)


def full_path(path=None):
    if path is None:
        return ROOT_DIRECTORY
    return ROOT_DIRECTORY + '/' + path


def parse_date(date_string):
    return datetime.strptime(date_string, DATE_FORMAT)
