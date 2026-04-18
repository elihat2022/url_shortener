from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities import Url


class UrlRepository(ABC):
    @abstractmethod
    def save_url(self, url: str) -> int:
        pass

    @abstractmethod
    def update_url_alias(self, url_id: int, alias: str) -> None:
        pass

    @abstractmethod
    def get_url_by_alias(self, alias: str) -> Optional[Url]:
        pass
