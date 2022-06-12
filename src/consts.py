from enum import Enum


class SubjectCodes(Enum):
    UKRAINIAN_LANGUAGE_AND_LITERATURE = 'Ukr'
    HISTORY = 'Hist'
    MATH = 'Math'
    PHYSICS = 'Phys'
    CHEMISTRY = 'Chem'
    BIOLOGY = 'Bio'
    GEOGRAPHY = 'Geo'
    ENGLISH = 'Eng'
    FRENCH = 'Fra'
    GERMAN = 'Deu'
    SPANISH = 'Spa'

    @property
    def name(self) -> str:
        if self == SubjectCodes.UKRAINIAN_LANGUAGE_AND_LITERATURE:
            return 'Українська мова і література'
        elif self == SubjectCodes.HISTORY:
            return 'Історія України'
        elif self == SubjectCodes.MATH:
            return 'Математика'
        elif self == SubjectCodes.PHYSICS:
            return 'Фізика'
        elif self == SubjectCodes.CHEMISTRY:
            return 'Хімія'
        elif self == SubjectCodes.BIOLOGY:
            return 'Біологія'
        elif self == SubjectCodes.GEOGRAPHY:
            return 'Географія'
        elif self == SubjectCodes.ENGLISH:
            return 'Англійська мова'
        elif self == SubjectCodes.FRENCH:
            return 'Французька мова'
        elif self == SubjectCodes.GERMAN:
            return 'Німецька мова'
        elif self == SubjectCodes.SPANISH:
            return 'Іспанська мова'
        else:
            return super(SubjectCodes, self).name
