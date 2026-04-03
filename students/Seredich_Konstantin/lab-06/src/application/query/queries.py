from dataclasses import dataclass

# --- Запросы (Queries) ---
@dataclass(frozen=True)
class GetDeckByIdQuery:
    deck_id: str

# --- Read DTO (Результаты) ---
@dataclass(frozen=True)
class DeckReadDto:
    """Упрощенная модель для UI. Без бизнес-методов, только данные."""
    id: str
    title: str
    cards_count: int
    is_archived: bool