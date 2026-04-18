from src.ports.repository import UrlRepository
from src.domain.entities import Url
from src.domain.utils import base62_converter


class UrlShortenerService:
    def __init__(self, repository: UrlRepository):
        self.repository = repository

    def execute(self, long_url: str) -> Url:
        url_id = self.repository.save_url(long_url)
        generated_alias = base62_converter(url_id)
        self.repository.update_url_alias(url_id, generated_alias)
        return self.repository.get_url_by_alias(generated_alias)
