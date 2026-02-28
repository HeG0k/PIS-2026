"""
GetRequestByIdHandler: Обработчик запроса заявки по ID

Предметная область: ПСО «Юго-Запад»
"""
from application.query.get_request_by_id_query import GetRequestByIdQuery
from application.query.dto.request_dto import RequestDto
from domain.models.request import Request


class GetRequestByIdHandler:
    """
    Handler: Получить заявку по ID
    
    Шаги:
    1. Загрузить Request из Repository
    2. Преобразовать в RequestDto
    3. Вернуть DTO
    """
    
    def __init__(self, request_repository):
        self.request_repository = request_repository
    
    def handle(self, query: GetRequestByIdQuery) -> RequestDto:
        """
        Обработать запрос GetRequestById
        
        Returns:
            RequestDto - упрощённая модель для чтения
        
        Raises:
            ValueError: Если заявка не найдена
        """
        # 1. Загрузка из репозитория
        request = self.request_repository.find_by_id(query.request_id)
        
        if not request:
            raise ValueError(f"Request {query.request_id} не найдена")
        
        # 2. Преобразование в DTO
        return self._map_to_dto(request)
    
    def _map_to_dto(self, request: Request) -> RequestDto:
        """Преобразовать доменную модель в DTO"""
        return RequestDto(
            request_id=request.request_id,
            coordinator_id=request.coordinator_id,
            status=request.status.value,
            zone_name=request.zone.name,
            zone_bounds=request.zone.bounds,
            assigned_group_id=request.assigned_group.group_id if request.assigned_group else None,
            created_at=request.created_at,
            activated_at=request.activated_at,
            completed_at=request.completed_at
        )
