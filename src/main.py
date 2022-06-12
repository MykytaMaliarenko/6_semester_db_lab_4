import csv
import logging
import time
import config as conf
from models import Student
from utils import extract_student
from pymongo.database import Database
from pymongo import MongoClient
from consts import SubjectCodes

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('app.log', mode='w'),
        logging.StreamHandler()
    ]
)


def prettify_csv_line(raw_line: dict) -> dict:
    return {
        key.lower(): value if value != 'null' else None
        for key, value in raw_line.items()
    }


def parse_file(db: Database, file, year: int):

    bulk = list()
    for index, line in enumerate(csv.DictReader(file, delimiter=';')):
        line = prettify_csv_line(line)
        student = extract_student(db, line, year)
        if student:
            bulk.append(student)

        if ((index + 1) % 10000) == 0:
            if len(bulk) > 0:
                Student.insert_many(db, bulk)
            logging.info(f'processed {index + 1} entries; inserted {len(bulk)}')
            bulk = []


def query_data(db: Database):
    pipeline = [
        {"$match": {"exams.subject.code": SubjectCodes.PHYSICS.value.lower()}},
        {"$unwind": "$exams"},
        {"$group": {
            "_id": {
                "region": "$exams.educational_institution.place.region.name",
                "year": "$exams.year"
            },
            "maxScore": {"$max": "$exams.score"}
        }},
    ]

    data = db.Student.aggregate(pipeline)

    with open('query_results.csv', mode='w') as file:
        write = csv.writer(file)
        write.writerow(['Region', 'Year', 'Max Score'])

        for line in data:
            write.writerow([
                line['_id']['region'],
                line['_id']['year'],
                line['maxScore']
            ])


def main():
    client = MongoClient(conf.DB_CONNECTION_STRING)
    db = client['lab_4']

    for file_info in conf.FILES_TO_PARSE:
        start_time = time.time()
        logging.info(f'start handling file: {file_info.path}')
        with open(
                file_info.path,
                mode='r',
                encoding=file_info.encoding
        ) as infile:
            parse_file(db, infile, file_info.year)

        logging.info(
            f'finished handling file: {file_info.path}; '
            f'took time: {round(time.time() - start_time)} seconds'
        )

    logging.info('Querying data...')
    query_data(db)


if __name__ == '__main__':
    main()
