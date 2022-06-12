import typing as t
from pymongo.database import Database
from pymongo.collection import Collection
from dataclasses import dataclass, asdict


@dataclass
class AbstractModel:
    def as_dict(self) -> t.Dict:
        return asdict(
            self,
            dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )

    @classmethod
    def get_collection(cls, db: Database) -> Collection:
        return db.get_collection(cls.__name__)

    def get_or_create(self, db: Database) -> 'AbstractModel':
        collection = self.get_collection(db)

        raw_data = collection.find_one(self.as_dict())
        if raw_data:
            return self.__class__(**raw_data)

        self._id = collection.insert_one(self.as_dict()).inserted_id
        return self

    @classmethod
    def insert_many(cls, db: Database, instances: t.List['AbstractModel']):
        collection = cls.get_collection(db)
        collection.insert_many([instance.as_dict() for instance in instances])

    @property
    def id(self) -> str:
        return self._id


@dataclass
class Region:
    name: str


@dataclass
class Area:
    name: str


@dataclass
class Territory:
    name: str


@dataclass
class Place:
    region: Region
    area: Area
    territory: Territory

    _id: t.Optional[str] = None


@dataclass
class EducationalInstitution:
    name: str
    place: Place

    _id: t.Optional[str] = None


@dataclass
class Subject:
    code: str
    name: str


@dataclass
class Exam:
    educational_institution: EducationalInstitution

    subject: Subject

    raw_score: float
    score: float
    school_score: int

    year: int
    status: str


@dataclass
class Student(AbstractModel):
    gender: str
    birth_year: int

    place_of_living: Place
    exams: t.List[Exam]

    studying_lang: t.Optional[str] = None
    educational_institution_id: t.Optional[EducationalInstitution] = None
    class_profile: t.Optional[str] = None

    _id: t.Optional[str] = None
