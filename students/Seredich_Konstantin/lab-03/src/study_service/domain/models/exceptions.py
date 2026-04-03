class DomainException(Exception):
    """Базовый класс для доменных ошибок"""
    pass

class InvalidCardContentException(DomainException):
    pass

class DeckArchivedException(DomainException):
    pass

class DailyLimitExceededException(DomainException):
    pass