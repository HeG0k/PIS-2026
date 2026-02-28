"""
Domain Layer: Zone (Зона поиска)

Value Object: Зона поиска с географическими координатами
Предметная область: ПСО «Юго-Запад»
"""
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)  # frozen=True делает класс immutable
class Zone:
    """
    Value Object: Зона поиска с координатами
    
    Attributes:
        name: Название зоны ("North", "South", "East", "West")
        bounds: Границы (lat_min, lat_max, lon_min, lon_max)
    
    Invariants:
        - Latitude в диапазоне [-90, 90]
        - Longitude в диапазоне [-180, 180]
        - lat_min < lat_max
        - lon_min < lon_max
    """
    
    name: str
    bounds: Tuple[float, float, float, float]  # (lat_min, lat_max, lon_min, lon_max)
    
    def __post_init__(self):
        """Валидация при создании"""
        if not self.name:
            raise ValueError("Zone name cannot be empty")
        
        lat_min, lat_max, lon_min, lon_max = self.bounds
        
        # Проверка диапазонов
        if not (-90 <= lat_min <= 90 and -90 <= lat_max <= 90):
            raise ValueError(
                f"Latitude must be in range [-90, 90]: {lat_min}, {lat_max}"
            )
        
        if not (-180 <= lon_min <= 180 and -180 <= lon_max <= 180):
            raise ValueError(
                f"Longitude must be in range [-180, 180]: {lon_min}, {lon_max}"
            )
        
        # Проверка порядка
        if lat_min >= lat_max:
            raise ValueError(
                f"lat_min must be < lat_max: {lat_min} >= {lat_max}"
            )
        
        if lon_min >= lon_max:
            raise ValueError(
                f"lon_min must be < lon_max: {lon_min} >= {lon_max}"
            )
    
    def contains_point(self, lat: float, lon: float) -> bool:
        """
        Проверить, находится ли точка в зоне
        
        Args:
            lat: Широта точки
            lon: Долгота точки
        
        Returns:
            True если точка внутри зоны
        """
        lat_min, lat_max, lon_min, lon_max = self.bounds
        return lat_min <= lat <= lat_max and lon_min <= lon <= lon_max
    
    def area_km2(self) -> float:
        """
        Примерная площадь зоны в км²
        
        Упрощённый расчёт (не учитывает кривизну Земли)
        """
        lat_min, lat_max, lon_min, lon_max = self.bounds
        
        # 1 градус широты ≈ 111 км
        # 1 градус долготы ≈ 111 км * cos(latitude)
        lat_delta = lat_max - lat_min
        lon_delta = lon_max - lon_min
        
        avg_lat = (lat_min + lat_max) / 2
        
        import math
        km_per_deg_lat = 111.0
        km_per_deg_lon = 111.0 * math.cos(math.radians(avg_lat))
        
        return (lat_delta * km_per_deg_lat) * (lon_delta * km_per_deg_lon)
    
    # Равенство и хэш генерируются автоматически в @dataclass
    # Два Zone с одинаковыми name и bounds - ОДНО И ТО ЖЕ


# Предопределённые зоны для ПСО «Юго-Запад»
NORTH_ZONE = Zone(
    name="North",
    bounds=(52.0, 52.5, 23.5, 24.0)  # Примерные координаты севера Бреста
)

SOUTH_ZONE = Zone(
    name="South", 
    bounds=(51.5, 52.0, 23.5, 24.0)
)

EAST_ZONE = Zone(
    name="East",
    bounds=(51.8, 52.3, 24.0, 24.5)
)

WEST_ZONE = Zone(
    name="West",
    bounds=(51.8, 52.3, 23.0, 23.5)
)
