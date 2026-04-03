from typing import List, Optional
from datetime import datetime
from .value_objects import CardContent, ReviewGrade, DeckSettings, EmailAddress
from .events import DomainEvent, CardAddedToDeckEvent, CardReviewedEvent
from .exceptions import DeckArchivedException, InvalidCardContentException

class Student:
    """Entity 1: Студент (Пользователь)"""
    def __init__(self, student_id: str, email: EmailAddress, nickname: str):
        self.id = student_id
        self.email = email
        self._nickname = nickname # Приватное поле
        self.is_active = True
        
    def ban_student(self):
        """Бизнес-метод вместо сеттера"""
        self.is_active = False

    def __eq__(self, other):
        # Сущности равны только если равны их ID
        if not isinstance(other, Student): return False
        return self.id == other.id
        
    def __hash__(self): return hash(self.id)

class Card:
    """Entity 2: Карточка (Внутренняя сущность Агрегата)"""
    def __init__(self, card_id: str, content: CardContent):
        self.id = card_id
        self.content = content
        self.interval_days = 0
        
    def apply_review(self, grade: ReviewGrade) -> int:
        """Логика интервального повторения"""
        if grade.score == 1:
            self.interval_days = 0 # Забыли, начинаем сначала
        elif grade.score == 2:
            self.interval_days = max(1, self.interval_days) # Трудно, интервал не растет
        elif grade.score == 3:
            self.interval_days = max(1, self.interval_days * 2) # Хорошо, х2
        elif grade.score == 4:
            self.interval_days = max(1, self.interval_days * 3) # Легко, х3
            
        return self.interval_days

    def __eq__(self, other):
        if not isinstance(other, Card): return False
        return self.id == other.id
        
    def __hash__(self): return hash(self.id)

class Deck:
    """Entity 3 & AGGREGATE ROOT: Колода карточек"""
    def __init__(self, deck_id: str, title: str, settings: DeckSettings, owner_id: str):
        self.id = deck_id
        
        if not title or len(title) < 3:
            raise ValueError("Название колоды минимум 3 символа")
        self._title = title
        
        self._settings = settings
        self._owner_id = owner_id
        self._cards: List[Card] = [] # Инкапсулированный список
        self._is_archived = False
        self._events: List[DomainEvent] = [] # Очередь событий
        
    # --- БИЗНЕС ЛОГИКА АГРЕГАТА ---
    
    def add_card(self, card_id: str, term: str, definition: str):
        """Добавление карточки через Aggregate Root (защита инвариантов)"""
        # Инвариант 1: Нельзя добавлять карточки в архивную колоду
        if self._is_archived:
            raise DeckArchivedException("Нельзя добавить карточку в архивную колоду")
            
        try:
            content = CardContent(term=term, definition=definition)
        except ValueError as e:
             # Инвариант 2: Валидный контент
             raise InvalidCardContentException(str(e))
             
        # Инвариант 3: Защита от дубликатов по термину
        if any(c.content.term == term for c in self._cards):
            raise InvalidCardContentException(f"Карточка с термином '{term}' уже существует в колоде")
            
        new_card = Card(card_id, content)
        self._cards.append(new_card)
        
        # Генерируем доменное событие
        self._events.append(CardAddedToDeckEvent(self.id, card_id, term))

    def review_card(self, card_id: str, grade_score: int):
        """Ответ на карточку"""
        if self._is_archived:
            raise DeckArchivedException("Нельзя изучать архивную колоду")
            
        card = next((c for c in self._cards if c.id == card_id), None)
        if not card:
            raise ValueError("Карточка не найдена в этой колоде")
            
        grade = ReviewGrade(grade_score)
        new_interval = card.apply_review(grade)
        
        self._events.append(CardReviewedEvent(card_id, grade_score, new_interval))

    def archive_deck(self):
        self._is_archived = True

    # Методы для работы с событиями (Infrastructure будет их забирать)
    def pull_events(self) -> List[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events

    def get_cards_count(self) -> int:
        return len(self._cards)

    def __eq__(self, other):
        if not isinstance(other, Deck): return False
        return self.id == other.id
        
    def __hash__(self): return hash(self.id)