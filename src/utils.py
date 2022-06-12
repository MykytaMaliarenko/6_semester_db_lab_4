import models
import typing as t
from functools import cache
from consts import SubjectCodes
from pymongo.database import Database


def parse_float(v: str) -> float:
    return float(v.replace(',', '.'))


def extract_exams(
        entry: t.Dict,
        year: int
) -> list[models.Exam]:
    parsed_exams = list()
    for subject in SubjectCodes:
        code = subject.value.lower()

        pt_name = entry[f'{code}ptname']
        pt_reg_name = entry[f'{code}ptregname']
        pt_area_name = entry[f'{code}ptareaname']
        pt_ter_name = entry[f'{code}pttername']
        ball = entry[f'{code}ball']
        ball100 = entry[f'{code}ball100']
        ball12 = entry[f'{code}ball12']
        test_status = entry[f'{code}teststatus']
        if pt_name is None or ball is None or ball12 is None:
            continue

        parsed_exams.append(
            models.Exam(
                subject=models.Subject(
                    code=subject.value.lower(),
                    name=subject.name
                ),
                educational_institution=models.EducationalInstitution(
                    name=pt_name,
                    place=models.Place(
                        region=models.Region(name=pt_reg_name),
                        area=models.Area(name=pt_area_name),
                        territory=models.Territory(name=pt_ter_name)
                    )
                ),
                raw_score=parse_float(ball),
                score=parse_float(ball100),
                school_score=int(ball12),
                year=year,
                status=test_status
            ))

    return parsed_exams


def extract_student(
        db: Database,
        entry: t.Dict,
        year: int
) -> t.Optional[models.Student]:
    _id = entry['outid']
    student = models.Student.get_collection(db).find_one(
        {
            '_id': _id
        })
    if student is not None:
        return None

    return models.Student(
        gender=entry['sextypename'],
        birth_year=int(entry['birth']),
        studying_lang=entry['classlangname'],
        place_of_living=models.Place(
            region=models.Region(name=entry['regname']),
            area=models.Area(name=entry['areaname']),
            territory=models.Territory(name=entry['tername']),
        ),
        educational_institution_id=models.EducationalInstitution(
            name=entry['eoname'],
            place=models.Place(
                region=models.Region(name=entry['eoregname']),
                area=models.Area(name=entry['eoareaname']),
                territory=models.Territory(name=entry['eotername'])
            )
        ) if entry['eoname'] else None,
        exams=extract_exams(entry, year),
        class_profile=entry['classprofilename'],
        _id=entry['outid']
    )
