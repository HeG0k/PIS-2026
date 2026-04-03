from dataclasses import dataclass

@dataclass(frozen=True)
class CreateDeckCommand:
    """Команда: Создать новую колоду"""
    deck_id: str
    title: str
    owner_id: str

    def __post_init__(self):
        if not self.deck_id or not self.deck_id.strip():
            raise ValueError("ID колоды не может быть пустым (NotBlank)")
        if not self.title or len(self.title.strip()) < 3:
            raise ValueError("Название должно содержать минимум 3 символа")

@dataclass(frozen=True)
class AddCardCommand:
    """Команда: Добавить карточку в колоду"""
    deck_id: str
    card_id: str
    term: str
    definition: str

    def __post_init__(self):
        if not self.deck_id or not self.card_id:
            raise ValueError("ID колоды и карточки обязательны")
        if not self.term or not self.definition:
            raise ValueError("Термин и определение не могут быть пустыми")