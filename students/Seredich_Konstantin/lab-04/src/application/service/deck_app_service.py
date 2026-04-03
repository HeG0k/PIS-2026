from src.application.command.commands import CreateDeckCommand, AddCardCommand
from src.application.query.queries import GetDeckByIdQuery, DeckReadDto
from src.application.command.handlers.create_deck_handler import CreateDeckHandler
from src.application.command.handlers.add_card_handler import AddCardHandler
from src.application.query.handlers.get_deck_handler import GetDeckByIdHandler

class DeckApplicationService:
    """Сервис-фасад, делегирующий вызовы нужным обработчикам"""
    
    def __init__(
        self, 
        create_handler: CreateDeckHandler, 
        add_card_handler: AddCardHandler,
        get_deck_handler: GetDeckByIdHandler
    ):
        self.create_handler = create_handler
        self.add_card_handler = add_card_handler
        self.get_deck_handler = get_deck_handler

    def create_deck(self, command: CreateDeckCommand) -> str:
        return self.create_handler.handle(command)

    def add_card(self, command: AddCardCommand) -> None:
        self.add_card_handler.handle(command)

    def get_deck(self, query: GetDeckByIdQuery) -> DeckReadDto:
        return self.get_deck_handler.handle(query)