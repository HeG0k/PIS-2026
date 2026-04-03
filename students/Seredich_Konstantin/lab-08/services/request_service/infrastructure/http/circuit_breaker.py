"""
Circuit Breaker: Защита от каскадных сбоев

Предметная область: ПСО «Юго-Запад»
"""
from typing import Any, Dict, Optional

import requests
from pybreaker import CircuitBreaker, CircuitBreakerError


class GroupServiceClient:
    """
    HTTP Client для Group Service с Circuit Breaker

    Паттерн: Circuit Breaker (Michael Nygard)
    Ответственность: Предотвращение каскадных сбоев при вызове Group Service
    """

    def __init__(self, base_url: str = "http://group-service:8000"):
        self.base_url = base_url

    def get_group(self, group_id: str) -> Optional[Dict[str, Any]]:
        try:
            return self._get_group_protected(group_id)
        except CircuitBreakerError:
            print("⚠️ Circuit breaker is OPEN for Group Service")
            return None

    @CircuitBreaker(fail_max=5, reset_timeout=60)
    def _get_group_protected(self, group_id: str) -> Dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/groups/{group_id}",
            timeout=5,
        )
        response.raise_for_status()
        return response.json()

    def find_ready_group(self) -> Optional[Dict[str, Any]]:
        try:
            return self._find_ready_group_protected()
        except (CircuitBreakerError, requests.RequestException) as e:
            print(f"⚠️ Failed to find ready group: {e}")
            return self._get_cached_group()

    @CircuitBreaker(fail_max=5, reset_timeout=60)
    def _find_ready_group_protected(self) -> Dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/groups",
            params={"status": "READY"},
            timeout=5,
        )
        response.raise_for_status()
        groups = response.json()
        return groups[0] if groups else None

    def _get_cached_group(self) -> Optional[Dict[str, Any]]:
        return None
