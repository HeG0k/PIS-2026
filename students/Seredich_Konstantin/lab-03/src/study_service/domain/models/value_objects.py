from dataclasses import dataclass
import re

@dataclass(frozen=True) # frozen=True делает класс Immutable
class CardContent:
    """VO 1: Содержимое карточки (Термин и Определение)"""
    term: str
    definition: str

    def __post_init__(self):
        if not self.term or len(self.term.strip()) < 2:
            raise ValueError("Термин должен содержать минимум 2 символа")
        if not self.definition or len(self.definition.strip()) < 2:
            raise ValueError("Определение не может быть пустым")

@dataclass(frozen=True)
class ReviewGrade:
    """VO 2: Оценка пользователя при повторении (от 1 до 4)"""
    score: int # 1-Снова, 2-Трудно, 3-Хорошо, 4-Легко

    def __post_init__(self):
        if self.score not in [1, 2, 3, 4]:
            raise ValueError("Оценка должна быть от 1 до 4")

@dataclass(frozen=True)
class DeckSettings:
    """VO 3: Настройки колоды"""
    max_new_cards_per_day: int
    
    def __post_init__(self):
        if self.max_new_cards_per_day <= 0:
            raise ValueError("Лимит новых карточек должен быть больше нуля")

@dataclass(frozen=True)
class EmailAddress:
    """VO 4: Email владельца колоды"""
    value: str

    def __post_init__(self):
        # Простая валидация email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.value):
            raise ValueError("Некорректный формат email")