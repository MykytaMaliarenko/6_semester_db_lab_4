from os import environ
from dataclasses import dataclass

__all__ = [
    'DB_CONNECTION_STRING',
    'DATA_DIRECTORY',
    'FILES_TO_PARSE',
    'BULK_UPLOAD_SIZE'
]

BULK_UPLOAD_SIZE = 5000

DB_HOST = environ.get('DB_HOST')
DB_USER = environ.get('DB_USER')
DB_PASSWORD = environ.get('DB_PASSWORD')
DB_CONNECTION_STRING = f'mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:27017/'

DATA_DIRECTORY = '../zno_data/'


@dataclass
class FileToParse:
    path: str
    year: int
    encoding: str


FILES_TO_PARSE = [
    FileToParse(
        path=DATA_DIRECTORY + 'Odata2021File.csv',
        year=2021,
        encoding='utf-8-sig'
    ),
    FileToParse(
        path=DATA_DIRECTORY + 'Odata2019File.csv',
        year=2019,
        encoding='cp1251'
    )
]
