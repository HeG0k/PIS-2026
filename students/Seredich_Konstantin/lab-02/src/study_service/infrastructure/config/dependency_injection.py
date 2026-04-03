from study_service.infrastructure.adapter.out_bound.in_memory_card_repository import InMemoryCardRepository
from study_service.application.service.card_study_service import CardStudyService
from study_service.infrastructure.adapter.in_bound.api_controller import CardController

class DependencyContainer:
    """Конфигурация DI: связывание портов и адаптеров (Сборка матрешки)"""
    
    def __init__(self):
        # 1. Создаем исходящие адаптеры (Инфраструктура)
        self.card_repository = InMemoryCardRepository()
        
        # 2. Создаем сервис (Application), передавая ему адаптеры под видом интерфейсов
        self.study_service = CardStudyService(card_repository=self.card_repository)
        
        # 3. Создаем контроллер, передавая ему сервис под видом UseCase-интерфейса
        self.card_controller = CardController(use_case=self.study_service)

    def get_controller(self) -> CardController:
        """Точка входа для запуска приложения"""
        return self.card_controller

# ДЕМОНСТРАЦИЯ РАБОТЫ АРХИТЕКТУРЫ
if __name__ == "__main__":
    print("--- Запуск приложения 'Говорю красиво' ---")
    container = DependencyContainer()
    api = container.get_controller()
    
    # Имитация прихода HTTP запроса от пользователя (пользователь ответил ВЕРНО)
    api.handle_review_request(card_id="card-123", is_correct=True)