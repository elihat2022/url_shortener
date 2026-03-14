from src.application.ports.url_repository import URL_Repository
from src.domain.base62_converter import base62_converter
from src.domain.url import Url

class UseCaseShortenUrl():
    def __init__(self, repository: URL_Repository):
        self.repository = repository

    def execute(self, long_url: str) -> Url:
        url_id = self.repository.save_url(long_url)
        generated_alias = base62_converter(url_id)
        self.repository.update_url_alias(url_id, generated_alias)
        final_url =self.repository.get_url_by_alias(generated_alias)
        return final_url