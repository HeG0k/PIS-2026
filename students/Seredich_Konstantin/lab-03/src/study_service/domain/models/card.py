from datetime import datetime, timedelta

class Card:
    """Доменная модель: Карточка для запоминания"""
    
    def __init__(self, card_id: str, term: str, definition: str):
        self.card_id = card_id
        self.term = term
        self.definition = definition
        self.interval_days = 0  # Интервал до следующего повторения
        self.next_review = datetime.now()

    def record_review(self, is_correct: bool) -> None:
        """
        Бизнес-логика: Расчет интервального повторения.
        Если ответ верный, увеличиваем интервал. Если нет - сбрасываем.
        """
        if is_correct:
            self.interval_days = max(1, self.interval_days * 2)
        else:
            self.interval_days = 0
            
        self.next_review = datetime.now() + timedelta(days=self.interval_days)